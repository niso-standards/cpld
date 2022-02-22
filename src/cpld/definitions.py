from rdflib import Namespace
import os

EXAMPLE_IRI_PATTTERN = "https?://example.(com|org)/"

CPLD_SCHEMA_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../schema/cpld.schema.jsonld")

CPLD = Namespace("https://cpld.example.com/schema/cpld/")
SCHEMA = Namespace("https://schema.org/")

SH = Namespace("http://www.w3.org/ns/shacl#")
DCT = Namespace("http://purl.org/dc/terms/")