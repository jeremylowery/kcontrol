__all__ = ['Info']
from .Control import Control

class Info(Control):
    def draw(self):
        if self.value:
            return "%s" % self.value
        else:
            return ""
