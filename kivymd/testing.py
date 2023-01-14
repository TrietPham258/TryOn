from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
"""
This virtual keyboard has two mode:

    docked mode (VKeyboard.docked = True)When only one person is utilizing the computer, such as a tablet or personal computer, docker mode is commonly used.
    free mode: (VKeyboard.docked = False) Typically used on multi touch surfaces. Multiple virtual keyboards can be utilized on the screen in this mode.

You must explicitly call VKeyboard.setup mode() if the docked mode changes; 
otherwise, the change will have no effect. The VKeyboard, which is constructed on top of a Scatter, will 
change the scatter's behavior and position the keyboard near the target during that call 
(if target and docked mode are set).
"""

class MainApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = "Red"
        
        self.label = Label(text="Type Something",  font_size="20sp")
        # Define Layout
        layout = GridLayout(cols=1)
        # Define VKeyboard
        keyboard = VKeyboard(on_key_up = self.key_up) #on_key_up/on_key_down

        layout.add_widget(self.label)
        layout.add_widget(keyboard)
        return layout

    def key_up(self, keyboard, keycode, *args): #keycode: the thing we press
        if isinstance(keycode, tuple):
            keycode = keycode[1]
        
        # Tracking typed character
        thing = "" if self.label.text == "Type Something" else self.label.text
        
        # Backspace
        if keycode == "backspace":
            thing = thing[:-1]
            keycode = ""
        # Spacebar
        if keycode == "spacebar":
            keycode = " "

        thing = f"{thing}{keycode}"
        # Update Label
        self.label.text = thing

MainApp().run()