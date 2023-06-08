#!/usr/bin/python3

import sys
import re
import pandas as pd
import logging
from logging import Logger


class ParamConstants(object):
    CLASSES: str = "classes"
    PACKAGES: str = "packages"
    COVERAGE_FILE: str = "coveragefile"
    FORMAT: str = "format"


class ParamParser(object):
    CHECK_FOR_LISTS = [ParamConstants.PACKAGES, ParamConstants.CLASSES]

    """Parses the parameter with the specific/unorthodox ways of passing lists from the gh action call"""

    @classmethod
    def getParameters(cls, paramLine: str) -> dict:
        params: dict = dict()
        tokens = re.split(r"(\w+)=", paramLine)
        keyFound: bool = False
        key: str = None
        for t in tokens:
            if len(t) > 0:
                if not keyFound:
                    key = t
                    keyFound = True
                elif key is not None:
                    z = t.rstrip()
                    if " " in z:
                        params[key] = z.split()
                    else:
                        params[key] = z
                    keyFound = False
                    key = None

        for v in cls.CHECK_FOR_LISTS:
            if v in params.keys():
                if type(params[v]) == str:
                    newlist: list = list()
                    if len(params[v]) > 0:
                        newlist.append(params[v])
                    params[v] = newlist
            else:
                params[v] = list()
        return params

    @classmethod
    def _getThresholdMapFromParam(cls, paramlist: list) -> dict:
        ret: dict = dict()
        for p in paramlist:
            if ":" in p:
                tokens = p.split(":")
                name = tokens[0].rstrip().lstrip().strip()
                val = tokens[1].rstrip().lstrip().strip()
                ret[name] = float(val)
        return ret

    @classmethod
    def getTresholdsMap(cls, params: dict) -> dict:
        treshs: dict = dict()
        treshKeys = [ParamConstants.CLASSES, ParamConstants.PACKAGES]
        for k in treshKeys:
            treshs[k] = cls._getThresholdMapFromParam(params[k])
        return treshs


class CoverageFileReader(object):
    """Base class for parsing coverage file"""

    @classmethod
    def _getPackagesCoverageMap(cts, filePath: str) -> dict:
        """returns a dict with package name as key and coverage level as value"""
        pass

    @classmethod
    def _getClassesCoverageMap(cts, filePath: str) -> dict:
        """returns a dict with class name as key and coverage level as value"""
        pass

    @classmethod
    def getCoverageMap(cts, filePath: str) -> dict:
        ret: dict = dict()
        ret[ParamConstants.CLASSES] = cts._getClassesCoverageMap(filePath)
        ret[ParamConstants.PACKAGES] = cts._getPackagesCoverageMap(filePath)
        return ret


class Nose2XmlCoverageFileReader(CoverageFileReader):
    """Nose2 XML coverage file reader"""

    @classmethod
    def _getPackagesCoverageMap(cts, filePath: str) -> dict:
        ret: dict = dict()
        r = pd.read_xml(filePath, xpath="./packages/*")
        x = r[r["name"] != "."]
        y = x[~x["name"].str.startswith("test.")]
        for index, row in y.iterrows():
            ret[row["name"]] = row["line-rate"]
        return ret

    @classmethod
    def _getClassesCoverageMap(cts, filePath: str) -> dict:
        ret: dict = dict()
        r = pd.read_xml(filePath, xpath="./packages/*/classes/*")
        x = r[r["name"] != "__init__.py"]
        y = x[~x["name"].str.startswith("test_")]
        for index, row in y.iterrows():
            ret[row["name"]] = row["line-rate"]
        return ret


class ThresholdChecker(object):
    logger: Logger = logging.getLogger("ThresholdChecker")

    @classmethod
    def assertTresholdCategoryLevels(
        cts, expectedLevels: dict, foundLevels: dict
    ) -> bool:
        for expected in expectedLevels:
            if expected == "*":
                ## all items must be above tresholds !
                for found in foundLevels:
                    if foundLevels[found] < expectedLevels[expected]:
                        cts.logger.error(
                            f"{found} coverage is {foundLevels[found]}, below expected {expectedLevels[expected]}"
                        )
                        return False
            else:
                if expected not in foundLevels:
                    cts.logger.error(f"{expected} cannot be found in the coverage file")
                    return False
                else:
                    if foundLevels[expected] < expectedLevels[expected]:
                        cts.logger.error(
                            f"{expected} coverage is {foundLevels[expected]}, below expected {expectedLevels[expected]}"
                        )
                        return False
        return True

    @classmethod
    def assertThreshold(cts, expectedDef: dict, foundDef: dict) -> bool:
        asserted: bool = True
        # assert class level tresholds, if any defined
        if ParamConstants.CLASSES in expectedDef.keys():
            asserted = asserted and cts.assertTresholdCategoryLevels(
                expectedDef[ParamConstants.CLASSES], foundDef[ParamConstants.CLASSES]
            )
        # assert package level tresholds, if any defined
        if ParamConstants.PACKAGES in expectedDef.keys():
            asserted = asserted and cts.assertTresholdCategoryLevels(
                expectedDef[ParamConstants.PACKAGES], foundDef[ParamConstants.PACKAGES]
            )
        return asserted


class ActionExecutor(object):
    """Performs internal action orchestration"""

    parsers: dict = {"nose2": Nose2XmlCoverageFileReader}

    @classmethod
    def assertTresholds(cts, cmdLineParams: str) -> bool:
        """Asseses test coverage tresholds, returns true if all criterias satisfied, false otherwise"""
        params: dict = ParamParser.getParameters(cmdLineParams)
        parser: CoverageFileReader = cts.parsers[params[ParamConstants.FORMAT]]
        foundCoverage = parser.getCoverageMap(params[ParamConstants.COVERAGE_FILE])
        expectedCoverage = ParamParser.getTresholdsMap(params)
        return ThresholdChecker.assertThreshold(expectedCoverage, foundCoverage)


def main():
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.INFO
    )
    logger: Logger = logging.getLogger("main")

    if not ActionExecutor.assertTresholds(" ".join(sys.argv[1:])):
        logger.error("One of the checks failed")
        sys.exit(255)
    else:
        logger.info("All checks succesfull")


if __name__ == "__main__":
    main()
