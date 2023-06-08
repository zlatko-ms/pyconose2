import unittest

from pyconose import ThresholdChecker


class TestTresholdChecker(unittest.TestCase):
    def test_001_testValueAsserterNamedSuccess(self) -> None:
        expected: dict = {"package.name.a": 0.8, "package.name.b": 0.7}
        found: dict = {"package.name.a": 0.81, "package.name.b": 0.72}
        self.assertTrue(ThresholdChecker.assertTresholdCategoryLevels(expected, found))

    def test_002_testValueAsserterNamedFail(self) -> None:
        expected: dict = {"package.name.a": 0.8, "package.name.b": 0.7}
        found: dict = {"package.name.a": 0.71, "package.name.b": 0.72}
        self.assertFalse(ThresholdChecker.assertTresholdCategoryLevels(expected, found))

    def test_003_testValueAsserterWildcardSuccess(self) -> None:
        expected: dict = {"*": 0.8}
        found: dict = {"package.name.a": 0.81, "package.name.b": 0.82}
        self.assertTrue(ThresholdChecker.assertTresholdCategoryLevels(expected, found))

    def test_004_testValueAsserterWildcardFail(self) -> None:
        expected: dict = {"*": 0.8}
        found: dict = {"package.name.a": 0.71, "package.name.b": 0.82}
        self.assertFalse(ThresholdChecker.assertTresholdCategoryLevels(expected, found))

    def test_005_testValueAsserterNotFoundFail(self) -> None:
        expected: dict = {"package.name.x": 0.8, "package.name.y": 0.8}
        found: dict = {"package.name.a": 0.71, "package.name.b": 0.82}
        self.assertFalse(ThresholdChecker.assertTresholdCategoryLevels(expected, found))

    def test_006_testGlobalDefAssertSuccess(self) -> None:
        expected: dict = {
            "packages": {"package.name.a": 0.7, "package.name.b": 0.71},
            "classes": {"class.name.a": 0.5, "class.name.b": 0.6},
        }
        found: dict = {
            "packages": {"package.name.a": 0.71, "package.name.b": 0.72},
            "classes": {"class.name.a": 0.51, "class.name.b": 0.61},
        }
        self.assertTrue(ThresholdChecker.assertThreshold(expected, found))

    def test_007_testGlobalDefAssertSuccessWildecar(self) -> None:
        expected: dict = {
            "packages": {"*": 0.7},
            "classes": {"*": 0.5},
        }
        found: dict = {
            "packages": {"package.name.a": 0.71, "package.name.b": 0.72},
            "classes": {"class.name.a": 0.51, "class.name.b": 0.61},
        }
        self.assertTrue(ThresholdChecker.assertThreshold(expected, found))

    def test_008_testGlobalDefAssertFailPartialBelow(self) -> None:
        expected: dict = {
            "packages": {"package.name.a": 0.7, "package.name.b": 0.71},
            "classes": {"class.name.a": 0.5, "class.name.b": 0.6},
        }
        found: dict = {
            "packages": {"package.name.a": 0.71, "package.name.b": 0.42},
            "classes": {"class.name.a": 0.51, "class.name.b": 0.61},
        }
        self.assertFalse(ThresholdChecker.assertThreshold(expected, found))

    def test_009_testGlobalDefAssertFailNotFound(self) -> None:
        expected: dict = {
            "packages": {"package.name.a": 0.7, "package.name.b": 0.71},
            "classes": {"class.name.a": 0.5, "class.name.b": 0.6},
        }
        found: dict = {
            "packages": {"package.name.a": 0.71, "package.name.b": 0.42},
            "classes": {"class.name.a": 0.51},
        }
        self.assertFalse(ThresholdChecker.assertThreshold(expected, found))

    def test_010_testGlobalDefAssertFailWildecar(self) -> None:
        expected: dict = {
            "packages": {"*": 0.7},
            "classes": {"*": 0.5},
        }
        found: dict = {
            "packages": {"package.name.a": 0.71, "package.name.b": 0.72},
            "classes": {"class.name.a": 0.51, "class.name.b": 0.41},
        }
        self.assertFalse(ThresholdChecker.assertThreshold(expected, found))
