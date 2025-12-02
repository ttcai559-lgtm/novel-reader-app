"""
音频播放器
支持播放控制、倍速播放、进度跳转等功能
"""
import pygame
from pathlib import Path
from typing import Optional, Callable
from enum import Enum
from loguru import logger
import time


class PlayerState(Enum):
    """播放器状态"""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class AudioPlayer:
    """音频播放器"""

    def __init__(self):
        """初始化音频播放器"""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.current_file: Optional[str] = None
        self.state = PlayerState.STOPPED
        self.speed = 1.0  # 播放速度
        self.volume = 1.0
        self._paused_position = 0
        logger.info("音频播放器初始化完成")

    def load(self, file_path: str) -> bool:
        """
        加载音频文件

        Args:
            file_path: 音频文件路径

        Returns:
            是否成功加载
        """
        try:
            if not Path(file_path).exists():
                logger.error(f"文件不存在: {file_path}")
                return False

            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            self.state = PlayerState.STOPPED
            logger.success(f"音频文件已加载: {file_path}")
            return True

        except Exception as e:
            logger.error(f"加载音频失败: {e}")
            return False

    def play(self, start_pos: float = 0.0) -> bool:
        """
        播放音频

        Args:
            start_pos: 起始位置（秒）

        Returns:
            是否成功播放
        """
        try:
            if self.current_file is None:
                logger.warning("未加载音频文件")
                return False

            pygame.mixer.music.play(start=start_pos)
            pygame.mixer.music.set_volume(self.volume)
            self.state = PlayerState.PLAYING
            logger.info(f"开始播放（速度: {self.speed}x, 音量: {self.volume}）")
            return True

        except Exception as e:
            logger.error(f"播放失败: {e}")
            return False

    def pause(self):
        """暂停播放"""
        if self.state == PlayerState.PLAYING:
            pygame.mixer.music.pause()
            self.state = PlayerState.PAUSED
            logger.info("播放已暂停")

    def resume(self):
        """恢复播放"""
        if self.state == PlayerState.PAUSED:
            pygame.mixer.music.unpause()
            self.state = PlayerState.PLAYING
            logger.info("播放已恢复")

    def stop(self):
        """停止播放"""
        pygame.mixer.music.stop()
        self.state = PlayerState.STOPPED
        logger.info("播放已停止")

    def set_volume(self, volume: float):
        """
        设置音量

        Args:
            volume: 音量 (0.0 - 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        logger.info(f"音量已设置为: {self.volume:.1%}")

    def set_speed(self, speed: float):
        """
        设置播放速度（需要重新加载）
        注意: pygame原生不支持变速，需要使用pydub处理

        Args:
            speed: 播放速度 (0.5 - 2.0)
        """
        self.speed = max(0.5, min(2.0, speed))
        logger.info(f"播放速度已设置为: {self.speed}x")
        logger.warning("速度变化需要使用pydub重新处理音频")

    def get_position(self) -> float:
        """
        获取当前播放位置

        Returns:
            当前位置（秒）
        """
        if self.state == PlayerState.PLAYING:
            return pygame.mixer.music.get_pos() / 1000.0
        return 0.0

    def seek(self, position: float):
        """
        跳转到指定位置

        Args:
            position: 目标位置（秒）
        """
        if self.current_file:
            was_playing = self.state == PlayerState.PLAYING
            self.stop()
            if was_playing:
                self.play(start_pos=position)
            logger.info(f"已跳转到: {position:.1f}秒")

    def is_playing(self) -> bool:
        """检查是否正在播放"""
        return pygame.mixer.music.get_busy() and self.state == PlayerState.PLAYING

    def get_state(self) -> PlayerState:
        """获取播放器状态"""
        return self.state

    def get_info(self) -> dict:
        """
        获取播放器信息

        Returns:
            播放器信息字典
        """
        return {
            'current_file': self.current_file,
            'state': self.state.value,
            'speed': self.speed,
            'volume': self.volume,
            'position': self.get_position(),
            'is_playing': self.is_playing()
        }

    def cleanup(self):
        """清理资源"""
        self.stop()
        pygame.mixer.quit()
        logger.info("音频播放器已关闭")


# 增强版播放器（支持真正的倍速）
class AudioPlayerAdvanced:
    """
    高级音频播放器
    使用pydub实现真正的倍速播放
    """

    def __init__(self):
        """初始化高级播放器"""
        from pydub import AudioSegment
        from pydub.playback import _play_with_simpleaudio

        self.current_audio: Optional[AudioSegment] = None
        self.current_file: Optional[str] = None
        self.playback = None
        self.speed = 1.0
        self.volume = 0  # dB变化
        self.state = PlayerState.STOPPED
        logger.info("高级音频播放器初始化完成")

    def load(self, file_path: str) -> bool:
        """
        加载音频文件

        Args:
            file_path: 音频文件路径

        Returns:
            是否成功
        """
        try:
            from pydub import AudioSegment

            if not Path(file_path).exists():
                logger.error(f"文件不存在: {file_path}")
                return False

            # 加载音频
            self.current_audio = AudioSegment.from_file(file_path)
            self.current_file = file_path
            logger.success(f"音频已加载: {file_path} (时长: {len(self.current_audio)/1000:.1f}秒)")
            return True

        except Exception as e:
            logger.error(f"加载音频失败: {e}")
            return False

    def play(self) -> bool:
        """
        播放音频（应用倍速和音量调整）

        Returns:
            是否成功
        """
        try:
            if self.current_audio is None:
                logger.warning("未加载音频")
                return False

            from pydub.playback import play
            import threading

            # 应用速度调整
            audio = self._apply_speed(self.current_audio, self.speed)

            # 应用音量调整
            audio = audio + self.volume

            # 在后台线程播放
            self.state = PlayerState.PLAYING

            def play_thread():
                try:
                    play(audio)
                    self.state = PlayerState.STOPPED
                except:
                    pass

            thread = threading.Thread(target=play_thread, daemon=True)
            thread.start()

            logger.info(f"开始播放（速度: {self.speed}x）")
            return True

        except Exception as e:
            logger.error(f"播放失败: {e}")
            return False

    def set_speed(self, speed: float):
        """
        设置播放速度

        Args:
            speed: 速度倍数 (0.5 - 2.0)
        """
        self.speed = max(0.5, min(2.0, speed))
        logger.info(f"播放速度设置为: {self.speed}x")

    def set_volume_db(self, db: float):
        """
        设置音量（dB）

        Args:
            db: 音量变化（dB），正数增大，负数减小
        """
        self.volume = max(-20, min(20, db))
        logger.info(f"音量设置为: {self.volume:+.1f}dB")

    @staticmethod
    def _apply_speed(audio, speed: float):
        """
        应用速度变化

        Args:
            audio: AudioSegment对象
            speed: 速度倍数

        Returns:
            调整后的AudioSegment
        """
        if speed == 1.0:
            return audio

        # 方法1: 改变帧率（会改变音调）
        # sound_with_altered_frame_rate = audio._spawn(audio.raw_data, overrides={
        #     "frame_rate": int(audio.frame_rate * speed)
        # })
        # return sound_with_altered_frame_rate.set_frame_rate(audio.frame_rate)

        # 方法2: 使用speedup/slowdown（保持音调，需要pyrubberband或其他库）
        # 这里简化处理，改变采样率
        new_frame_rate = int(audio.frame_rate * speed)
        return audio._spawn(audio.raw_data, overrides={
            "frame_rate": new_frame_rate
        }).set_frame_rate(audio.frame_rate)

    def get_duration(self) -> float:
        """
        获取音频时长

        Returns:
            时长（秒）
        """
        if self.current_audio:
            return len(self.current_audio) / 1000.0
        return 0.0

    def export_with_speed(self, output_path: str, speed: float = None) -> bool:
        """
        导出变速后的音频

        Args:
            output_path: 输出路径
            speed: 速度倍数，None则使用当前速度

        Returns:
            是否成功
        """
        try:
            if self.current_audio is None:
                logger.warning("未加载音频")
                return False

            speed = speed or self.speed
            audio = self._apply_speed(self.current_audio, speed)

            # 导出
            audio.export(output_path, format=Path(output_path).suffix[1:])
            logger.success(f"变速音频已导出: {output_path} (速度: {speed}x)")
            return True

        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False


if __name__ == '__main__':
    # 测试代码
    player = AudioPlayer()

    # 测试基础播放
    # player.load("test_audio.mp3")
    # player.set_volume(0.8)
    # player.play()
    # time.sleep(5)
    # player.pause()
    # time.sleep(2)
    # player.resume()
    # time.sleep(5)
    # player.stop()

    # 测试高级播放器
    # advanced_player = AudioPlayerAdvanced()
    # advanced_player.load("test_audio.mp3")
    # advanced_player.set_speed(1.5)  # 1.5倍速
    # advanced_player.play()
    # time.sleep(10)
