from . import CONFIG, handler
from .exceptions import *
import requests
from json import JSONDecodeError
from requests_file import FileAdapter
import os
import os.path
import re
import json
from pyld import jsonld
from bs4 import BeautifulSoup
from rfc3987 import parse as rfc3987_parse
from warnings import warn
from .definitions import EXAMPLE_IRI_PATTTERN
from rdflib import ConjunctiveGraph, URIRef, Namespace, RDF
import logging


log = logging.getLogger(__name__)
if CONFIG.log.level == "DEBUG":
    log.setLevel(logging.DEBUG)

log.addHandler(handler)


if CONFIG.html.validator != "tidy":
    raise Exception(f"Do not know validator '{CONFIG.html.validator}'")




requests_session = requests.session()
requests_session.mount("file://", FileAdapter())


class Document(object):
    def __init__(self):
        raise Exception(
            "This class can only be instantiated by way of one of the class methods, `from_file`, `from_data`"
        )

    @classmethod
    def from_file(cls, filename):
        base_folder = os.path.dirname(os.path.relpath(filename))
        with open(filename, "rb") as f:
            data = f.read()

        document = cls.from_data(data, base_folder = base_folder)

        return document

    @classmethod
    def from_data(cls, data, base_folder=None):
        document = cls.__new__(cls)  # Does not call __init__
        super(
            Document, document
        ).__init__()  # Don't forget to call any polymorphic base class initializers

        if base_folder is None:
            document._base_folder = os.curdir
        else:
            document._base_folder = os.path.relpath(base_folder)

        document._dataset = ConjunctiveGraph()

        document._process_html(data)
        document._process_jsonld()

        return document

    def _validate_html(self, data):

        if CONFIG.html.validator == "tidy":
            from tidylib import tidy_document

            TIDY_OPTIONS = vars(CONFIG.html.tidy)

            _, errors = tidy_document(data, options=TIDY_OPTIONS)

            if len(errors) > 0:
                tidy_exception = Exception(errors)

                raise InvalidHTMLStructureException() from tidy_exception

        else:
            raise Exception(f"Cannot validate using `{CONFIG.html.validator}`")

    def _validate_html_structure(self):
        """
        This is meant to ensure that all necessary ingredients are there in the HTML 
        to make the document parseable as Linked Document
        """

        # Make sure that there is a head element
        if self._soup.html.head is None:
            raise MissingHeadElementException()

        # Make sure that DC Terms is registered as a schema, and that a conformsTo statement exists in the HTML
        schema_dct_link = self._soup.html.head.find("link", attrs={"rel": "schema.dcterms", "href": "http://purl.org/dc/terms/"})
        if schema_dct_link is None:
            raise MissingDCTSchemaDefinitionException()
        
        # Make sure that DC Terms is registered as a schema, and that a conformsTo statement exists in the HTML
        conforms_to_meta = self._soup.html.head.find("meta", attrs={"name": "dcterms.conformsTo", "content": "https://w3id.org/cpld/"})
        if conforms_to_meta is None:
            raise MissingConformsToException()
        
        # Make sure that there's a document iri specified on a meta tag in the head
        meta_ids = self._soup.html.head.findAll("meta", attrs={"name": "id"})
        if len(meta_ids) > 1:
            raise MultipleDocumentIRIsException()
        elif len(meta_ids) == 0:
            raise MissingDocumentIRIException()

        if "content" not in meta_ids[0].attrs or meta_ids[0].attrs["content"] == "" or meta_ids[0].attrs["content"] is None:
             raise MissingDocumentIRIException()

    def _process_html(self, data):
        self._raw_html = data
        self._validate_html(data)
        self._soup = BeautifulSoup(markup=data, features="lxml")
        self._validate_html_structure()

        self._document_iri = self._document_iri_from_html()

    def _process_jsonld(self):

        jsonld_data = self._extract_jsonld()
        if len(jsonld_data) == 0:
            raise NoJSONLDFoundException()

        self._load_jsonld(jsonld_data)
        self._validate_dataset()

    def _document_iri_from_html(self):
        try:
            meta_ids = self._soup.html.head.findAll("meta", attrs={"name": "id"})
            document_iri = meta_ids[0]["content"]
            if document_iri is None:
                raise MissingDocumentIRIException()
        except TypeError as e:
            raise MissingDocumentIRIException() from e

        try:
            # Make sure that document IRI is a valid absolute IRI
            rfc3987_parse(document_iri, rule="IRI")
        except Exception as e:
            raise InvalidDocumentIRIException() from e

        # Make sure that the document IRI does not end with a hash
        if document_iri.endswith("#"):
            raise InvalidHashDocumentIRIException()

        # Make sure that the html base is set.
        if self._soup.html.head.base is None or not "href" in self._soup.html.head.base.attrs:
            raise MissingHTMLBaseException()

        if self._soup.html.head.base.attrs["href"] != document_iri:
            raise HTMLBaseMismatchException()

        return document_iri

    def _load_referenced_jsonld(self, referenced_jsonld_file):
        try:
            # If it's a valid IRI, we'll use it as URL for retrieving the data.
            rfc3987_parse(referenced_jsonld_file)

            referenced_jsonld_url = referenced_jsonld_file
            if referenced_jsonld_file.startswith("http"):
                referenced_jsonld_url = referenced_jsonld_file
            elif referenced_jsonld_file.startswith("file"):
                referenced_jsonld_url = referenced_jsonld_file
            else:
                raise Exception("This is not a retrievable URI")
        except:
            # It is not a valid IRI, but most likely a relative reference to a local file.
            if os.path.isabs(referenced_jsonld_file):
                # Absolute path... turn into URL
                referenced_jsonld_url = f"file://{referenced_jsonld_file}"
            else:
                # Relative path... turn into URL (relative to the HTML file)

                if "_base_folder" in self.__dict__:
                    referenced_jsonld_url = f"file://{os.path.join(os.path.abspath(self._base_folder), referenced_jsonld_file)}"
                else:
                    # this document is created from data, using the current dir to create an absolute path
                    referenced_jsonld_url = f"file://{os.path.join(os.path.abspath(os.curdir), referenced_jsonld_file)}"
        
        response = requests_session.get(referenced_jsonld_url)

        try:
            if response.ok:
                return response.json()
            else:
                log.debug(response.content)
                raise CouldNotRetrieveReferencedJSONException()
        except JSONDecodeError as e:
            raise InvalidRemoteJSONFoundException() from e

    def _extract_jsonld(self):
        jsonld_data = []
        # Load embedded JSON-LD
        try:
            jsonld_data.extend([
                json.loads(jsonld_tag.string)
                for jsonld_tag in self._soup.html.head.find_all(
                    "script", attrs={"type": "application/ld+json"}
                )
            ])
        except json.JSONDecodeError as e:
            raise InvalidEmbeddedJSONFoundException() from e
        
        # Load referenced JSON-LD
        # TODO: Be more restrictive and only find the JSON-LD that has a proper rel="preload" attribute?
        for jsonld_tag in self._soup.find_all(
            "link", attrs={"type": "application/ld+json"}
        ):
            jsonld_data.append(self._load_referenced_jsonld(jsonld_tag["href"]))

        return jsonld_data


    def _load_jsonld(self, jsonld_data):
        for jsonld_element in jsonld_data:
            if isinstance(jsonld_element.get('@context'), list):
                context = {}
                for context_element in jsonld_element.get('@context'):
                    if isinstance(context_element, str):
                        context.update(self._load_referenced_jsonld(context_element).get('@context'))
                    elif isinstance(context_element, dict):
                        context.update(context_element)
                jsonld_element['@context'] = context

        try:
            nquads = jsonld.to_rdf(jsonld_data, {'format': 'application/n-quads'})
        except Exception as e:
            """The JSON content could not be interpreted as RDF"""
            raise NoQuadsFoundException() from e

        if len(nquads) == 0:
            """The JSON content was interpreted as RDF, but did not contain any triples/quads"""
            raise NoQuadsFoundException()

        self._dataset.parse(data=nquads, format="nquads")

        jsonld_processor = jsonld.JsonLdProcessor()
        ctx = jsonld_processor.process_context(jsonld_processor._get_initial_context({'processingMode': 'json-ld-1.1'}), jsonld_data, None)

        for mapping_key, mapping_value in ctx['mappings'].items():
            if mapping_value['_prefix'] is True:
                prefix = mapping_key # The namespace prefix
                ns = Namespace(mapping_value['@id']) # The URI for the namespace
                self._dataset.bind(prefix, ns) 


    
    def _validate_dataset(self):
        
        document_iriref = URIRef(self._document_iri)
        if document_iriref not in self._dataset.all_nodes():
            raise NoStatementsAboutDocumentIRIException()

        if len(list(self._dataset.objects(document_iriref, RDF.type))) == 0 :
            raise MissingDocumentTypeException()

        log.debug(list(self._dataset.namespace_manager.namespaces()))        




    def get(self, property):

        if property == "docid" or property == "document_iri":
            return self.get_document_iri()

        return None

    def get_document_iri(self):
        return self._document_iri

    def get_raw_html(self):
        return self._raw_html

    def get_html(self):
        return str(self._soup)

    def get_html_element_by_id(self, html_id):
        return str(self._soup.find_all(attrs={"id": html_id})[0])

    def get_pretty_html(self):
        return self._soup.prettify()

    def get_jsonld(self):
        pass

    def get_nquads(self):
        pass

    def get_triple_objects(self, subject, predicate):
        return self._dataset.objects(subject=URIRef(subject), predicate=URIRef(predicate))
