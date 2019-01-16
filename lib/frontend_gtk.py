import gi
from gi.overrides.Gdk import Gdk

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from typing import List
from lib.abstract_frontend import Frontend
from lib.multiple_choice import MultipleChoice


class FrontendGtk(Frontend):

    def get_tags(self, available_tags: List[str], allow_custom_tags) -> List[str]:
        selected_tags = _multi_select("Please choose tags: ", available_tags, allow_custom_tags)
        return selected_tags

    def get_user_confirmation(self, prompt: str) -> bool:
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, prompt)
        response = dialog.run()
        dialog.destroy()
        return response == Gtk.ResponseType.YES

    def list_tags(self, files: List[str], tags: List[str]):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Tags on selected files:")
        dialog.format_secondary_text(
            "\n".join(tags)
        )
        dialog.run()
        dialog.destroy()


class TagChoiceDialog(Gtk.Dialog):

    def __init__(self, parent, prompt: str, mc: MultipleChoice, allow_custom_tags: bool):
        Gtk.Dialog.__init__(self, prompt, parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.NONE))
        self.mc = mc
        self.allow_custom_tags = allow_custom_tags
        self.set_default_size(150, 100)
        self.search_input_field = Gtk.Entry()
        self.main_container = None
        self._update_main_container()
        self._format_action_area()
        self.show_all()

    def _update_main_container(self):
        if self.main_container is not None:
            self.main_container.destroy()
        self.main_container = self._build_main_container()
        self.get_content_area().add(self.main_container)
        self.show_all()

    def _build_main_container(self):
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        _set_widget_margins(main_container, 5, 5, 0, 5)
        self.search_input_field.connect("key-release-event", self._on_key_release)
        main_container.add(self.search_input_field)
        self._build_options_box("")
        main_container.add(self.options_box)
        return main_container

    def _build_options_box(self, current_search_string: str):
        self.options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        for option in self.mc.options:
            if current_search_string in option:
                button = Gtk.CheckButton(option)
                button.set_active(self.mc.is_selected(option))
                button.connect("toggled", self.on_button_toggled, option)
                self.options_box.add(button)

    def _update_options_visibility(self, current_search_string: str):
        if self.options_box is not None:
            self.options_box.destroy()
        self._build_options_box(current_search_string)
        self.main_container.add(self.options_box)
        self.show_all()

    def _format_action_area(self):
        action_area = self.get_action_area()
        _set_widget_margins(action_area, 10, 5, 5, 5)
        action_area.set_halign(Gtk.Align.CENTER)

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.mc.select(name)
        else:
            self.mc.unselect(name)

    def _on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Return:  # If Enterkey pressed, reset text
            if self.allow_custom_tags:
                self.mc.select(widget.get_text())
                widget.set_text("")
                self._update_options_visibility("")
        else:
            current_search_string = self.search_input_field.get_text()
            self._update_options_visibility(current_search_string)


def _set_widget_margins(widget: Gtk.Widget, top: int, right: int, bottom: int, left: int):
    widget.set_margin_top(top)
    widget.set_margin_right(right)
    widget.set_margin_bottom(bottom)
    widget.set_margin_left(left)


def _multi_select(prompt: str, options: List[str], allow_custom_tags: bool):
    if len(options) == 0:
        return []
    mc = MultipleChoice(options, True)
    dialog = TagChoiceDialog(None, prompt, mc, allow_custom_tags)
    dialog.run()
    selected_options = mc.selection
    return selected_options
