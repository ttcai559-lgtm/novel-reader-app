"""
TXT小说转有声读物 - Android APP主程序（简化版）
使用Kivy框架开发
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class NovelReaderApp(App):
    """小说阅读器主应用"""

    def build(self):
        """构建UI"""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 标题
        title = Label(
            text='📚 TXT小说转有声读物',
            size_hint=(1, 0.2),
            font_size='24sp'
        )
        layout.add_widget(title)

        # 版本信息
        version_label = Label(
            text='版本 1.0.0\n基础版本 - 测试打包',
            size_hint=(1, 0.3),
            font_size='16sp'
        )
        layout.add_widget(version_label)

        # 说明文字
        info_label = Label(
            text='这是一个基础测试版本\n'
                 '用于验证APK打包流程\n'
                 '完整功能将在后续版本中添加',
            size_hint=(1, 0.3),
            font_size='14sp',
            halign='center'
        )
        layout.add_widget(info_label)

        # 测试按钮
        test_btn = Button(
            text='✓ APP运行正常',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='18sp'
        )
        test_btn.bind(on_press=self.on_test_click)
        layout.add_widget(test_btn)

        return layout

    def on_test_click(self, instance):
        """测试按钮点击"""
        instance.text = '✓ 测试成功！APP正常工作'
        instance.background_color = (0.2, 0.6, 1, 1)


if __name__ == '__main__':
    NovelReaderApp().run()
