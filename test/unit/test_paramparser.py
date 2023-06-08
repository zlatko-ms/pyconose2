import unittest

from pyconose import ParamConstants, ParamParser


class TestParamParser(unittest.TestCase):
    paramLineFull: str = "format=nose2 coveragefile=myfile packages=mypack.mysubpack:0.72 mypack.myotherpack:0.84 classes=mypack.mysubpack.myclass:0.86 mypack.myotherpack.myclass:0.91"
    paramLineNoTresholds: str = "coveragefile=myfile packages= classes="
    paramLinePackages: str = "packages=mypack.mysubpack:0.72 mypack.myotherpack:0.84"
    paramLineClasses: str = (
        "classes=mypack.mysubpack.myclass:0.86 mypack.myotherpack.myclass:0.91"
    )

    def test_001_coverageFileParamOnly(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineNoTresholds)
        self.assertEquals("myfile", params[ParamConstants.COVERAGE_FILE])
        self.assertEquals(type(params[ParamConstants.PACKAGES]), list)
        self.assertEquals(type(params[ParamConstants.CLASSES]), list)
        self.assertEquals(len(params[ParamConstants.CLASSES]), 0)
        self.assertEquals(len(params[ParamConstants.PACKAGES]), 0)

    def test_002_coveragePackageTresholdsOnly(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLinePackages)
        self.assertEquals(type(params[ParamConstants.PACKAGES]), list)
        self.assertEquals(type(params[ParamConstants.CLASSES]), list)
        self.assertEquals(len(params[ParamConstants.CLASSES]), 0)
        self.assertEquals(len(params[ParamConstants.PACKAGES]), 2)
        self.assertTrue("mypack.mysubpack:0.72" in params[ParamConstants.PACKAGES])
        self.assertTrue("mypack.myotherpack:0.84" in params[ParamConstants.PACKAGES])

    def test_003_coverageClassesTresholdsOnly(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineClasses)
        self.assertEquals(type(params[ParamConstants.PACKAGES]), list)
        self.assertEquals(type(params[ParamConstants.CLASSES]), list)
        self.assertEquals(len(params[ParamConstants.CLASSES]), 2)
        self.assertTrue(
            "mypack.mysubpack.myclass:0.86" in params[ParamConstants.CLASSES]
        )
        self.assertTrue(
            "mypack.myotherpack.myclass:0.91" in params[ParamConstants.CLASSES]
        )
        self.assertEquals(len(params[ParamConstants.PACKAGES]), 0)

    def test_004_fullParamLine(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineFull)
        self.assertEquals("myfile", params[ParamConstants.COVERAGE_FILE])
        self.assertEquals("nose2", params[ParamConstants.FORMAT])
        self.assertEquals(type(params[ParamConstants.CLASSES]), list)
        self.assertEquals(len(params[ParamConstants.CLASSES]), 2)
        self.assertTrue(
            "mypack.mysubpack.myclass:0.86" in params[ParamConstants.CLASSES]
        )
        self.assertTrue(
            "mypack.myotherpack.myclass:0.91" in params[ParamConstants.CLASSES]
        )
        self.assertEquals(type(params[ParamConstants.PACKAGES]), list)
        self.assertEquals(len(params[ParamConstants.PACKAGES]), 2)
        self.assertTrue("mypack.mysubpack:0.72" in params[ParamConstants.PACKAGES])
        self.assertTrue("mypack.myotherpack:0.84" in params[ParamConstants.PACKAGES])

    def test_005_tresholdElementsParse(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineFull)
        treshClasses: dict = ParamParser._getThresholdMapFromParam(
            params[ParamConstants.CLASSES]
        )
        self.assertEqual(treshClasses["mypack.mysubpack.myclass"], 0.86)
        self.assertEqual(treshClasses["mypack.myotherpack.myclass"], 0.91)
        treshPacks: dict = ParamParser._getThresholdMapFromParam(
            params[ParamConstants.PACKAGES]
        )
        self.assertEqual(treshPacks["mypack.mysubpack"], 0.72)
        self.assertEqual(treshPacks["mypack.myotherpack"], 0.84)

    def test_006_thresholdMap(self) -> None:
        params: dict = ParamParser.getParameters(self.paramLineFull)
        tresholds: dict = ParamParser.getTresholdsMap(params)
        self.assertTrue(ParamConstants.CLASSES in tresholds.keys())
        self.assertEqual(
            tresholds[ParamConstants.CLASSES]["mypack.mysubpack.myclass"], 0.86
        )
        self.assertEqual(
            tresholds[ParamConstants.CLASSES]["mypack.myotherpack.myclass"], 0.91
        )
        self.assertTrue(ParamConstants.PACKAGES in tresholds.keys())
        self.assertEqual(tresholds[ParamConstants.PACKAGES]["mypack.mysubpack"], 0.72)
        self.assertEqual(tresholds[ParamConstants.PACKAGES]["mypack.myotherpack"], 0.84)
