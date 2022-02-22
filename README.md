# Content Profile / Linked Document Tests

This repository contains a test suite for implementations of the Content Profile and Linked Document standard

## How to run

First, you'll have to use `poetry` to install required packages:

`poetry install`

Then you can change into the `src` directory and run `pytest`:

`poetry run pytest` (use `-v` or `-vv` to get more verbose output)

## Defining Tests

The tests are captured in the [manifest.json](src/tests/data/manifest.json) using the following structure:

| attribute | description |
| --- | --- |
| `id` | A readable identifier of a test, starting with an index, e.g. `1-html-docid` | 
| `type` | One of `RetrievalTest`, `ComparisonTest` or `NegativeTest` (described below) | 
| `description` | A description of what the test tests | 
| `input` | The filename for the data that is to be used as input for the test |
| `property` | An optional property whose value is to be retrieved (`RetrievalTest` only) |
| `output` | The expected output of the retrieval (`RetrievalTest` only) |
| `html_output` | Expected HTML output of a `ComparisonTest` |
| `jsonld_output` | Expected JSON-LD output of a `ComparisonTest` |
| `nquads_output` | Expected (sorted) NQuads output of a `ComparisonTest` |
| `raises` | The name of the expected exception raised in the `NegativeTest` |

For example, the following instructs a `RetrievalTest` to extract the value for the `docid` property from a CPLD Document instantiated from the `1-html-docid-input.html` file, and compare this value with the contents of the `1-html-docid-output.txt` file:

```json
{
    "id": "1-html-docid",
    "type": "RetrievalTest",
    "description": "Extract document ID from HTML file",
    "input": "1-html-docid-input.html",
    "property": "docid",
    "output": "1-html-docid-output.txt"
}
```

See [tests.md](tests.md) for generated documentation for this file.

The [test_cpld_cases.py](src/tests/test_cpld_cases.py) file is a `pytest` implementation of the test suite that uses the [manifest.json](src/tests/data/manifest.json) file to parametrize standard test types using the CP/LD library implemented in the [cpld](src/cpld) package. 

**NB** it is the intention to separate the tests from the Python implementation in the future.

## Types of Tests

* The `RetrievalTest` retrieves a property value from an instantiated CPLD Document object (from the `input` file) and compares it to the value stored in the file indicated by the `output` attribute. The Python library implements this using a standard *getter* method on the CPLD Document class.
* The `ComparisonTest` instantiates a CPLD Document from the `input` file, and compares the literal serialization of (part of) that document to the information stored in the `html_output`, `jsonld_output` or `nquads_output`. It can be used to test roundtripping, or check that all intended RDF triples are properly loaded from the JSON-LD.
* The `NegativeTest` attempts to instantiate a CPLD Document from the `input` file, and expects a specific exception to be raised by the implementation. The test fails if no exception is raised, or if an exception of a different type is raised. The exceptions are currently only documented in the [exceptions.py](src/cpld/exceptions.py) file.

## Test Documentation

The [tests.md](tests.md) file is periodically generated from the [manifest.json](src/tests/data/manifest.json) file to give a more readable overview of the test suite.