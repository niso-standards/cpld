# CP/LD Tutorial

## Introduction

This is a step-by step introduction to creating your first Linked Document that is conformant to the CP/LD standard.

It makes sense to use [VSCode](https://code.visualstudio.com) and the [CP/LD Viewer](https://marketplace.visualstudio.com/items?itemName=Elsevier.cpld-viewer) extension to test your code.

## Basics

The CP/LD standard describes a mechanism for combining HTML5 for content (i.e. scientific articles, books, anything) with Linked Data, that is very similar to Google Structure Data, and microformats such as RDFa. The main difference is that where Google Structured Data is meant to facilitate the situation where the HTML and Linked Data capture the *same* information, CP/LD is there to capture *metadata* about the HTML. 

CP/LD uses HTML (https://html.spec.whatwg.org) for content structure, and JSON-LD to represent Linked Data, if you're not familiar with JSON-LD it makes sense to peruse the introductory material at <https://json-ld.org>. The JSON-LD specification lives at <https://www.w3.org/TR/json-ld/>

To get going, we will need 1) an HTML file (`example1.html`) and 2) a JSON-LD file that captures the Linked Data (`example1.jsonld`).

### The HTML

Let's have a look at the basic HTML structure of `example1.html`. To turn this into a Linked Document, we need to add the following information to the HTML:

1. We first mint a document *identifier* for the linked document. Ideally this is a [dereferenceable IRI](https://www.w3.org/TR/cooluris/), and it should be an HTTPS IRI. Let's use the following IRI:
   ```
   https://cpld.example.com/document/3a2b3c
   ```
2. The document type tells any reader (e.g. a browser) that this is uses the latest version of HTML.
   ```html
   <!DOCTYPE html>
   ```
3. The `xml:base` attribute tells XML and HTML parsers that any local identifiers in the HTML (e.g. the value of an `id` attribute) can be turned into an absolute URI by prepending the value of the `xml:base` attribute. We use the identifier we minted earlier.
    ```html
    <html xmlns="http://www.w3.org/1999/xhtml" xml:base="https://cpld.example.com/document/3a2b3c">
    ```
    The `xmlns` definition is there to ensure that XML parsers use the correct namespace.
4. Inside the `<head>` of the HTML file, a `<meta>` element specifies the document identifier:
   ```html
   <meta name="id" content="https://cpld.example.com/document/3a2b3c" />
   ```
5. Inside the `<head>` of the HTML file, a `<link>` element defines the `dct` namespace schema as prefix for the `http://purl.org/dc/terms` namespace.
    ```html
    <link rel="schema.dct" href="http://purl.org/dc/terms/" />
    ```
6. This allows us to then use the `dct` prefix tor stating conformance using the `<meta>` element. We use the pattern described by the [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dc-html/) consortium (note the dot-notation, instead of a colon). **NB** We may also choose to adopt RDFa prefixes instead:
   ```html
   <meta name="dct.conformsTo" content="https://cpld.example.com/schema/cpld/" />
   ```
   Note that the value of the `content` attribute should point to the official CP/LD namespace. Additional conformance statements may be added, but this one is required.
7. Finally, we insert a `<link>` element that points to the JSON-LD file that contains the Linked Data that describes this document:
   ```html
   <link type="application/ld+json" rel="describedby" href="tutorial1.jsonld" />
   ```

The `<head>` may contain any other standard HTML elements, such as style information, scripts. It is recommended to not include the code inline, but point at external files using `<link>` and `<script>` elements.

In code:

```html
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:base="https://cpld.example.com/document/3a2b3c">
    <head>
        <meta name="id" content="https://cpld.example.com/document/3a2b3c" />
        <link rel="schema.dct" href="http://purl.org/dc/terms/" />
        <meta name="dct.conformsTo" content="https://cpld.example.com/schema/cpld/" />
        <link type="application/ld+json" rel="describedby" href="example1.jsonld" />
    </head>
    <body>
    </body>
</html>
```

### The JSON-LD

The basic structure of the JSON-LD file (`example1.jsonld`) needs the following information:

1. We link to the CP/LD context to make our JSON-LD easier to read. The context defines namespace prefixes, and helps the parser interpret the JSON as linked data. The context will be hosted at a predictable location, but for now we'll use the `cpld-niso-context.jsonld` in this repository:
   ```json
   "@context": "cpld-niso-context.jsonld",
   ```
2. The context also needs to map the document identifier to the reserved `doc` namespace:
   ```json
   "@context": [
    "cpld-niso-context.jsonld",
    { "doc": "https://cpld.example.com/document/1a2b3c#" }
   ],
   ```
3. With the context in place, we can start the actual linked data by specifying the main resource: the document:
    ```json
    "id": "https://cpld.example.com/document/1a2b3c",
    ```
4. We specify (again) that the document conforms to the CP/LD standard:
    ```json
    "conformsTo": "http://cpld.example.com/schema/cpld/",
    ```
5. And we specify the type of the document, in this case a [`schema:Article`](https://schema.org/Article):
   ```json
   "type": "schema:Article"
   ```


The complete example:

```json
{
    "@context": [
        "cpld-niso-context.jsonld", 
        { "doc": "https://cpld.example.com/document/1a2b3c#" } 
    ],
    "id": "https://cpld.example.com/document/1a2b3c",
    "conformsTo": "http://cpld.example.com/schema/cpld/",
    "type": "schema:Article"
}
```

