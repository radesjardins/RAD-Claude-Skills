---
name: recipe-create-feedback-form
version: 1.0.0
description: "This skill should be used when the user says \"create a feedback form\", \"make a survey\", \"set up a Google Form\", \"send out a form to collect feedback\", \"build a survey and email it\", or wants to create a Google Form for collecting feedback and share it with recipients via Gmail."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-forms", "gws-gmail"]
---

# Create and Share a Google Form

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-forms`, `gws-gmail`

Create a Google Form for feedback and share it via Gmail.

## Steps

1. Create form: `gws forms forms create --json '{"info": {"title": "Event Feedback", "documentTitle": "Event Feedback Form"}}'`
2. Get the form URL from the response (responderUri field)
3. Email the form: `gws gmail +send --to attendees@company.com --subject 'Please share your feedback' --body 'Fill out the form: FORM_URL'`

