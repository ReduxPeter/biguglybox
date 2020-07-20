import kivy
kivy.require('1.0.6')

import asyncio
import websockets

from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation


class TopBarItemWidget(BoxLayout):
    def __init__(self, transparent=False, **kwargs):
        super(TopBarItemWidget, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.padding = [10, 10]
        self.transparent = transparent

        with self.canvas.before:
            Color(0, 0, 0, 0 if self.transparent else 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class TopBarWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(TopBarWidget, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.spacing = kwargs.get('spacing', 10)
        self.padding = 5


class MainScreenWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreenWidget, self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.orientation = 'vertical'
        self.padding = 5
        self.recording = False

        with self.canvas.before:
            self.color = Color(255, 0, 0, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # All temporary stuff
        row1_layout = TopBarWidget()
        audio_status = TopBarItemWidget()
        audio_status.add_widget(Label(text='Audio'))
        row1_layout.add_widget(audio_status)
        row1_layout.add_widget(TopBarItemWidget())

        logo = TopBarItemWidget()
        logo.add_widget(Image(source='logo.png'))
        row1_layout.add_widget(logo)

        row2_layout = TopBarWidget(spacing=0)
        shutter_info = TopBarItemWidget(transparent=True)
        shutter_info.add_widget(Label(text='180 degrees'))
        row2_layout.add_widget(shutter_info)
        iso_info = TopBarItemWidget(transparent=True)
        iso_info.add_widget(Label(text='500'))
        row2_layout.add_widget(iso_info)
        diafragma_info = TopBarItemWidget(transparent=True)
        diafragma_info.add_widget(Label(text='f 1.2'))
        row2_layout.add_widget(diafragma_info)
        nd_info = TopBarItemWidget(transparent=True)
        nd_info.add_widget(Label(text='1.7'))
        row2_layout.add_widget(nd_info)

        row3_layout = TopBarWidget()
        row3_layout.add_widget(TopBarItemWidget())
        row3_layout.add_widget(TopBarItemWidget())
        row3_layout.add_widget(TopBarItemWidget())
        row3_layout.add_widget(TopBarItemWidget())
        row3_layout.add_widget(TopBarItemWidget())

        row4_layout = TopBarWidget()
        row4_layout.add_widget(TopBarItemWidget())
        row4_layout.add_widget(TopBarItemWidget())
        row4_layout.add_widget(TopBarItemWidget())
        row4_layout.add_widget(TopBarItemWidget())

        self.add_widget(row1_layout)
        self.add_widget(row2_layout)
        self.add_widget(row3_layout)
        self.add_widget(row4_layout)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'r':
            self.toggle_record()
        return True

    def start_record(self):
        self.recording = True
        self.color.a = 0
        anim = Animation(duration=0.3, a=1.0)
        anim.start(self.color)

    def stop_record(self):
        self.recording = False
        self.color.a = 1
        anim = Animation(duration=0.3, a=0.0)
        anim.start(self.color)

    def toggle_record(self):
        if self.recording is True:
            self.stop_record()
        else:
            self.start_record()


class BigUglyBoxApp(App):
    def build(self):
        main_screen = MainScreenWidget()
        return main_screen


if __name__ == '__main__':
    # Window.fullscreen = True
    Window.size = (500, 280)
    BigUglyBoxApp().run()
