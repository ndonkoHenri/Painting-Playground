from typing import Union

from kivy.graphics import Line, Color
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.pickers import MDColorPicker


class PaintApp(MDApp):

    def build(self):
        """
        The build function is the main entry point for the build system. It
        creates a new Builder object.
        :return: A MainScreen Object containing the main screen to the app
        """

        self.canvas_widget = CanvasWidget()
        self.canvas_widget.set_canvas_color('#000000')  # initial black color

        return self.canvas_widget


class CanvasWidget(Widget):
    line_thickness = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color_picker = MDColorPicker(size_hint=(0.45, 0.85))

    def set_canvas_color(self, hex):
        """
        The set_canvas_color function sets the background color of the canvas i.e the color of the line.

        :param hex: the hex-color-code to apply
        """
        try:
            self.canvas.add(Color(*get_color_from_hex(hex)))
            self.ids.btn_color_picker.text_color = get_color_from_hex(hex)
        except Exception as e:
            if isinstance(hex, list):
                self.canvas.add(Color(*hex))
                self.ids.btn_color_picker.text_color = tuple(hex)
                self.ids.btn_color_picker.icon_color = tuple(hex)

            else:
                print(e)

    def on_touch_down(self, touch):
        """
        The on_touch_down function is called when the user touches the screen.
        It is responsible for recording where they touched, and if it was on a widget,
        grabbing that widget so that we can manipulate it later.  If not, then we just
        return false to allow other widgets to accept the touch.

        :param touch: Stores the information about the touch
        """

        if Widget.on_touch_down(self, touch):
            return

        touch.ud["current_line"] = Line(points=(touch.x, touch.y), width=self.line_thickness)
        self.draw_on_canvas(touch.ud['current_line'].points)

    def on_touch_move(self, touch):
        """
        The on_touch_move function is called whenever the user moves their finger on the screen.
        It adds the point where the touch occurred to the currently drawned line(stored in touch.ud).
        It draws it on the canvas using draw_on_canvas.

        :param touch: Stores the information about the touch
        """
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points += (touch.x, touch.y)
            self.draw_on_canvas(touch.ud['current_line'].points)

    def draw_on_canvas(self, points):
        """
        The draw_on_canvas function draws the points on the canvas.
        It takes in a list of points and creates/updates lines on the canvas.
        """
        with self.canvas:
            Line(points=points, width=self.line_thickness)

    def clear_canvas(self):
        """
        The clear_canvas function clears the canvas of all widgets and then redraws them. This is necessary because
        when a widget is removed from the parent, it's canvas gets cleared. However, if we want to animate our
        widgets (like in this case), we need to keep track of what was drawn on the canvas so that we can draw it
        again later.
        """
        saved_children = self.children[:]  # [:] is used for copying! Creates a new pointer for the new variable
        self.clear_widgets()

        self.canvas.clear()
        for child in saved_children:
            self.add_widget(child)

    def open_color_picker(self):

        self.color_picker.open()
        self.color_picker.bind(
            on_select_color=self.on_select_color,
            on_release=self.get_selected_color,
        )

    def get_selected_color(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''

        self.set_canvas_color(selected_color)

        self.color_picker.dismiss()

    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''Called when a gradient image is clicked.'''


class ColorButton(ToggleButton):
    """
    A custom toggle button used for the colors.
    """


class LineTypeButton(ToggleButton):
    pass


if __name__ == "__main__":
    from kivy import Config

    Config.set("graphics", "height", "760")  # set the windows height
    Config.set("graphics", "width", "540")  # set the windows width
    # we disable a debug mode functionality( comment the line below and do a right-click in window to see more clearly)
    Config.set("input", "mouse", "mouse,disable_multitouch")

    from kivy.core.window import Window

    # the apps background color( white in this case)
    Window.clearcolor = get_color_from_hex("#FFFFFF")

    # running the app
    PaintApp().run()
