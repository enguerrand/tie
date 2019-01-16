from typing import List


class MultipleChoice:
    def __init__(self, options: List[str], multi_select: bool):
        if len(options) == 0:
            raise ValueError("options list cannot be empty")
        self.options = sorted(options)
        self.multi_select = multi_select
        self.current_focus = 0
        self.selection = set()

    def clear_selection(self):
        self.selection.clear()

    def focus_next(self):
        self.current_focus = (self.current_focus + 1) % len(self.options)

    def focus_previous(self):
        self.current_focus -= 1
        if self.current_focus < 0:
            self.current_focus += len(self.options)

    def toggle_focused(self):
        current_focused = self.options[self.current_focus]
        self.toggle_option(current_focused)

    def is_focused(self, option: str):
        return self.options[self.current_focus] == option

    def is_selected(self, option: str):
        return option in self.selection

    def toggle_option(self, option: str):
        if self.is_selected(option):
            self.unselect(option)
        else:
            self.select(option)

    def select(self, option: str):
        if not self.multi_select:
            self.clear_selection()
        if not option in self.options:
            self._add_option(option)
        self.selection.add(option)

    def unselect(self, option: str):
        if self.multi_select:
            self.selection.remove(option)

    def _get_focused_option(self):
        return self.options[self.current_focus]

    def _set_focused_option(self, option: str):
        self.current_focus = self.options.index(option)

    def _add_option(self, option):
        currently_focused = self._get_focused_option()
        self.options.append(option)
        self.options.sort()
        self._set_focused_option(currently_focused)

    def has_option(self, option):
        return option in self.options

