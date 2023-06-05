class CPLDException(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidHTMLStructureException(CPLDException):
    """Invalid HTML structure used, as determined by external validator"""
    def __init__(self):
        super().__init__("Invalid HTML structure used, as determined by external validator")

class MissingHeadElementException(CPLDException):
    """HTML structure does not contain the obligatory <head> element"""
    def __init__(self):
        super().__init__("HTML structure does not contain the obligatory <head> element")

class MissingDCTSchemaDefinitionException(CPLDException):
    """HTML structure does not contain the obligatory <link> element that introduces the DCT namespace"""
    def __init__(self):
        super().__init__("HTML structure does not contain the obligatory <link> element that introduces the DCT namespace")

class MissingConformsToException(CPLDException):
    """HTML structure does not contain the obligatory <meta> element that states conformance to the CPLD schema"""
    def __init__(self):
        super().__init__("HTML structure does not contain the obligatory <meta> element that states conformance to the CPLD schema")

class InvalidDocumentIRIException(CPLDException):
    """Invalid IRI used as Document IRI"""
    def __init__(self, msg=None):
        if msg is None:
            msg = "Invalid IRI used as Document IRI"
        super().__init__(msg)

class InvalidHashDocumentIRIException(InvalidDocumentIRIException):
    """Invalid Hash IRI used as Document IRI"""
    def __init__(self):
        super().__init__("Invalid Hash IRI used as Document IRI")

class MissingDocumentIRIException(CPLDException):
    """Document does not specify a '<meta>' element with a value for the 'id' attribute"""
    def __init__(self):
        super().__init__("Document does not specify a '<meta>' element with a value for the 'id' attribute")

class MultipleDocumentIRIsException(CPLDException):
    """Document specifies more than one '<meta>' element with a value for the 'id' attribute"""
    def __init__(self):
        super().__init__("Document specifies more than one '<meta>' element with a value for the 'id' attribute")

class MissingHTMLBaseException(CPLDException):
    """Document does not specify a 'base' element in the html head"""
    def __init__(self):
        super().__init__("Document does not specify a 'base' element in the html head")

class HTMLBaseMismatchException(CPLDException):
    """Document base 'href' attribute does not match the document iri"""
    def __init__(self):
        super().__init__("Document base 'href' attribute does not match the document iri")

class NoJSONLDFoundException(CPLDException):
    """No JSON-LD was found while parsing the Linked Document"""
    def __init__(self):
        super().__init__("No JSON-LD was found while parsing the Linked Document")

class NoQuadsFoundException(CPLDException):
    """No RDF quads resulted from parsing the JSON-LD"""
    def __init__(self):
        super().__init__("No RDF quads resulted from parsing the JSON-LD")

class MissingDocumentTypeException(CPLDException):
    """No type specified for Document IRI"""
    def __init__(self):
        super().__init__("No type specified for Document IRI")

class InvalidEmbeddedJSONFoundException(CPLDException):
    """Could not parse script element content into a JSON object"""
    def __init__(self):
        super().__init__("Could not parse script element content into a JSON object")

class InvalidRemoteJSONFoundException(CPLDException):
    """Could not parse response content into a JSON object"""
    def __init__(self):
        super().__init__("Could not parse response contentinto a JSON object")

class CouldNotRetrieveReferencedJSONException(CPLDException):
    """Could not retrieve JSON data from referenced location"""
    def __init__(self):
        super().__init__("Could not retrieve JSON data from referenced location")


## Namespace & IRI validation in Dataset

class NoStatementsAboutDocumentIRIException(CPLDException):
    """The document IRI does not appear in any quads"""
    def __init__(self):
        super().__init__("The document IRI does not appear in any quads")

class NoCPLDNamespaceException(CPLDException):
    """The CPLD Namespace IRI is not defined"""
    def __init__(self):
        super().__init__("The CPLD Namespace IRI is not defined")