"""
TXT小说转有声读物 - Android APP主程序
使用Kivy框架开发
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class NovelReaderApp(App):
    """小说阅读器主应用"""

    def build(self):
        """构建UI"""
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 标题
        title = Label(
            text='TXT小说转有声读物',
            size_hint=(1, 0.15),
            font_size='20sp',
            bold=True
        )
        self.layout.add_widget(title)

        # 状态显示区域
        self.status_label = Label(
            text='欢迎使用！点击下方按钮测试',
            size_hint=(1, 0.2),
            font_size='16sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        self.layout.add_widget(self.status_label)

        # 计数器显示
        self.counter_label = Label(
            text='点击次数: 0',
            size_hint=(1, 0.15),
            font_size='18sp',
            bold=True,
            color=(1, 0.5, 0, 1)
        )
        self.layout.add_widget(self.counter_label)
        self.click_count = 0

        # 测试按钮1
        btn1 = Button(
            text='点我测试 1',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 1, 1),
            font_size='16sp'
        )
        btn1.bind(on_press=self.on_button1_click)
        self.layout.add_widget(btn1)

        # 测试按钮2
        btn2 = Button(
            text='点我测试 2',
            size_hint=(1, 0.15),
            background_color=(1, 0.5, 0, 1),
            font_size='16sp'
        )
        btn2.bind(on_press=self.on_button2_click)
        self.layout.add_widget(btn2)

        # 文本输入框
        self.text_input = TextInput(
            text='在这里输入文字测试...',
            size_hint=(1, 0.2),
            multiline=False,
            font_size='14sp'
        )
        self.layout.add_widget(self.text_input)

        return self.layout

    def on_button1_click(self, instance):
        """按钮1点击事件"""
        self.click_count += 1
        self.counter_label.text = f'点击次数: {self.click_count}'
        self.status_label.text = '按钮1被点击了！'
        self.status_label.color = (0.2, 0.8, 0.2, 1)
        instance.background_color = (0.2, 0.8, 0.2, 1)

    def on_button2_click(self, instance):
        """按钮2点击事件"""
        self.click_count += 1
        self.counter_label.text = f'点击次数: {self.click_count}'
        self.status_label.text = '按钮2被点击了！'
        self.status_label.color = (1, 0.2, 0.2, 1)
        instance.background_color = (1, 0.2, 0.2, 1)


if __name__ == '__main__':
    NovelReaderApp().run()
