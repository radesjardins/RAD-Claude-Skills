---
name: recipe-draft-email-from-doc
version: 1.0.0
description: "This skill should be used when the user says \"send my doc as an email\", \"draft an email from a Google Doc\", \"use this document as my email body\", \"email the contents of my doc\", \"turn my doc into an email\", or wants to read content from a Google Docs document and send it as the body of a Gmail message."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-docs", "gws-gmail"]
---

# Draft a Gmail Message from a Google Doc

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-docs`, `gws-gmail`

Read content from a Google Doc and use it as the body of a Gmail message.

## Steps

1. Get the document content: `gws docs documents get --params '{"documentId": "DOC_ID"}'`
2. Copy the text from the body content
3. Send the email: `gws gmail +send --to recipient@example.com --subject 'Newsletter Update' --body 'CONTENT_FROM_DOC'`

