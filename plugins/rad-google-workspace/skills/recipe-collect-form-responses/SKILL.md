---
name: recipe-collect-form-responses
version: 1.0.0
description: "This skill should be used when the user says \"check my form responses\", \"see who filled out my form\", \"read Google Form submissions\", \"show form answers\", \"pull responses from my survey\", or wants to retrieve and review responses submitted to a Google Form."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-forms"]
---

# Check Form Responses

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-forms`

Retrieve and review responses from a Google Form.

## Steps

1. List forms: `gws forms forms list` (if you don't have the form ID)
2. Get form details: `gws forms forms get --params '{"formId": "FORM_ID"}'`
3. Get responses: `gws forms forms responses list --params '{"formId": "FORM_ID"}' --format table`

