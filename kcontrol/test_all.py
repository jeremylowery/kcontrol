import os
import sys
import unittest

def main():
    loader = unittest.TestLoader()
    suites = []
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__),'kcontrol/Controls'))
    rep_dir = os.path.abspath(os.path.dirname(__file__))
    for d, n, f in os.walk(base_dir):
        for file in f:
            if file.endswith('.py') and file.startswith('test_'):
                print("Testing: %s" % file.replace('.py','').replace('test_',''))
                b = d.replace(rep_dir,'').replace('/','.')[1:]
                e = file.replace('.py','')
                path = "%s.%s" % (b, e)
                suite = loader.loadTestsFromName(path)
                runner = unittest.TextTestRunner()
                runner.run(suite)
                print('='*80)

    for d, n, f in os.walk(base_dir):
        for file in f:
            if file.endswith('.py') and file != '__init__.py' and \
                not file.startswith('test_'):
                if "test_%s" % file not in f:
                    print("Missing Test Case for %s" % file)

if __name__ == '__main__':
    main()
    print('DONE')
