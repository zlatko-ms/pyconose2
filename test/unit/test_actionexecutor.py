import unittest
from pycovcheck import ActionExecutor, ParamConstants
import logging


class TestActionExecutor(unittest.TestCase):
    fixtureFile1 = "./test/fixtures/unit/coverage1.xml"
    fixtureFile2 = "./test/fixtures/unit/coverage2.xml"
    paramLinePrefix: str = f"format=nose2"
    paramPackagesNamedSuccess: str = "azbaseliner.pricing:0.8 azbaseliner.util:0.9"
    paramPackagesWildcarSuccess: str = "*:0.8"
    paramClassesNamedSucccess: str = "pricer.py:0.8 collections.py=0.9"
    paramClassesWildcarSuccess: str = "*:0.8"
    paramPackagesNamedFailure: str = "azbaseliner.pricing:0.9 azbaseliner.util:0.9"
    paramClassesNamedFailure: str = "pricer.py:0.99 collections.py=0.9"
    paramPackagesWildcarFailure: str = "*:0.99"

    def test_001_successfullNamedCheck(self) -> None:
        paramLine = f"{self.paramLinePrefix} {ParamConstants.COVERAGE_FILE}={self.fixtureFile1} {ParamConstants.PACKAGES}={self.paramPackagesNamedSuccess} {ParamConstants.CLASSES}={self.paramClassesNamedSucccess}"
        self.assertTrue(ActionExecutor.assertTresholds(paramLine))

    def test_002_successfullWildcarPackagesCheck(self) -> None:
        paramLine = f"{self.paramLinePrefix} {ParamConstants.COVERAGE_FILE}={self.fixtureFile1} {ParamConstants.PACKAGES}={self.paramPackagesWildcarSuccess} {ParamConstants.CLASSES}={self.paramClassesNamedSucccess}"
        self.assertTrue(ActionExecutor.assertTresholds(paramLine))

    def test_003_successfullWildcarClassesCheck(self) -> None:
        paramLine = f"{self.paramLinePrefix} {ParamConstants.COVERAGE_FILE}={self.fixtureFile2} {ParamConstants.PACKAGES}={self.paramPackagesNamedSuccess} {ParamConstants.CLASSES}={self.paramClassesWildcarSuccess}"
        self.assertTrue(ActionExecutor.assertTresholds(paramLine))

    def test_004_successfullWildcarCheck(self) -> None:
        paramLine = f"{self.paramLinePrefix} {ParamConstants.COVERAGE_FILE}={self.fixtureFile2} {ParamConstants.PACKAGES}={self.paramClassesWildcarSuccess} {ParamConstants.CLASSES}={self.paramClassesWildcarSuccess}"
        self.assertTrue(ActionExecutor.assertTresholds(paramLine))

    def test_005_failedNamedCheck(self) -> None:
        paramLine = f"{self.paramLinePrefix} {ParamConstants.COVERAGE_FILE}={self.fixtureFile1} {ParamConstants.PACKAGES}={self.paramPackagesNamedFailure} {ParamConstants.CLASSES}={self.paramClassesWildcarSuccess}"
        self.assertFalse(ActionExecutor.assertTresholds(paramLine))

    def test_006_failedWildcarCheck(self) -> None:
        paramLine = f"{self.paramLinePrefix} {ParamConstants.COVERAGE_FILE}={self.fixtureFile1} {ParamConstants.PACKAGES}={self.paramPackagesWildcarFailure} {ParamConstants.CLASSES}={self.paramClassesWildcarSuccess}"
        self.assertFalse(ActionExecutor.assertTresholds(paramLine))
