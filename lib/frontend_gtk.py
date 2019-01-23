import gi
from gi.overrides.Gdk import Gdk

from lib import autocomplete

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

    def show_message(self, message: str):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
        dialog.run()
        dialog.destroy()


class TagChoiceDialog(Gtk.Dialog):

    def __init__(self, parent, prompt: str, mc: MultipleChoice, allow_custom_tags: bool):
        Gtk.Dialog.__init__(self, prompt, parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.mc = mc
        self.allow_custom_tags = allow_custom_tags
        self.set_default_size(150, 100)
        self.search_input_field = self._build_search_input_field()
        self.main_container = self._build_main_container(self.search_input_field)
        self.scroll = self._build_scroll_window()
        self.main_container.add(self.scroll)
        self.options_box = None
        self._update_options_box("")
        self.get_content_area().add(self.main_container)
        self._format_action_area()
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.show_all()
        self.search_input_field.grab_focus()

    def _build_scroll_window(self) -> Gtk.ScrolledWindow:
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(500)
        return scroll

    def _build_search_input_field(self) -> Gtk.Entry:
        input_field = Gtk.Entry()
        input_field.connect("key-release-event", self._on_key_release)
        return input_field

    def _build_main_container(self, search_input_field: Gtk.Entry) -> Gtk.Box:
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        _set_widget_margins(main_container, 5, 5, 0, 5)
        main_container.add(search_input_field)
        return main_container

    def _build_options_box(self, current_search: str) -> Gtk.Box:
        options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        for option in self.mc.options:
            if current_search in option:
                button = Gtk.CheckButton(option)
                button.set_active(self.mc.is_selected(option))
                button.connect("toggled", self.on_button_toggled, option)
                options_box.add(button)
        return options_box

    def _update_options_box(self, current_search: str):
        if self.options_box is not None:
            self.scroll.remove(self.options_box)
            self.options_box.destroy()
        self.options_box = self._build_options_box(current_search)
        self.scroll.add(self.options_box)
        self.show_all()

    def _auto_complete(self, current_search: str):
        auto_completion = autocomplete.auto_complete(current_search, self.mc.options)
        self.search_input_field.set_text(auto_completion)
        Gtk.Entry.do_move_cursor(self.search_input_field, 1, len(auto_completion), False)

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
        current_search = self.search_input_field.get_text().lower()
        current_search_stripped = current_search.strip()
        control_pressed = (ev.state & Gdk.ModifierType.CONTROL_MASK == Gdk.ModifierType.CONTROL_MASK)
        if ev.keyval == Gdk.KEY_Return:
            self._handle_return_key(current_search_stripped, control_pressed)
        elif ev.keyval == Gdk.KEY_space and control_pressed:
            self._auto_complete(current_search)
        else:
            self._update_options_box(current_search)

    def _handle_return_key(self, current_search: str, control_pressed: bool):
        if control_pressed:
            self.response(Gtk.ResponseType.OK)
        if len(current_search) == 0:
            return
        if self.allow_custom_tags or self.mc.has_option(current_search):
            self.mc.toggle_option(current_search)
            self.search_input_field.set_text("")
            self._update_options_box("")


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
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        return mc.selection
    else:
        return []
