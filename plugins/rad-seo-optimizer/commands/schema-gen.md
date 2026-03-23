---
name: schema-gen
description: Generate JSON-LD schema markup for a page
arguments:
  - name: type
    description: "Schema type or page path (e.g., 'FAQ', 'Product', 'Article', 'Organization', or a file path to auto-detect)"
    required: false
---

Generate JSON-LD structured data markup using the `schema-architect` skill.

**Target**: $ARGUMENTS (or auto-detect from current page if not specified)

Process:
1. If a file path is provided, read the page and auto-detect the appropriate schema type(s)
2. If a schema type is specified, generate that type with guidance on required properties
3. Extract actual content from the page (never use placeholder data)
4. Generate complete, valid JSON-LD with all required and recommended properties
5. Include integration guidance for the site's framework
6. Identify additional schema opportunities for the page

Output ready-to-paste JSON-LD code blocks with inline comments explaining each property.
