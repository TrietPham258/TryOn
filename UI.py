from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder


class UI(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    Builder.load_string("""


<MDLabel>
    markup: True


<FirstInput@MDTextField>
    id: root.id
    hint_text: root.hint_text
    icon_right: root.icon_right
    size_hint_x: None
    width: 200
    font_size: 18

    # Position
    pos_hint: root.pos_hint
    multiline: False
    max_text_length: root.max_text_length
    mode: "round"

    # Color
    fill_color_normal: 1, 1, 1, 1
    text_color_normal: 0, 0, 0, 1
    hint_text_color_normal: 0, 0, 0, .4
    icon_right_color_normal: 0, 0, 0, 1


<FirstButton@MDRoundFlatButton>
    id: root.id
    text: root.text
    font_size: 15
    pos_hint: {'center_x': .5}
    md_bg_color: get_color_from_hex('#b2a575')
    line_color: 0, 0, 0, 0
    text_color: 1, 1, 1, 1


<Password@MDRelativeLayout>
    size_hint_y: None
    height: text_field.height
    hint_text: ""
    canvas.before:
        Color:
            rgba: 1, 0, 0, 1
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height

    MDTextField:
        id: text_field
        mode: "round"
        password: True
        hint_text: root.hint_text
        size_hint_x: None
        width: 200
        font_size: 18
        fill_color_normal: 1, 1, 1, 1
        text_color_normal: 0, 0, 0, 1
        hint_text_color_normal: 0, 0, 0, .4
        
    MDIconButton:
        icon: "eye-off"
        ripple_scale: .5
        pos_hint: {"center_y": .5}
        pos: text_field.width - self.width + dp(8), 0
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off" 
            text_field.password = False if text_field.password is True else True


<MDIconButton>
    theme_icon_color: "Custom"
    icon_color: (0, 0, 0, 1)
    

<Sample@FitImage>
    source: root.source 
    size_hint: None, None
    size: 60, 80
    pos_hint: {'center_x': .5, 'center_y': .5}


<CloButton>
    id: clobutton
    source: ""
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos

    size_hint: None, None
    size: 60, 80
    pos_hint: {'center_x': .5, 'center_y': .5}


    MDRectangleFlatButton:
        id: clo_button
        md_bg_color: 0, 0, 0, 0
        line_color: 0, 0, 0, 0
        text_color: 0, 0, 0, 0
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: 1, 1
        on_release: 
            app.root.ids.drag_ob.source = root.source
            if app.current_mode == "Sticker Mode": \
            app.root.ids.drag_ob.drag_timeout = 999999999999999999
            
        on_release:
            if app.current_mode == "Automatic Mode": \
            app.root.ids.drag_ob.drag_timeout = 0 
            if app.current_type == "Automatic Shirts" and app.current_mode == "Automatic Mode": \
            app.root.ids.drag_ob.size = 109, 145 
            if app.current_type == "Automatic Shirts" and app.current_mode == "Automatic Mode": \
            app.root.ids.drag_ob.pos = app.root.ids.fitting_image.pos[0] + 88, app.root.ids.fitting_image.pos[1] + 175
        on_release:
            if app.current_type == "Automatic Dresses" and app.current_mode == "Automatic Mode": \
            app.root.ids.drag_ob.size = 248, 330
            if app.current_type == "Automatic Dresses" and app.current_mode == "Automatic Mode": \
            app.root.ids.drag_ob.pos = app.root.ids.fitting_image.pos[0] + 19, app.root.ids.fitting_image.pos[1] + 24
        on_release:
            if app.current_type == "Automatic Shorts" and app.current_mode == "Automatic Mode": \
            app.root.ids.drag_ob.size = 129, 172
            if app.current_type == "Automatic Shorts" and app.current_mode == "Automatic Mode": \
            app.root.ids.drag_ob.pos = app.root.ids.fitting_image.pos[0] + 80, app.root.ids.fitting_image.pos[1] + 69

        Sample:
            source: root.source


<DragObject@DragBehavior+Image>
    # Define the properties for the DragLabel
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 0
    drag_distance: 10
    source: root.source
""")