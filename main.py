# filepath: d:\code\image\image\main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from main_app import IDCopyApp
from main3 import ImageResizerApp

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Button(text='身份证复印功能', on_press=self.launch_idcopy))
        layout.add_widget(Button(text='尺寸调整功能', on_press=self.launch_resizer))
        return layout

    def launch_idcopy(self, instance):
        IDCopyApp().run()

    def launch_resizer(self, instance):
        ImageResizerApp().run()

if __name__ == "__main__":
    MainApp().run()