# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

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
