import unittest

from pyconose import CoverageFileReader, ParamConstants


class TestCoverageFileReader(unittest.TestCase):
    fixtureFile = "./test/fixtures/unit/coverage1.xml"

    def test_001_classCoverage(self) -> None:
        cov: dict = CoverageFileReader._getClassesCoverageMap(self.fixtureFile)
        self.assertEqual(len(cov.keys()), 3)
        self.assertTrue("main.py" in cov.keys())
        self.assertEqual(cov["main.py"], 0.0)
        self.assertTrue("pricer.py" in cov.keys())
        self.assertEqual(cov["pricer.py"], 0.8512)
        self.assertTrue("collections.py" in cov.keys())
        self.assertEqual(cov["collections.py"], 0.9474)

    def test_002_packageCoverage(self) -> None:
        cov: dict = CoverageFileReader._getPackagesCoverageMap(self.fixtureFile)
        self.assertEqual(len(cov.keys()), 3)
        self.assertTrue("azbaseliner" in cov.keys())
        self.assertEqual(cov["azbaseliner"], 1.0)
        self.assertTrue("azbaseliner.pricing" in cov.keys())
        self.assertEqual(cov["azbaseliner.pricing"], 0.8512)
        self.assertTrue("azbaseliner.util" in cov.keys())
        self.assertEqual(cov["azbaseliner.util"], 0.9474)

    def test_003_allCoverage(self) -> None:
        cov: dict = CoverageFileReader.getCoverageMap(self.fixtureFile)
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
