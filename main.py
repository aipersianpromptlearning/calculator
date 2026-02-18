import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import math
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class MainLayout(BoxLayout):
    display = ObjectProperty(None)
    sci_grid = ObjectProperty(None)
    def adjust_font_size(self):
        text_len = len(self.display.text)
        base_font_size = 85
        char_limit = 10
        if text_len > char_limit:
            new_size = (char_limit / text_len) * base_font_size
            self.display.font_size = max(new_size, 30)
        else:
            self.display.font_size = base_font_size
    def toggle_eng(self):
        if self.sci_grid.height == 0:
            self.sci_grid.size_hint_y = 0.45
            self.sci_grid.opacity = 1
        else:
            self.sci_grid.size_hint_y = None
            self.sci_grid.height = 0
            self.sci_grid.opacity = 0

    def calc(self, expression):
        if expression:
            try:
                expr = expression.replace('×', '*').replace('÷', '/')
                expr = expr.replace('^', '**')
                
                allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                allowed_names['sin'] = lambda x: math.sin(math.radians(x))
                allowed_names['cos'] = lambda x: math.cos(math.radians(x))
                allowed_names['tan'] = lambda x: math.tan(math.radians(x))
                allowed_names['cot'] = lambda x: 1 / math.tan(math.radians(x))
                allowed_names['asin'] = lambda x: math.degrees(math.asin(x))
                allowed_names['acos'] = lambda x: math.degrees(math.acos(x))
                allowed_names['atan'] = lambda x: math.degrees(math.atan(x))
                allowed_names['acot'] = lambda x: math.degrees(math.atan(1/x))
                allowed_names['arcsin'] = allowed_names['asin']
                allowed_names['arccos'] = allowed_names['acos']
                allowed_names['arctan'] = allowed_names['atan']
                allowed_names['arccot'] = allowed_names['acot']

                result = eval(expr, {"__builtins__": None}, allowed_names)
                result = round(result, 10)
                self.display.text = str(result)
                self.adjust_font_size()
            except Exception:
                self.display.text = "Error"

class MyCalculatorApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    MyCalculatorApp().run()

