"""
任务管理器
管理TTS合成任务的执行
"""
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
from tqdm import tqdm


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TTSTask:
    """TTS任务"""
    task_id: int
    text: str
    output_path: str
    chapter_title: str = ""
    status: TaskStatus = TaskStatus.PENDING
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class TaskManager:
    """任务管理器"""

    def __init__(self, max_workers: int = 4):
        """
        初始化任务管理器

        Args:
            max_workers: 最大并发数
        """
        self.max_workers = max_workers
        self.tasks: List[TTSTask] = []
        self.completed_count = 0
        self.failed_count = 0
        logger.info(f"任务管理器初始化 (最大并发: {max_workers})")

    def add_task(
        self,
        task_id: int,
        text: str,
        output_path: str,
        chapter_title: str = "",
        metadata: Dict = None
    ) -> TTSTask:
        """
        添加任务

        Args:
            task_id: 任务ID
            text: 文本内容
            output_path: 输出路径
            chapter_title: 章节标题
            metadata: 元数据

        Returns:
            任务对象
        """
        task = TTSTask(
            task_id=task_id,
            text=text,
            output_path=output_path,
            chapter_title=chapter_title,
            metadata=metadata or {}
        )
        self.tasks.append(task)
        return task

    def add_tasks_batch(self, task_list: List[Dict]) -> int:
        """
        批量添加任务

        Args:
            task_list: 任务列表，每个任务为字典

        Returns:
            添加的任务数
        """
        count = 0
        for task_data in task_list:
            self.add_task(
                task_id=task_data.get('task_id', len(self.tasks)),
                text=task_data['text'],
                output_path=task_data['output_path'],
                chapter_title=task_data.get('chapter_title', ''),
                metadata=task_data.get('metadata', {})
            )
            count += 1

        logger.info(f"批量添加 {count} 个任务")
        return count

    async def execute_async(
        self,
        tts_engine,
        progress_callback: Optional[Callable] = None,
        show_progress: bool = True
    ) -> Dict:
        """
        异步执行所有任务

        Args:
            tts_engine: TTS引擎实例
            progress_callback: 进度回调函数
            show_progress: 是否显示进度条

        Returns:
            执行结果统计
        """
        logger.info(f"开始执行 {len(self.tasks)} 个任务...")
        self.completed_count = 0
        self.failed_count = 0

        # 创建进度条
        pbar = tqdm(total=len(self.tasks), desc="合成进度") if show_progress else None

        # 使用信号量限制并发
        semaphore = asyncio.Semaphore(self.max_workers)

        async def execute_single_task(task: TTSTask):
            """执行单个任务"""
            async with semaphore:
                try:
                    task.status = TaskStatus.RUNNING

                    # 确保输出目录存在
                    Path(task.output_path).parent.mkdir(parents=True, exist_ok=True)

                    # 执行TTS合成
                    success = await tts_engine.synthesize(task.text, task.output_path)

                    if success:
                        task.status = TaskStatus.COMPLETED
                        self.completed_count += 1
                    else:
                        task.status = TaskStatus.FAILED
                        task.error = "合成失败"
                        self.failed_count += 1

                except Exception as e:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                    self.failed_count += 1
                    logger.error(f"任务 {task.task_id} 失败: {e}")

                finally:
                    if pbar:
                        pbar.update(1)
                    if progress_callback:
                        progress_callback(task)

        # 并发执行所有任务
        await asyncio.gather(*[execute_single_task(task) for task in self.tasks])

        if pbar:
            pbar.close()

        # 统计结果
        result = {
            'total': len(self.tasks),
            'completed': self.completed_count,
            'failed': self.failed_count,
            'success_rate': self.completed_count / len(self.tasks) if self.tasks else 0
        }

        logger.success(f"任务执行完成: {self.completed_count}/{len(self.tasks)} 成功")
        return result

    def execute_sync(
        self,
        tts_engine,
        progress_callback: Optional[Callable] = None,
        show_progress: bool = True
    ) -> Dict:
        """
        同步执行所有任务

        Args:
            tts_engine: TTS引擎实例
            progress_callback: 进度回调
            show_progress: 是否显示进度

        Returns:
            执行结果统计
        """
        # 创建事件循环
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            self.execute_async(tts_engine, progress_callback, show_progress)
        )

    def get_failed_tasks(self) -> List[TTSTask]:
        """获取失败的任务"""
        return [task for task in self.tasks if task.status == TaskStatus.FAILED]

    def get_completed_tasks(self) -> List[TTSTask]:
        """获取完成的任务"""
        return [task for task in self.tasks if task.status == TaskStatus.COMPLETED]

    def retry_failed(self, tts_engine) -> Dict:
        """
        重试失败的任务

        Args:
            tts_engine: TTS引擎

        Returns:
            执行结果
        """
        failed_tasks = self.get_failed_tasks()
        if not failed_tasks:
            logger.info("没有失败的任务需要重试")
            return {'total': 0, 'completed': 0, 'failed': 0}

        logger.info(f"重试 {len(failed_tasks)} 个失败任务")

        # 重置失败任务状态
        for task in failed_tasks:
            task.status = TaskStatus.PENDING
            task.error = None

        # 临时替换任务列表
        original_tasks = self.tasks
        self.tasks = failed_tasks

        # 执行重试
        result = self.execute_sync(tts_engine)

        # 恢复任务列表
        self.tasks = original_tasks

        return result

    def clear(self):
        """清空任务"""
        self.tasks.clear()
        self.completed_count = 0
        self.failed_count = 0
        logger.info("任务已清空")

    def get_summary(self) -> Dict:
        """
        获取任务统计

        Returns:
            统计信息
        """
        status_count = {}
        for status in TaskStatus:
            status_count[status.value] = sum(1 for task in self.tasks if task.status == status)

        return {
            'total_tasks': len(self.tasks),
            'status_breakdown': status_count,
            'completed_count': self.completed_count,
            'failed_count': self.failed_count
        }


if __name__ == '__main__':
    # 测试代码
    manager = TaskManager(max_workers=2)

    # 添加测试任务
    manager.add_task(0, "测试文本1", "output/test1.mp3", "第一章")
    manager.add_task(1, "测试文本2", "output/test2.mp3", "第二章")

    # 查看统计
    summary = manager.get_summary()
    print(f"任务统计: {summary}")
