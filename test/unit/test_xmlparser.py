import unittest

from pycovcheck import CoverageXMLFileReader, ParamConstants


class TestCoverageFileReader(unittest.TestCase):
    fixtureFile = "./test/fixtures/unit/nose2/coverage1.xml"

    def test_001_coverageMap(self) -> None:
        cov: dict = CoverageXMLFileReader.getCoverageMap(self.fixtureFile)
        self.assertTrue(ParamConstants.PACKAGES in cov.keys())
        self.assertTrue("azbaseliner" in cov[ParamConstants.PACKAGES].keys())
        self.assertEqual(cov[ParamConstants.PACKAGES]["azbaseliner"], 1.0)
        self.assertTrue("azbaseliner.pricing" in cov[ParamConstants.PACKAGES].keys())
        self.assertEqual(cov[ParamConstants.PACKAGES]["azbaseliner.pricing"], 0.8512)
        self.assertTrue("azbaseliner.util" in cov[ParamConstants.PACKAGES].keys())
        self.assertEqual(cov[ParamConstants.PACKAGES]["azbaseliner.util"], 0.9474)

        self.assertTrue(ParamConstants.CLASSES in cov.keys())
        self.assertTrue("main.py" in cov[ParamConstants.CLASSES].keys())
        self.assertEqual(cov[ParamConstants.CLASSES]["main.py"], 0.0)
        self.assertTrue("pricer.py" in cov[ParamConstants.CLASSES].keys())
        self.assertEqual(cov[ParamConstants.CLASSES]["pricer.py"], 0.8512)
        self.assertTrue("collections.py" in cov[ParamConstants.CLASSES].keys())
        self.assertEqual(cov[ParamConstants.CLASSES]["collections.py"], 0.9474)
