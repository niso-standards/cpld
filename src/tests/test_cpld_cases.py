import pytest
import json
import os.path
import re
import warnings
from ..cpld.document import *

MANIFEST_FILE = "manifest.json"

DATA_DIR = os.path.join(os.path.relpath(os.path.dirname(__file__)),'data')

COMPARISON_TEST = "ComparisonTest"
NEGATIVE_TEST = "NegativeTest"
RETRIEVAL_TEST = "RetrievalTest"
TRIPLES_TEST = "TriplesTest"

def read_file(filename):
    with open(os.path.join(DATA_DIR, filename), 'r') as f:
        return f.read().strip()

def load_cases():
    with open(os.path.join(DATA_DIR, MANIFEST_FILE),"rb") as f:
        manifest = json.load(f)

    cases = []
    for test_case in manifest:
        test_case['base_dir'] = os.path.join(DATA_DIR, os.path.dirname(test_case['input_file']))
        for loadable in ['input_file', 'output_file', 'html_output_file', 'jsonld_output_file', 'nquads_output_file']:
            if loadable in test_case: 
                test_case[re.sub('_file$', '', loadable)] = read_file(test_case[loadable])

        cases.append(test_case)

    return cases


CASE_FILTERS = {
    COMPARISON_TEST: lambda case: 'input_file' in case and any([p in case for p in ['html_output', 'html_output_file', 'jsonld_output', 'jsonld_output_file']]),
    NEGATIVE_TEST:   lambda case: 'input_file' in case and 'raises' in case,
    RETRIEVAL_TEST:  lambda case: 'input_file' in case and any([p in case for p in ['output', 'output_file']]),
    TRIPLES_TEST:    lambda case: 'input_file' in case and 'subject' in case and 'predicate' in case and 'objects' in case,
}

def filter_cases(cases, test_type):
    return [case for case in cases if case['type'] == test_type and CASE_FILTERS[test_type](case)]

def pytest_generate_tests(metafunc):
    cases = load_cases()
    comparison_cases = filter_cases(cases, COMPARISON_TEST)
    negative_cases = filter_cases(cases, NEGATIVE_TEST)
    retrieval_cases = filter_cases(cases, RETRIEVAL_TEST)
    triples_cases = filter_cases(cases, TRIPLES_TEST)

    unsupported_cases = [case for case in cases if not case in comparison_cases + negative_cases + retrieval_cases + triples_cases]


    if len(unsupported_cases) > 0:
        warnings.warn(UserWarning(f"The manifest.json file contains unsupported test cases:\n {unsupported_cases}"))

    if "comparison_case" in metafunc.fixturenames:      
        metafunc.parametrize("comparison_case", comparison_cases, ids=[case['id'] for case in comparison_cases], indirect=True)

    if "negative_case" in metafunc.fixturenames:
        metafunc.parametrize("negative_case", negative_cases, ids=[case['id'] for case in negative_cases] ,indirect=True)

    if "retrieval_case" in metafunc.fixturenames:
        metafunc.parametrize("retrieval_case", retrieval_cases, ids=[case['id'] for case in retrieval_cases], indirect=True)

    if "triples_case" in metafunc.fixturenames:
        metafunc.parametrize("triples_case", triples_cases, ids=[case['id'] for case in triples_cases], indirect=True)


@pytest.fixture
def comparison_case(request):
    return request.param

@pytest.fixture
def negative_case(request):
    return request.param

@pytest.fixture
def retrieval_case(request):
    return request.param

@pytest.fixture
def triples_case(request):
    return request.param

def test_retrieval_tests(retrieval_case):
    """Parametrized with all retrieval cases with property and output"""
    
    document = Document.from_data(retrieval_case['input'], base_folder=retrieval_case['base_dir'])

    property_value = document.get(retrieval_case['property'])

    assert property_value == retrieval_case['output']

def test_comparison_tests(comparison_case):
    """Parametrized with all comparison cases with input/output"""
    document = Document.from_data(comparison_case['input'], base_folder=comparison_case['base_dir'])

    if 'html_output' in comparison_case:
        if 'html_id' in comparison_case:
            output = document.get_html_element_by_id(comparison_case['html_id'])
        else:
            output = document.get_raw_html()
        assert output == comparison_case['html_output']

    if 'jsonld_output' in comparison_case:
        output = document.get_jsonld()
        assert output == comparison_case['jsonld_output']

    if 'nquads_output' in comparison_case:
        output = document.get_nquads()
        assert output == comparison_case['nquads_output']


def test_negative_tests(negative_case):
    """Parametrized with all negative cases with input"""

    try:
        document = Document.from_data(negative_case['input'], base_folder=negative_case['base_dir'])
        success = False
    except Exception as e:
        if type(e).__name__ == negative_case['raises']:
            """The exception is of the predefined type, the test is successful"""

            success = True
        else:
            """The exception is of a different type, the test fails"""

            raise Exception(f"Found exception of type {type(e).__name__}") from e
            success = False

    assert success

def test_triples_tests(triples_case):
    document = Document.from_data(triples_case['input'], base_folder=triples_case['base_dir'])
    triples = sorted([str(t) for t in document.get_triple_objects(triples_case['subject'], triples_case['predicate'])])

    assert triples == sorted(triples_case['objects'])

