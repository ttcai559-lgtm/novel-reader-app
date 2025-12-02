"""
TXT小说转有声读物 - Android APP主程序
使用Kivy框架开发
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
import asyncio
import threading
from pathlib import Path


class HomeScreen(Screen):
    """主页面 - 文件选择和转换"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 标题
        title = Label(
            text='📚 TXT小说转有声读物',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)

        # 文件选择器
        self.file_chooser = FileChooserListView(
            filters=['*.txt'],
            size_hint=(1, 0.4)
        )
        layout.add_widget(self.file_chooser)

        # 选中文件显示
        self.selected_file_label = Label(
            text='未选择文件',
            size_hint=(1, 0.08),
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(self.selected_file_label)

        # 音色选择
        voice_layout = BoxLayout(size_hint=(1, 0.08), spacing=10)
        voice_layout.add_widget(Label(text='音色:', size_hint=(0.3, 1)))
        self.voice_spinner = Spinner(
            text='晓晓(温柔女声)',
            values=(
                '晓晓(温柔女声)',
                '晓伊(甜美女声)',
                '晓梦(少女音)',
                '云希(青年男声)',
                '云扬(磁性男声)',
                '云健(沉稳男声)'
            ),
            size_hint=(0.7, 1)
        )
        voice_layout.add_widget(self.voice_spinner)
        layout.add_widget(voice_layout)

        # 语速控制
        speed_layout = BoxLayout(size_hint=(1, 0.08), spacing=10)
        speed_layout.add_widget(Label(text='语速:', size_hint=(0.3, 1)))
        self.speed_slider = Slider(
            min=0.5, max=2.0, value=1.0,
            size_hint=(0.5, 1)
        )
        self.speed_label = Label(text='1.0x', size_hint=(0.2, 1))
        self.speed_slider.bind(value=self.on_speed_change)
        speed_layout.add_widget(self.speed_slider)
        speed_layout.add_widget(self.speed_label)
        layout.add_widget(speed_layout)

        # 转换按钮
        self.convert_btn = Button(
            text='🎙️ 开始转换',
            size_hint=(1, 0.12),
            background_color=(0.2, 0.6, 1, 1),
            font_size='18sp'
        )
        self.convert_btn.bind(on_press=self.start_conversion)
        layout.add_widget(self.convert_btn)

        # 进度条
        self.progress_bar = ProgressBar(
            max=100,
            size_hint=(1, 0.06)
        )
        layout.add_widget(self.progress_bar)

        # 状态标签
        self.status_label = Label(
            text='准备就绪',
            size_hint=(1, 0.08),
            color=(0.3, 0.8, 0.3, 1)
        )
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def on_speed_change(self, instance, value):
        """语速变化回调"""
        self.speed_label.text = f'{value:.1f}x'

    def start_conversion(self, instance):
        """开始转换"""
        if not self.file_chooser.selection:
            self.status_label.text = '❌ 请先选择TXT文件'
            self.status_label.color = (1, 0, 0, 1)
            return

        file_path = self.file_chooser.selection[0]
        self.selected_file_label.text = f'📄 {Path(file_path).name}'

        # 获取音色映射
        voice_map = {
            '晓晓(温柔女声)': 'zh-CN-XiaoxiaoNeural',
            '晓伊(甜美女声)': 'zh-CN-XiaoyiNeural',
            '晓梦(少女音)': 'zh-CN-XiaomengNeural',
            '云希(青年男声)': 'zh-CN-YunxiNeural',
            '云扬(磁性男声)': 'zh-CN-YunyangNeural',
            '云健(沉稳男声)': 'zh-CN-YunjianNeural'
        }
        voice = voice_map.get(self.voice_spinner.text, 'zh-CN-XiaoxiaoNeural')
        speed = self.speed_slider.value

        # 禁用按钮
        self.convert_btn.disabled = True
        self.status_label.text = '🔄 正在转换...'
        self.status_label.color = (1, 0.8, 0, 1)

        # 在后台线程转换
        thread = threading.Thread(
            target=self.convert_in_background,
            args=(file_path, voice, speed)
        )
        thread.start()

    def convert_in_background(self, file_path, voice, speed):
        """后台转换（调用Python核心代码）"""
        try:
            # 导入核心模块
            from novel_to_audio import NovelToAudio

            converter = NovelToAudio()

            # 设置进度回调
            def update_progress(task):
                progress = (task.task_id / 100) * 100  # 简化
                Clock.schedule_once(
                    lambda dt: setattr(self.progress_bar, 'value', progress)
                )

            # 转换
            result = converter.convert(
                novel_path=file_path,
                voice=voice,
                merge=True
            )

            # 更新UI
            Clock.schedule_once(lambda dt: self.on_conversion_complete(result))

        except Exception as e:
            Clock.schedule_once(lambda dt: self.on_conversion_error(str(e)))

    def on_conversion_complete(self, result):
        """转换完成"""
        self.convert_btn.disabled = False
        self.progress_bar.value = 100
        self.status_label.text = f'✅ 转换完成! ({result["tasks_completed"]}个音频)'
        self.status_label.color = (0.3, 0.8, 0.3, 1)

        # 切换到播放器页面
        self.manager.current = 'player'
        self.manager.get_screen('player').load_audiobook(result['merged_file'])

    def on_conversion_error(self, error):
        """转换出错"""
        self.convert_btn.disabled = False
        self.progress_bar.value = 0
        self.status_label.text = f'❌ 转换失败: {error}'
        self.status_label.color = (1, 0, 0, 1)


class PlayerScreen(Screen):
    """播放器页面"""

    current_position = NumericProperty(0)
    total_duration = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None
        self.is_playing = False
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 返回按钮
        back_btn = Button(
            text='← 返回',
            size_hint=(1, 0.08),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        # 标题
        self.title_label = Label(
            text='🎧 有声读物播放器',
            size_hint=(1, 0.1),
            font_size='22sp',
            bold=True
        )
        layout.add_widget(self.title_label)

        # 封面（占位）
        cover_layout = BoxLayout(size_hint=(1, 0.3))
        cover = Label(text='📚', font_size='120sp')
        cover_layout.add_widget(cover)
        layout.add_widget(cover_layout)

        # 当前章节
        self.chapter_label = Label(
            text='准备播放...',
            size_hint=(1, 0.08),
            font_size='16sp'
        )
        layout.add_widget(self.chapter_label)

        # 进度条
        self.play_progress = Slider(
            min=0, max=100, value=0,
            size_hint=(1, 0.08)
        )
        self.play_progress.bind(on_touch_up=self.seek_audio)
        layout.add_widget(self.play_progress)

        # 时间显示
        time_layout = BoxLayout(size_hint=(1, 0.06))
        self.current_time_label = Label(text='00:00')
        self.total_time_label = Label(text='00:00')
        time_layout.add_widget(self.current_time_label)
        time_layout.add_widget(Label(text=''))  # 占位
        time_layout.add_widget(self.total_time_label)
        layout.add_widget(time_layout)

        # 播放控制按钮
        controls_layout = BoxLayout(size_hint=(1, 0.12), spacing=15)

        # 后退10秒
        back_10_btn = Button(text='⏪ 10s')
        back_10_btn.bind(on_press=self.skip_backward)
        controls_layout.add_widget(back_10_btn)

        # 播放/暂停
        self.play_pause_btn = Button(
            text='▶️ 播放',
            background_color=(0.2, 0.6, 1, 1)
        )
        self.play_pause_btn.bind(on_press=self.toggle_play)
        controls_layout.add_widget(self.play_pause_btn)

        # 前进10秒
        forward_10_btn = Button(text='10s ⏩')
        forward_10_btn.bind(on_press=self.skip_forward)
        controls_layout.add_widget(forward_10_btn)

        layout.add_widget(controls_layout)

        # 倍速控制
        speed_layout = BoxLayout(size_hint=(1, 0.08), spacing=10)
        speed_layout.add_widget(Label(text='播放速度:', size_hint=(0.3, 1)))
        self.playback_speed_slider = Slider(
            min=0.5, max=2.0, value=1.0,
            size_hint=(0.5, 1)
        )
        self.playback_speed_label = Label(text='1.0x', size_hint=(0.2, 1))
        self.playback_speed_slider.bind(value=self.on_playback_speed_change)
        speed_layout.add_widget(self.playback_speed_slider)
        speed_layout.add_widget(self.playback_speed_label)
        layout.add_widget(speed_layout)

        self.add_widget(layout)

        # 定时更新进度
        Clock.schedule_interval(self.update_progress, 0.5)

    def load_audiobook(self, audio_path):
        """加载有声书"""
        try:
            self.sound = SoundLoader.load(audio_path)
            if self.sound:
                self.total_duration = self.sound.length
                self.chapter_label.text = f'📖 {Path(audio_path).stem}'
                self.total_time_label.text = self.format_time(self.total_duration)
        except Exception as e:
            self.chapter_label.text = f'❌ 加载失败: {e}'

    def toggle_play(self, instance):
        """播放/暂停切换"""
        if not self.sound:
            return

        if self.is_playing:
            self.sound.stop()
            self.play_pause_btn.text = '▶️ 播放'
            self.is_playing = False
        else:
            self.sound.play()
            self.play_pause_btn.text = '⏸️ 暂停'
            self.is_playing = True

    def skip_backward(self, instance):
        """后退10秒"""
        if self.sound:
            new_pos = max(0, self.sound.get_pos() - 10)
            self.sound.seek(new_pos)

    def skip_forward(self, instance):
        """前进10秒"""
        if self.sound:
            new_pos = min(self.total_duration, self.sound.get_pos() + 10)
            self.sound.seek(new_pos)

    def seek_audio(self, instance, touch):
        """拖动进度条"""
        if self.sound and instance.collide_point(*touch.pos):
            seek_pos = (self.play_progress.value / 100) * self.total_duration
            self.sound.seek(seek_pos)

    def on_playback_speed_change(self, instance, value):
        """播放速度变化"""
        self.playback_speed_label.text = f'{value:.1f}x'
        # Kivy的SoundLoader不直接支持变速，需要用pydub预处理

    def update_progress(self, dt):
        """更新播放进度"""
        if self.sound and self.is_playing:
            current = self.sound.get_pos()
            if self.total_duration > 0:
                self.play_progress.value = (current / self.total_duration) * 100
                self.current_time_label.text = self.format_time(current)

    @staticmethod
    def format_time(seconds):
        """格式化时间"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f'{minutes:02d}:{secs:02d}'


class NovelReaderApp(App):
    """主应用"""

    def build(self):
        # 创建屏幕管理器
        sm = ScreenManager()

        # 添加页面
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(PlayerScreen(name='player'))

        return sm


if __name__ == '__main__':
    NovelReaderApp().run()
