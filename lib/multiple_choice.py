from typing import List


class MultipleChoice:
    def __init__(self, options: List[str], multi_select: bool):
        self.options = options
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
        self._toggle(current_focused)

    def is_focused(self, option: str):
        return self.options[self.current_focus] == option

    def is_selected(self, option: str):
        return option in self.selection

    def _toggle(self, option: str):
        if self.is_selected(option):
            self._unselect(option)
        else:
            self._select(option)

    def _select(self, option: str):
        if not self.multi_select:
            self.clear_selection()
        self.selection.add(option)

    def _unselect(self, option: str):
        if self.multi_select:
            self.selection.remove(option)
