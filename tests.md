
# Content Profile / Linked Document Tests

## 1-html-docid
### RetrievalTest

*Extract document ID from HTML file*

    

 input: [1-html-docid-input.html](src/tests/data/1-html-docid-input.html)

 output: [1-html-docid-output.txt](src/tests/data/1-html-docid-output.txt)
## 2-html-valid
### ComparisonTest

*Process valid HTML document, and know it's valid*

    

 input: [2-html-valid-input.html](src/tests/data/2-html-valid-input.html)

 html_output: [2-html-valid-output.html](src/tests/data/2-html-valid-output.html)
## 3-html-invalid
### NegativeTest

*Process invalid HTML document, and fail to initialize a document object*

    

raises: `InvalidHTMLStructureException`

 input: [3-html-invalid-input.html](src/tests/data/3-html-invalid-input.html)
## 3b-html-missing-head
### NegativeTest

*Process HTML document that does not contain a head, and fail to initialize a document object*

    

raises: `MissingHeadElementException`

 input: [3b-html-missing-head-input.html](src/tests/data/3b-html-missing-head-input.html)
## 3c-html-missing-dct
### NegativeTest

*Process HTML document that does not contain a link element to DCT, and fail to initialize a document object*

    

raises: `MissingDCTSchemaDefinitionException`

 input: [3c-html-missing-dct-input.html](src/tests/data/3c-html-missing-dct-input.html)
## 3d-html-missing-conformsTo
### NegativeTest

*Process HTML document that does not contain dcterms:conformsTo to the CPLD schema, and fail to initialize a document object*

    

raises: `MissingConformsToException`

 input: [3d-html-missing-conformsTo-input.html](src/tests/data/3d-html-missing-conformsTo-input.html)
## 4a-html-missing-document-id
### NegativeTest

*Process HTML document with missing document id, and fail to initialize a document object*

    

raises: `MissingDocumentIRIException`

 input: [4-html-missing-document-id-input.html](src/tests/data/4-html-missing-document-id-input.html)
## 4b-html-multiple-document-ids
### NegativeTest

*Process HTML document with more than one document id, and fail to initialize a document object*

    

raises: `MultipleDocumentIRIsException`

 input: [4b-html-multiple-document-ids-input.html](src/tests/data/4b-html-multiple-document-ids-input.html)
## 4c-html-invalid-document-id
### NegativeTest

*Process HTML document with invalid document id (no IRI), and fail to initialize a document object*

    

raises: `InvalidDocumentIRIException`

 input: [4c-html-invalid-document-id-input.html](src/tests/data/4c-html-invalid-document-id-input.html)
## 4e-html-invalid-hash-document-id
### NegativeTest

*Process HTML document with document id that ends with a hash character (#) and fail to initialize a document object*

    

raises: `InvalidHashDocumentIRIException`

 input: [4e-html-invalid-hash-document-id-input.html](src/tests/data/4e-html-invalid-hash-document-id-input.html)
## 5a-html-missing-xml-base
### NegativeTest

*Process HTML document with missing xml:base on html root, and fail to initialize a document object*

    

raises: `MissingXMLBaseException`

 input: [5a-html-missing-xml-base-input.html](src/tests/data/5a-html-missing-xml-base-input.html)
## 5b-html-xml-base-mismatch
### NegativeTest

*Process HTML document with xml:base that does not match the document iri, and fail to initialize a document object*

    

raises: `XMLBaseMismatchException`

 input: [5b-html-xml-base-mismatch-input.html](src/tests/data/5b-html-xml-base-mismatch-input.html)
## 6a-jsonld-no-jsonld-found
### NegativeTest

*Process HTML document without any embedded or linked JSON-LD, and fail to initialize a document object*

    

raises: `NoJSONLDFoundException`

 input: [6a-jsonld-no-jsonld-found-input.html](src/tests/data/6a-jsonld-no-jsonld-found-input.html)
## 6b-jsonld-no-quads-found
### NegativeTest

*Process HTML document where embedded JSON-LD does not contain any RDF, and fail to initialize a document object*

    

raises: `NoQuadsFoundException`

 input: [6b-jsonld-no-quads-found-input.html](src/tests/data/6b-jsonld-no-quads-found-input.html)
## 6c-jsonld-no-statements-about-document-id-found
### NegativeTest

*Process HTML document where embedded JSON-LD does not contain any statements about the Document IRI, and fail to initialize a document object*

    

raises: `NoStatementsAboutDocumentIRIException`

 input: [6c-jsonld-no-statements-about-document-id-found-input.html](src/tests/data/6c-jsonld-no-statements-about-document-id-found-input.html)
## 6d-jsonld-invalid-embedded-json-input
### NegativeTest

*Process HTML document where embedded JSON-LD is not valid JSON and fail*

    

raises: `InvalidEmbeddedJSONFoundException`

 input: [6d-jsonld-invalid-embedded-json-input.html](src/tests/data/6d-jsonld-invalid-embedded-json-input.html)
## 6e-jsonld-invalid-linked-local-json-input
### NegativeTest

*Process HTML document where linked local JSON-LD is not valid JSON and fail*

    

raises: `InvalidRemoteJSONFoundException`

 input: [6e-jsonld-invalid-linked-local-json-input.html](src/tests/data/6e-jsonld-invalid-linked-local-json-input.html)