#!/usr/bin/python3

import sys
import re
import pandas as pd

# from itertools import chain, starmap
# import json
# import yaml


class ParamConstants(object):
    CLASSES: str = "classes"
    PACKAGES: str = "packages"
    COVERAGE_FILE: str = "coveragefile"


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
        r = pd.read_xml(
            "./test/fixtures/unit/coverage1.xml", xpath="./packages/*/classes/*"
        )
        x = r[r["name"] != "__init__.py"]
        y = x[~x["name"].str.startswith("test_")]
        for index, row in y.iterrows():
            ret[row["name"]] = row["line-rate"]
        return ret

    @classmethod
    def getCoverageMap(cts, filePath: str) -> dict:
        ret: dict = dict()
        ret[ParamConstants.CLASSES] = cts._getClassesCoverageMap(filePath)
        ret[ParamConstants.PACKAGES] = cts._getPackagesCoverageMap(filePath)
        return ret


class TresholdAssesor(object):
    @classmethod
    def assess(cts, expected: dict, found: dict) -> bool:
        # classes
        ret: bool = True
        for k, v in expected[ParamConstants.CLASSES].items():
            if k not in found[ParamConstants.CLASSES].keys():
                print(f"ERROR : unable to find coverage for class {k}")
                ret = False
            else:
                f = found[ParamConstants.CLASSES][k]
                if f < v:
                    print(f"ERROR : unable to find coverage for class {k}")
                    ret = False
        return ret


def main():
    params: dict = ParamParser.getParameters(" ".join(sys.argv[1:]))
    print(f"main params = {params}")
    # covFile = params[ParamConstants.COVERAGE_FILE]
    # expectedCoverage = ParamParser.getTresholdsMap(params)
    # foundCoverage = CoverageFileReader.getCoverageMap(covFile)


if __name__ == "__main__":
    main()
