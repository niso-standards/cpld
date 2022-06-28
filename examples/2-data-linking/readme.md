This folder contains two files a (much simplified) JATS 1.1 article and a HTML representation of the same article:

* Example Data Linking Article.xml 
* Example Data Linking Article.html

This article contains references to several external data repositories that we would like to express in a CP/LD version of the document. These include:

*	Links to Datasets hosted in Zenodo
*	Links to a Facility in the form of the NASA SDO observatory
*	Github Repositories. 

### Conversion to RDF

* Use the `jats-to-rdf.xslt` stylesheet from <https://github.com/PeerJ/jats-conversion> to convert the JATS XML to RDF/XML (this uses BIBO, DCTerms and Prism)
* NB: this does not convert the bibliographic references.
* Convert the RDF/XML to JSON-LD
* This is the basis for the `example2.jsonld` file.


### CPLD compliance

* A couple of cleanup steps in the JSON-LD:
  * Remove empty values for `@id` that are artefacts of the conversion.
  * Change the identifier for the work to the full HTTPS IRI DOI rather than a URN.
  * Add the `doc` namespace
* A couple of cleanup steps in the HTML:
  * Change doctype to just HTML
  * Add the `xml:base` attribute
  * Add the required meta-tags in the `<head>`
  * Remove the metadata-sections from the HTML (these are now in the JSON-LD)




### LICENSE information

The `jats-to-rdf.xslt` file was published under the following license:

  The MIT License (MIT)

  Copyright (c) 2016 PeerJ

  Permission is hereby granted, free of charge, to any person obtaining a copy of
  this software and associated documentation files (the "Software"), to deal in
  the Software without restriction, including without limitation the rights to
  use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
  the Software, and to permit persons to whom the Software is furnished to do so,
  subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.