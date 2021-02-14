import unittest

from .FilePicker import FilePicker

class FilePickerTestCase(unittest.TestCase):
    def testFilePicker(self):
        # Basic value test
        ctrl = FilePicker('favorite_image')
        self.assertEqual(str(ctrl), 
            "<input type='file' value='' id='favorite_image' name='favorite_image'  />")


if __name__ == '__main__':
    unittest.main()
