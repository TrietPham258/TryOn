from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivymd.toast import toast
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivymd.uix.slider import MDSlider
from AppNavigationDrawer import ItemDrawer, ContentNavigationDrawer, DrawerList
from FileManagement import FileManagement
from UI import UI
from Database_sqlite3 import MyDatabase
from kivy.metrics import dp
import sqlite3


class CloButton(MDFloatLayout):
    source = StringProperty()


class EmptyButton(MDFloatLayout):
    pass


class CustomSlider(MDSlider):
    # To reduce the touch area
    def collide_point(self, x, y):
        # Width area, Height area
        w_r, h_r = 80, 0
        return self.x+w_r <= x <= self.right-w_r and self.y+h_r <= y <= self.top-h_r


class Product(MDBoxLayout):
    pass


class ConfirmButton(MDBoxLayout):
    pass


class TailorApp(MDApp, Widget):
    def __init__(self, **kwargs):
        self.icon = "images/App icon 2.png"
        self.title = "Tailor App"
        super().__init__(**kwargs)

        # Class Declaration
        self.file_manage = FileManagement()
        self.db = MyDatabase()

        # Get the physical size of screen (any devices)
        #self.window_sizes = Window.size
        # Example phone size
        self.window_sizes = Window.size = 360, 620

        # Ids list from kv files
        self.id_lst = []

        # Available accounts
        self.accounts = [['admin', 'password'], ['user', 'password'], ["admin", "nice"], ['', '']]

        # Fitting mode
        self.current_mode = "Automatic Mode"
        self.current_type = "Automatic Shirts"

        # Confirm order list
        self.final_order_list = []

    def build(self):
        self.theme_cls.theme_style = "Light"
        Builder.load_file("LogIn.kv")
        Builder.load_file("SignUp.kv")
        Builder.load_file("Homepage.kv")
        Builder.load_file("MeasurementPage.kv")
        Builder.load_file("FittingPage.kv")
        Builder.load_file("FittingRoom.kv")
        Builder.load_file("CheckoutPage.kv")
        return UI(transition=NoTransition())
    
    # Start function
    def on_start(self):
        # Collect id
        self.get_id()
        # Activate the databse
        self.db.build()

        # Icon for Navigation Drawer
        icons_item = {
            # Add icon : 'name' here
        }
        for icon_name in icons_item.keys():
            self.root.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )

        # Add clothes for FittingRoom
        for i in range(1, 4, 2):
            self.root.ids.clothes.ids.box_clothes.add_widget(
                CloButton(source=f"Sample Clothes/Shirt/shirt {i} front.png")
                )

        # Size list - must specify here, can't use self.root.ids.drag_ob.size
        # because of size update with Slider
        self.size_lst = [[99, 132]]
        for i in range(1, 19):
            n = round(i*0.1, 1) + 1
            a = round(self.size_lst[0][0] * n)
            b = round(self.size_lst[0][1] * n)
            self.size_lst.append([a, b])
        

        # Remove the pre-laid slider and label for Automatic Mode
        self.root.ids.fittingroom_layout.remove_widget(self.root.ids.size_slider)
        self.root.ids.fittingroom_layout.remove_widget(self.root.ids.size_label)

        # The order_list need a first Product for kivy to add more (Bug)
        # Removing --> Blank order_list
        self.root.ids.order_list.remove_widget(self.root.ids.example_product)

        
    # Get all id from ids dictionary
    def get_id(self):
        for i in self.root.ids:
            self.id_lst.append(i)

    # Show result on screen
    def announcement(self, text):
        toast(text)

    # Log In
    # *args: user, password
    def logger(self, *args):
        # Check fidelity
        if self.info_fidelity(*args):
            return True
        
    # Sign Up
    def error_text(self, error_type, *args):
        for i in args:
            i.required = True
            i.helper_text_mode = "on_error"
        # Log In error
        if error_type == "wrong login":
            args[1].helper_text = "Incorrect account or password"
        # Sign Up error
        if error_type == "password mismatch":
            args[2].helper_text = "Passwords do not match"
        elif error_type == "info missing":
            for arg in args:
                arg.helper_text = "All boxes need to be filled"

    def info_fidelity(self, *args):
        # Reset previous error
        for i in args:
            i.required = False
            i.helper_text = ""

        # User and password fidelity
        # Log In
        if args[0] == self.root.ids.user:
            if [args[0].text, args[1].text] in self.accounts:
                if args[0].text == "admin" and args[1].text == "password":
                    self.root.ids.account_page.text = 'Admin'
                    self.root.ids.account_page.icon = 'head-cog'
                else:
                    self.root.ids.account_page.text = 'User'
                    self.root.ids.account_page.icon = 'account'
                return True
            else:
                self.error_text("wrong login", *args)

        # Sign Up
        elif args[0] == self.root.ids.signup_user:
            if args[0].text and args[1].text == args[2].text and args[1]:
                # Adding created account
                self.accounts.append([args[0].text, args[1].text])
                return True
            if self.root.ids.signup_password.text != self.root.ids.repeat_password.text:
                self.error_text("password mismatch", *args)
            for i in args:
                if i.text == "":
                    self.error_text("info missing", *args)
                    break
            
        # Reset all text
        self.reset_text_box()
    
    def reset_text_box(self):
        # Reset Log In text
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""
        # Reset Sign Up text
        self.root.ids.signup_user.text = ""
        self.root.ids.signup_password.text = ""
        self.root.ids.repeat_password.text = ""

    # *args: signup_user, signup_password, repeat_password
    def create_account(self, *args):
        # Check required information
        if self.info_fidelity(args[0], args[1], args[2]):
            return True

    # Measurement Page
    def specific_gender(self, text, value):
        inx = self.id_lst.index("bra_size")
        if value:
            if text == "Male":
                self.root.ids[self.id_lst[inx]].hint_text = ""
                self.root.ids[self.id_lst[inx]].disabled = True
            elif text == "Female":
                self.root.ids[self.id_lst[inx]].disabled = False
                self.root.ids[self.id_lst[inx]].hint_text = "34DD/30A"

    def confirm_measurement(self):
        toast("Measurements confirmed")
    
    # Fitting Page
    # Switch between Sticker Mode and Automatic Mode
    def fp_mode(self):
        self.current_mode = "Sticker Mode" if self.current_mode == "Automatic Mode" else "Automatic Mode"
        self.fr_change_clothes_type("Tops")
        self.root.ids.size_slider.value = 0
        if self.current_mode == "Sticker Mode":
            self.root.ids.fittingroom_layout.add_widget(self.root.ids.size_label)
            self.root.ids.fittingroom_layout.add_widget(self.root.ids.size_slider)
            self.root.ids.drag_ob.source = "images/Blank Space.png"
            self.root.ids.drag_ob.size = 99, 132
            
        elif self.current_mode == "Automatic Mode":
            self.root.ids.fittingroom_layout.remove_widget(self.root.ids.size_slider)
            self.root.ids.fittingroom_layout.remove_widget(self.root.ids.size_label)
            self.root.ids.drag_ob.source = "images/Blank Space.png"
            self.root.ids.drag_ob.drag_timeout = 0

    # Fitting Room
    def fr_back(self):
        self.root.current = "screen5"
    
    def fr_change_clothes_type(self, text):
        # Types have 2 more repetitions to avoid out of range IndexError
        types = [["Tops", self.root.ids.tops], 
        ["Dresses", self.root.ids.dresses], 
        ["Bottoms", self.root.ids.bottoms]]

        for i in types:
            if text == i[0]:
                i[1].md_bg_color = get_color_from_hex('#d9d9d9')
            else:  
                i[1].md_bg_color = get_color_from_hex('#ffffff')
        
        # Reset clothes list
        self.root.ids.clothes.ids.box_clothes.clear_widgets()
        self.root.ids.clothes.ids.box_clothes.add_widget(EmptyButton())
        
        # Add clothes for FittingRoom
        if self.current_mode == "Automatic Mode":
            if text == "Tops":  
                self.current_type = "Automatic Shirts"
                for i in range(1, 4, 2):
                    self.root.ids.clothes.ids.box_clothes.add_widget(
                        CloButton(source=f"Sample Clothes/Shirt/shirt {i} front.png")
                        )
            elif text == "Dresses":
                # Example of Ao Dai
                self.current_type = "Automatic Dresses"
                for i in range(1, 2):
                    self.root.ids.clothes.ids.box_clothes.add_widget(
                        CloButton(source=f"Sample Clothes/Dress/ao dai {i} front.png")
                        )
            elif text == "Bottoms":
                self.current_type = "Automatic Shorts"
                for i in range(4, 8):
                    self.root.ids.clothes.ids.box_clothes.add_widget(
                        CloButton(source=f"Sample Clothes/Short/short {i} front.png")
                        )
        elif self.current_mode == "Sticker Mode":
            if text == "Tops":  
                for i in range(1, 8):
                    self.root.ids.clothes.ids.box_clothes.add_widget(
                        CloButton(source=f"Sample Clothes/Shirt/shirt {i} front.png")
                        )
            elif text == "Dresses":
                # Example of Ao Dai
                for i in range(1, 3):
                    self.root.ids.clothes.ids.box_clothes.add_widget(
                        CloButton(source=f"Sample Clothes/Dress/ao dai {i} front.png")
                        )
            elif text == "Bottoms":
                for i in range(1, 8):
                    self.root.ids.clothes.ids.box_clothes.add_widget(
                        CloButton(source=f"Sample Clothes/Short/short {i} front.png")
                        )
            
    # Change clothes size
    def fr_slider(self, *args):
        self.root.ids.drag_ob.size = self.size_lst[int(args[2])]
    
    # Confirm clothes and add clothes to checkout
    def fr_confirm_clothes(self):     
        # Reset the confirm button
        if self.root.ids.drag_ob.source == "images/Blank Space.png":
            pass
        else:
            self.root.ids.order_list.add_widget(Product(source = self.root.ids.drag_ob.source, text=self.root.ids.drag_ob.source[21:29]))
    
    # Clear order_list
    def ck_clear_order(self):
        self.root.ids.order_list.clear_widgets()
        self.final_order_list = []

    # Confirm all order
    def ck_select_orders(self, value, product_name, quantity):
        if value:
            self.final_order_list.append(["value", product_name, int(quantity)])
        elif not value:
            self.final_order_list = self.final_order_list[:-1] 
    
    def ck_confirm_orders(self):
        if self.final_order_list: 
            toast("ORDERS CONFIRMED")

            for a, b, c in self.final_order_list:
                self.db.submit(b, c)
            
        elif not self.final_order_list:
            toast("NONE SELECTED") 


if __name__ == "__main__":
    TailorApp().run()    

# Note
"""
    The Kivy Design Language .kv needs to be saved before the program runs, or else it will not work
"""