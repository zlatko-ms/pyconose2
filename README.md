# Pycovcheck

Asserts test coverage for python code.

This GitHub action reads a python coverage file in xml format and performs assertions on the coverage level of packages and classes.

You can specify global coverage rules ( i.e for all packages or classes ) or specific rules (for each package or class) and you can of course mix them in order to reflect your coverage strategy and targets to meet.

The coverage xml file can be produced by a number of test frameworks. This action was tested against the ones produced by pycoverage and nose2. Format being unique and shared among the frameworks, it is likely that any coverage.xml file can be processed and asserted.

## Usage

### Version

The current stable version is v2.

### Params

| Name      | Required | Description                                                                                     | Default Value             |
| --------- | -------- | ------------------------------------------------------------------------------------------------| ------------------------- |
| packages     | Yes      | list of <packageName>:<coverageTreshold> statements. The treshold is a percentage expressed as float. To apply a global treshold on all pacakges omit the package name and provide only :<coverageTreshold>                                 | empty list |
| classes  | Yes       | list of <className>:<coverageTreshold> statements.  The treshold is a percentage expressed as float. To apply a global treshold on all classis omit the package name and provide only :<coverageTreshold>   | empty list |
| coveragefile    | No       | Path to the coverage file to perform assertions against | ./coverage.xml |


### Examples

**Single class assertion** 

Use the following in order to assert a given class coverage : 

```yaml
      - name: Assert coverage of collections.py is above or equal to 93% 
        uses: zlatko-ms/pycovcheck@v2
        with: 
          coveragefile: ./test/fixtures/unit/nose2/coverage1.xml
          classes:  collections.py:0.93
```

**Multiple class assertion** 

Use the following in order to assert the coverage of a set of classes : 

```yaml
      - name: Assert coverage of collections.py is above or equal to 93% and coverage of finder.py is above or equal to 97%
        uses: zlatko-ms/pycovcheck@v2
        with: 
          coveragefile: ./test/fixtures/unit/nose2/coverage1.xml
          classes:  |
            azbaseliner.util.collections.py:0.93
            azbaseliner.pricing.finder.py:0.97
```

**Global class assertion** 

Use the following in order to assert the coverage level for all the classes, which is probably the most common use case : 

```yaml
      - name: Assert coverage of all classes is above or equal to 80% 
        uses: zlatko-ms/pycovcheck@v2
        with: 
          coveragefile: ./test/fixtures/unit/nose2/coverage2.xml
          classes: :0.8
```

**Assert coverage of a single package** 

Use the following in order to assert a given package coverage  : 

```yaml
      - name: Assert coverage of azbazeliner.pricer package is above 85%
        uses: zlatko-ms/pycovcheck@v2
        with: 
          coveragefile: ./test/fixtures/unit/nose2/coverage1.xml
          packages:  azbaseliner.pricing:0.85
```

**Assert coverage of multiple packages** 

Use the following in order to assert a the coverage of several packages   : 

```yaml
      - name: Assert coverage of azbazeliner.pricer package is above 07% and azbazliner.report is above 85%
        uses: zlatko-ms/pycovcheck@v2
        with: 
          coveragefile: ./test/fixtures/unit/nose2/coverage1.xml
          packages: |
            azbaseliner.pricing:0.97
            azbaseliner.report:0.85
```

**Global package assertion** 

Use the following to assert all packages coverage : 

```yaml
      - name: Assert coverage of all packages is above or equal to 80% 
        uses: zlatko-ms/pycovcheck@v2
        with: 
          coveragefile: ./test/fixtures/unit/nose2/coverage2.xml
          packages: :0.8
```

**Mixed class/package assertions** 

Use the following to assert both package and classes coverage : 


```yaml
      - name: Assert coverage of all packages is above or equal to 80% and make sure that the pricer class has at least 97% of coverage while reporter class has at least 85% coverage
        uses: zlatko-ms/pycovcheck@v2
        with: 
          coveragefile: ./test/fixtures/unit/nose2/coverage2.xml
          packages: :0.8
          classes: 
            azbaseliner.pricing.pricer.py:0.97
            azbaseliner.pricing.reporter.py:0.85
```
