_all__ = ['RepeatControl', 'RepeaterControl']

from kcontrol.Controls.Control import Control
from kcontrol.Controls.CompositeControl import CompositeControl

class RepeatControl(Control):
    """A control that is repeated numerous times in a repeater"""
    pass

class RepeaterControl(CompositeControl):
    """A control that repeats another control based off a data source

    The RepeaterControl determines which child controls it contains based off
    of the children attribute of its data source. Repeater Controls are suited
    for showing records from a data set. """

    repeatControl = RepeatControl
    
    def buildControls(self):
        """Construct the child controls from the data source's children"""
        CompositeControl.buildControls(self)
        try:
            children = self.ds.children
        except AttributeError:
            return
        #raise str(self.ds)
        for ctrl_ds in children:
            ctrl = self.makeRepeatControl()
            ctrl.ds = ctrl_ds
            self.addControl(ctrl)
            
    def makeRepeatControl(self):
        """Create an instance of the control that is repeated"""
        return self.repeatControl()

