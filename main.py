import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import math  # <--- اضافه کردن کتابخانه ریاضی

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class MainLayout(BoxLayout):
    display = ObjectProperty(None)
    sci_grid = ObjectProperty(None) # <--- ارجاع به پنل مهندسی
    def adjust_font_size(self):
        """
        این تابع سایز فونت را بر اساس تعداد کاراکترها تنظیم می‌کند.
        """
        text_len = len(self.display.text)
        base_font_size = 85  # سایز اصلی فونت
        char_limit = 10      # تعداد کاراکتری که با سایز اصلی جا می‌شود

        if text_len > char_limit:
            # فرمول کاهش سایز: (حد مجاز / طول فعلی) * سایز اصلی
            new_size = (char_limit / text_len) * base_font_size
            # جلوگیری از ریز شدن بیش از حد (کمتر از ۳۰ نشود)
            self.display.font_size = max(new_size, 30)
        else:
            self.display.font_size = base_font_size

    def toggle_eng(self):
        # تغییر منطق باز شدن پنل
        if self.sci_grid.height == 0:
            # اینجا مهم است: به جای ارتفاع پیکسلی، وزن (Ratio) می‌دهیم
            # 0.45 یعنی حدود 45 درصد ارتفاع فضای موجود را بگیرد
            self.sci_grid.size_hint_y = 0.45
            self.sci_grid.opacity = 1
        else:
            # حالت بسته
            self.sci_grid.size_hint_y = None
            self.sci_grid.height = 0
            self.sci_grid.opacity = 0

    def calc(self, expression):
        if expression:
            try:
                expr = expression.replace('×', '*').replace('÷', '/')
                expr = expr.replace('^', '**')
                
                allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

                # --- 1. توابع مثلثاتی (ورودی درجه -> تبدیل به رادیان) ---
                allowed_names['sin'] = lambda x: math.sin(math.radians(x))
                allowed_names['cos'] = lambda x: math.cos(math.radians(x))
                allowed_names['tan'] = lambda x: math.tan(math.radians(x))
                # کتانژانت: 1 تقسیم بر تانژانت
                allowed_names['cot'] = lambda x: 1 / math.tan(math.radians(x))

                # --- 2. توابع معکوس (خروجی رادیان -> تبدیل به درجه) ---
                # asin, acos, atan در پایتون موجودند
                allowed_names['asin'] = lambda x: math.degrees(math.asin(x))
                allowed_names['acos'] = lambda x: math.degrees(math.acos(x))
                allowed_names['atan'] = lambda x: math.degrees(math.atan(x))
                # آرک‌کتانژانت: atan(1/x)
                allowed_names['acot'] = lambda x: math.degrees(math.atan(1/x))

                # --- 3. نگاشت نام‌های طولانی به کوتاه (اختیاری) ---
                # اگر کاربر بنویسد arcsin، ما آن را به asin وصل می‌کنیم
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
