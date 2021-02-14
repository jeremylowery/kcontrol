import unittest

from kcontrol import Control, ResWatcher
import kcontrol.config as cfg

class ControlTestCase(unittest.TestCase):
    def testControl(self):
        # Basic value test
        ctrl = Control()
        ctrl.value = "test"
        self.assertEqual(str(ctrl), "test")
    
    
    def testControlSignature(self):
        # Basic value test
        ctrl = Control('first_name', 'First Name')
        self.assertEqual(ctrl.name, 'first_name')
        self.assertEqual(ctrl.caption, 'First Name')

    def testResource(self):
        # Until threading is done...
        cfg.update({'kcontrol_url' : 'kcontrol/res/'})

        ctrl = Control()
        ctrl.pushResourceUp('css','date/res/css/date.css')
        ctrl.pushResourceUp('css','css/form.css')
        self.assertEqual(ResWatcher.css, ['kcontrol/res/date/res/css/date.css',
            'kcontrol/res/css/form.css'])
        self.assertEqual([],ResWatcher.js)


        ctrl = Control()
        ctrl.pushResourceUp('js','date/res/js/date.js')
        ctrl.pushResourceUp('js','js/form.js')
        self.assertEqual(ResWatcher.js, ['kcontrol/res/date/res/js/date.js',
            'kcontrol/res/js/form.js'])
        self.assertEqual(ResWatcher.css, ['kcontrol/res/date/res/css/date.css',
            'kcontrol/res/css/form.css'])

        print(ResWatcher.js)
        print(ResWatcher.css)
if __name__ == '__main__':
    unittest.main()
