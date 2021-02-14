__all__ = ['Label']
from .Control import Control

class Label(Control):
    def draw(self):
        if not self.value:
            self.value = self.defaultValue
        caption = self.caption or self.value
        return "<label for='%s'>%s</label>" % (self.name, caption)
