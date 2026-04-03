---
name: recipe-forward-labeled-emails
version: 1.0.0
description: "This skill should be used when the user says \"forward my labeled emails\", \"send these flagged messages to someone\", \"forward everything tagged needs-review\", \"forward a batch of emails\", \"send labeled Gmail messages to another address\", or wants to find Gmail messages with a specific label and forward them to another email address."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail"]
---

# Forward Labeled Gmail Messages

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-gmail`

Find Gmail messages with a specific label and forward them to another address.

## Steps

1. Find labeled messages: `gws gmail users messages list --params '{"userId": "me", "q": "label:needs-review"}' --format table`
2. Get message content: `gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'`
3. Forward via new email: `gws gmail +send --to manager@company.com --subject 'FW: [Original Subject]' --body 'Forwarding for your review:

[Original Message Body]'`

