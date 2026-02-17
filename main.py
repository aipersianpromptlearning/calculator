import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
# اضافه کردن این خط ضروری است
from kivy.properties import ObjectProperty 

class MainLayout(GridLayout):
    # این خط اتصال بین فایل KV و پایتون را برقرار می‌کند
    display = ObjectProperty(None)

    def calc(self, event):
        if event:
            try:
                # محاسبه مقدار
                self.display.text = str(eval(event))
            except Exception:
                self.display.text = "Error"

class MyCalculatorApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    MyCalculatorApp().run()
