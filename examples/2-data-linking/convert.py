import lxml.etree as ET

dom = ET.parse("Example Data Linking Article.xml")
xslt = ET.parse("jats-to-rdf.xslt")
transform = ET.XSLT(xslt)
newdom = transform(dom)

rdfxml = ET.tostring(newdom, pretty_print=True)

with open("out.rdf", "wb") as f:
    f.write(rdfxml)

from rdflib import Graph

g = Graph()
g.parse(rdfxml, format="xml")

g.serialize("out.jsonld", format="json-ld", auto_compact=True)