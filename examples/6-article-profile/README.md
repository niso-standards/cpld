# Linked Article Profile

- [1. Abstract](#1-abstract)
- [2. Introduction](#2-introduction)
  - [2.1. Scope](#21-scope)
  - [2.2. Profile format](#22-profile-format)
  - [2.3. Relationship to other Standards](#23-relationship-to-other-standards)
- [3. Conformance](#3-conformance)
- [4. Manifest](#4-manifest)
  - [4.1. Introduction](#41-introduction)
  - [4.2. Requirements](#42-requirements)
  - [4.3. Manifest Contexts](#43-manifest-contexts)
  - [4.4. Identifier](#44-identifier)
  - [4.5. Scholarly Article Conformance](#45-scholarly-article-conformance)
  - [4.6. Publication Type](#46-publication-type)
  - [4.7. Reading order and Resources](#47-reading-order-and-resources)
  - [4.8. Properties](#48-properties)
- [5. Data](#5-data)
  - [5.1. Introduction](#51-introduction)
  - [5.2. Narrative Requirements](#52-narrative-requirements)
  - [5.3. Property and Ontological Requirements](#53-property-and-ontological-requirements)
  - [5.4. Data Contexts](#54-data-contexts)
  - [5.5. Identifier](#55-identifier)
  - [5.6. Scholarly Article Conformance](#56-scholarly-article-conformance)
  - [5.7. Publication Type](#57-publication-type)
  - [5.8. Parts](#58-parts)
  - [5.9. Authors](#59-authors)
  - [5.10. Citations](#510-citations)
- [6. Content](#6-content)
  - [6.1. Introduction](#61-introduction)
  - [6.2. Requirements](#62-requirements)
  - [6.3. The Header](#63-the-header)
  - [6.4. Sections](#64-sections)
  - [6.5. References and Citations](#65-references-and-citations)

<!-- omit from toc -->
## 1. Abstract
This is a Content Profile definition for Scholarly Articles. It extends the CP/LD standard with a set of REQUIRED and RECOMMENDED elements to create a shareable representation of Scholarly Articles. It is also a [publication manifest](https://www.w3.org/TR/pub-manifest/) profile.

It uses [schema.org](https://schema.org) metadata, and augments it with properties central to scientific publications, such as bibliographic references. 

## 2. Introduction

### 2.1. Scope
This specification defines a general format to describe and represent Scholarly Articles. It is designed to be adaptable to the needs of specific publishers.

### 2.2. Profile format

A Linked Article is represented in three parts:

* A *manifest* description in JSON-LD, following the [publication manifest](https://www.w3.org/TR/pub-manifest/) reccomendation.
* At least one *data* file in [JSON-LD](https://www.w3.org/TR/json-ld11/), optionally embedded in HTML (below), that captures the (meta) data of the article.
* At least one *content* file in [HTML](https://html.spec.whatwg.org), and optionally multiple ancillary files, that capture(s) the content of the article. 

The properties in the manifest, content and data files describe the basic information a user agent requires to process and render the article.

The manifest and content files also identify key entities in a Scholarly Article. The entity types are categorized as follows:

* **Ontological entity types** represent real world entities, such as the article itself, persons, organisations etc. These are mostly captured using the [schema.org](https://schema.org) vocabulary.
* **Narrative entity types** represent the narrative role of parts of the text, such as the abstract, title, a reference, citation, etc. These are captured in a separate Narrative Structure Vocabulary specified by this profile.

### 2.3. Relationship to other Standards
This profile incorporates existing standards as much as possible, such as the aforementioned [schema.org](https://schema.org) and [publication manifest](https://www.w3.org/TR/pub-manifest/), but also [....]

## 3. Conformance
As well as sections marked as non-normative, all authoring guidelines, diagrams, examples, and notes in this specification are non-normative. Everything else in this specification is normative.

The key words MAY, MUST, MUST NOT, RECOMMENDED, REQUIRED, and SHOULD in this document are to be interpreted as described in [BCP 14](https://tools.ietf.org/html/bcp14)[RFC2119](https://tools.ietf.org/html/rfc2119)[RFC8174](https://tools.ietf.org/html/rfc8174) when, and only when, they appear in all capitals, as shown here.

## 4. Manifest

### 4.1. Introduction
The Scholarly Article manifest is defined by a set of properties that describe the basic information a user agent requires to process an Article. These properties are categorized in the [Publication Manifest](https://www.w3.org/TR/pub-manifest/). Where these properties are extende from the Publication Manifest is specified in this section.

### 4.2. Requirements
The requirements for the expression of Scholarly Article properties and resource relations are defined as follows:

#### 4.2.1. REQUIRED <!-- omit from toc -->
* `conformsTo`
* `@context`
* `id` (Document IRI)
* `type`
* `readingOrder`
* `resources`

#### 4.2.2. RECOMMENDED <!-- omit from toc -->
* `abstract`
* `author`
* `copyrightHolder`
* `copyrightNotice`
* `copyrightYear`
* `dateCreated`
* `dateModified`
* `inLanguage`
* `license`
* `publisher`
* `title`

### 4.3. Manifest Contexts
A Scholarly Article manifest and has to start by setting the JSON-LD context. The context has the following two major components:

* the schema.org context: `https://schema.org`
* the publication context `https://www.w3.org/ns/pub-context`

It is optional to include the global language for literals, or any other context information as long as it does not override the two major components.

###### 4.3.0.0.1. EXAMPLE<!-- omit from toc -->
```
{
  "@context": [
      "https://schema.org",
      "https://www.w3.org/ns/pub-context",
      {"language" : "en"}
  ]
  ...
}
```

### 4.4. Identifier

The identifier value for the `id` property MUST be the Document IRI as specified by the CP/LD standard.

### 4.5. Scholarly Article Conformance

The conformance URL expressed in the `conformsTo` term MUST be "`https://niso.org/cpld/article/`"

###### 4.5.0.0.1. EXAMPLE<!-- omit from toc -->
```
{
  "@context": [ "https://schema.org", "https://www.w3.org/ns/pub-context"],
  "conformsTo": "https://niso.org/cpld/article/"
}
```

### 4.6. Publication Type

The *publication type* is defined using the `type` term. The value for the `type` property MUST be "[`ScholarlyArticle`](https://schema.org/ScholarlyArticle)":

###### 4.6.0.0.1. EXAMPLE
```
{
  "@context": [ "https://schema.org", "https://www.w3.org/ns/pub-context"],
  "type": "ScholarlyArticle"
  ...
}
```

### 4.7. Reading order and Resources

The `readingOrder` and `resources` arrays MUST point at at least one HTML resource that represents the *content* of the Scholarly Article.

For the *data* part of the Scholarly Article, there are thee options:

1. The `resources` array points at at least one JSON-LD resource that represents the *data* part of the Scholarly Article.
2. At least one of the HTML resources that represent the *content* of the Scholarly Article has the *data* part as embedded JSON-LD.
3. The *data* part of the Scholarly Article is included in the *manifest* resource. 

### 4.8. Properties

Usage of properties and entities in the manifest is equivalent to their use in the data file(s). See below.

## 5. Data

### 5.1. Introduction
The Scholarly Article data is defined by a set of properties, ontological and narrative entities that describe the essential (meta) data about the article. The properties and ontological entities are are defined by [schema.org](https://schema.org). The narrative entities are defined here.

### 5.2. Narrative Requirements
Narrative entity types are defined in the narrative structure vocabulary. They exist in the `nas` namespace (`https://cpld.example.com/publishing/schema/nas/`).

* Narrative entities MUST be defined in the `doc` namespace, as specified by the CP/LD standard.
* Narrative entities MUST have a narrative entity type as value for the `type` property.
* Every narrative entity MUST be linked directly from the document entity through the `schema:hasPart` relation.
* Every narrative entity MUST have a corresponding element in the HTML content.

###### 5.2.0.0.1. EXAMPLE
```
{
    ...
    "id": "https://cpld.example.com/document/3a2b3c"
    "hasPart": [
        { "id": "doc:el1", "type": "Introduction" }
        ...
    ]
    ...
}
```

#### 5.2.1. REQUIRED <!-- omit from toc -->

* `Abstract` - The academic abstract of the article
* `Affiliation` - Text that represents the affiliation of one of the authors
* `AuthorName` - The name of an author
* `Byline` - Part of the text that gives the names of the author(s)
* `Title` - The title of the article
  
#### 5.2.2. RECOMMENDED <!-- omit from toc -->

* `Acknowledgement` - A paragraph that lists any grants or other contributions by parties other than the author(s)
* `Citation` - A mention in the running text, of a scientific work listed in the references section.
* `Conclusion` - A section that contains the conclusion of the article
* `CorrespondingAuthorName` - The name of the corresponding author
* `EditorHighlights` - Any highlights for the article, usually a bulleted list provided by the editor(s).
* `Evaluation` - A section that describes the way in which the research outcomes were evaluated.
* `Highlights` - Any highlights for the article, usually a bulleted list provided bu the author(s).
* `Introduction` - The introduction section
* `Keyword` - A single keyword
* `Keywords` - Descriptive keywords for the article
* `Materials` - A section that describes the materials used for the research.
* `Method` - A section that describes the method(s) used for the research.
* `Reference` - A description of another scientific work 
* `References` - A section that lists every reference to other scientific work that is cited in the article.
* `Results` - A section that describes the results of the research.

#### 5.2.3. Additional requirements

There MUST NOT be any `Reference` that does not also have a `Citation` and vice versa.

### 5.3. Property and Ontological Requirements

The real world entities described in the Scholarly Article data are essential for understanding who created the article, how it relates to other articles, and what the scientific contribution of the article is.

They are expressed using the [schema.org](https://schema.org) vocabulary.

#### 5.3.1. REQUIRED <!-- omit from toc -->
* `author`
* `conformsTo`
* `@context`
* `hasPart`
* `id` (Document IRI)
* `title`
* `type`

#### 5.3.2. RECOMMENDED <!-- omit from toc -->
* `abstract`
* `citation`
* `copyrightHolder`
* `copyrightNotice`
* `copyrightYear`
* `dateCreated`
* `dateModified`
* `inLanguage`
* `license`
* `publisher`

### 5.4. Data Contexts

The data context needs to include the CP/LD context from `https://niso.org/cpld` to import definitions that are specific to CP/LD, such as the Narrative Structure Vocabulary.

###### 5.4.0.0.1. EXAMPLE<!-- omit from toc -->
```
{
  "@context": [
      "https://schema.org",
      "https://www.w3.org/ns/pub-context",
      "https://niso.org/cpld"
      {"language" : "en"}
  ]
  ...
}
```

### 5.5. Identifier

The identifier value for the `id` property MUST be the Document IRI as specified by the CP/LD standard.

### 5.6. Scholarly Article Conformance

As in the manifest, the conformance URL expressed in the `conformsTo` term MUST be "`https://niso.org/cpld/article/`"

### 5.7. Publication Type

As in the manifest, the *publication type* is defined using the `type` term. The value for the `type` property MUST be "[`ScholarlyArticle`](https://schema.org/ScholarlyArticle)":

### 5.8. Parts

Any element in the HTML of the Scholarly Article that has associated statements in the JSON-LD MUST be related from the Article via the `hasPart` relation.

See the Narrative Requirements (above)

### 5.9. Authors

The author(s) of the Scholarly Article are entities of type `Person`, with sufficient properties to disambiguate between them. 

* It is RECOMMENDED for the entities to have a well known IRI identifier, such as an ORCID IRI. Non-IRI identifiers should be expressed using the `identifier` property defined by [schema.org](https://schema.org).
* Note that these entities MAY be defined externally; e.g. the availability of an ORCID IRI is sufficient to retrieve the JSON-LD description of that `Person` entity from ORCID directly through dereferencing.
* The `Person` entities MUST be mentioned in the content HTML.

#### 5.9.1. REQUIRED
* `familyName`
* `givenName`
* `id`
* `type`

#### 5.9.2. RECOMMENDED
* `email`
* `affiliation` - value MUST be entity of type `Organization`
* `initials`
* `name`

###### 5.9.2.0.1. EXAMPLE
```
{
    "id": "https://cpld.example.com/document/1a2b3c",
    "hasPart": [
        ...
        {"id": "an1", "type": "AuthorName", "mentions": "https://orcid.org/0000-0003-2739-1921"}
        ...
    ]
    "title": "A description of approachable magicians",
    "author": [
        {
            "id": "https://orcid.org/0000-0003-2739-1921",
            "type": "Person",
            "givenName": "Beilar J.",
            "familyName": "Cranorin",
            "affiliation": { "id": "https://example.com/oba882f" }
        },
        {
            ...
        }
    ]
}
```

### 5.10. Citations

Every `Reference` and `Citation` entity indicates a relation between the Scholarly Article and some other work. These are captured using the `citation` property from [schema.org](https://schema.org).

The value of the `citation` property is an entity of type `CreativeWork` or one of its subclasses. 

The `Reference` and `Citation` narrative entities MUST refer to the `CreativeWork` using a `renders` or `mentions` property, respectively.

###### 5.10.0.0.1. EXAMPLE
```
{
    "id": "https://cpld.example.com/document/1a2b3c",
    "hasPart": [
        ...
        {"id": "c1", "type": "Citation", "mentions": "https://dx.doi.org/99.x637277b/112233493517690454"},
        {"id": "r1", "type": "Reference", "renders": "https://dx.doi.org/99.x637277b/112233493517690454"}
        ...
    ]
    "citation": [
        {
            "id": "https://dx.doi.org/99.x637277b/112233493517690454",
            "type": "Article",
            "title": "School-age elves' perception of the elevator experience"
        },
        {
            ...
        }
    ]
}
```

## 6. Content

### 6.1. Introduction
The content file(s) of a Scholarly Article expresses the human-readable information contained in the article.

There MUST at a minimum be one HTML file in the Scholarly Article, and this file MUST be present in the `readingOrder` and `resources` array in the manifest.

Every HTML element that is described in the JSON-LD data MUST have a fragment identifier.

### 6.2. Requirements
The general requirements for the structure of the `<head>` of the HTML content follow from the CP/LD Standard and will not be repeated here.

#### 6.2.1. REQUIRED 

* The `<title>` element in the `<head>` of the HTML MUST reflect the title of the Scholarly Article
* A `<heading>` element that captures, amongst others, the `Title`, `Byline` and `Abstract` narrative entities.
* `<section>` elements for each section of the article

### 6.3. The Header

The header of the Scholarly Article encompasses one of the below Narrative entities, in a fixed structure

#### 6.3.1. REQUIRED
* `Abstract` - The academic abstract of the article
* `Affiliation` - Text that represents the affiliation of one of the authors
* `AuthorName` - The name of an author
* `Byline` - Part of the text that gives information about the author(s) and their affiliations.
* `Title` - The title of the article

#### 6.3.2. OPTIONAL
* `CorrespondingAuthorName` - The name of the corresponding author
* `EditorHighlights` - Any highlights for the article, usually a bulleted list provided by the editor(s).
* `Highlights` - Any highlights for the article, usually a bulleted list provided bu the author(s).
* `Keyword` - A single keyword
* `Keywords` - Descriptive keywords for the article

#### 6.3.3. Template

The `<header>` template has a fixed structure for the `Title`, `Byline` and `Affiliations`. Additional sections in the `<header>` are captured as `<section>` (see the section pattern below).

```
<header id="...">
    <h1 id="[TITLE-ENTITY-ID]">...title...</h1>
    <div id="..."> 
        <div id="[BYLINE-ENTITY-ID]">
            <span id="[AUTHORNAME-ENTITY-ID]">... author name ...</span> and <span id="[AUTHORNAME-ENTITY-ID]">... author name ... </span> ...
        </div>
        <div id="...">
            <dl id="...">
                <dt id="[AFFILIATION-ENTITY-ID]">... affiliation ...</dt>
                <dt id="[AFFILIATION-ENTITY-ID]">... affiliation ...</dt>
                ...
            </dl>
        </div>
    </div>
    <section id="[SECTION-ENTITY-ID]"> 
        <h2 id="...">... section title ...</h2>
        ....
        </div>
    </section>
</header>
```

Note that it is OPTIONAL to create `href` links between the author names and the affiliation lines, but this is not required as that link exists in the JSON-LD data.

### 6.4. Sections

The pattern for each section is as follows:

```
  <section id="[SECTION-ENTITY-ID]"> 
      <h2 id="...">... section title ...</h2>
      ....
      </div>
  </section>
```

### 6.5. References and Citations

Citations 