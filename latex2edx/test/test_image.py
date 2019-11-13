import os
import unittest
try:
    from path import path	# needs path.py
except Exception as err:
    from path import Path as path
try:
    from StringIO import StringIO
except:
    from io import StringIO

import latex2edx as l2emod
from latex2edx.main import latex2edx
from latex2edx.test.util import make_temp_directory


class TestImage(unittest.TestCase):

    def test_image1(self):
        # make sure includegraphics works
        testdir = path(l2emod.__file__).parent / 'testtex'
        fn = testdir / 'example-html-text.tex'
        print("file %s" % fn)
        with make_temp_directory() as tmdir:
            nfn = '%s/%s' % (tmdir, fn.basename())
            os.system('cp %s/* %s' % (testdir, tmdir))
            os.chdir(tmdir)
            l2e = latex2edx(nfn, output_dir=tmdir)
            l2e.convert()
            xbfn = nfn[:-4] + '.xbundle'
            self.assertTrue(os.path.exists(xbfn))
            xb = open(xbfn).read()
            self.assertIn('<img src="/static/images/example-image.png" width="660"/>', xb)
            self.assertTrue(os.path.exists(path(tmdir) / 'static/images/example-image.png'))
            cfn = path(tmdir) / 'course/2015_Spring.xml'
            self.assertTrue(os.path.exists(cfn))
            self.assertIn('<course number="8.01x" display_name="Mechanics" start="2015-04-21" org="MITx" semester="2015_Spring">', open(cfn).read())

if __name__ == '__main__':
    unittest.main()
