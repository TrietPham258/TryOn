from kivymd.theming import ThemableBehavior, ThemeManager
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout


# Navigation Drawer
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color