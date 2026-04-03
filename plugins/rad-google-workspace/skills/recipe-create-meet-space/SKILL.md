---
name: recipe-create-meet-space
version: 1.0.0
description: "This skill should be used when the user says \"create a Meet link\", \"set up a video call\", \"generate a meeting room\", \"make a Google Meet space\", \"send out a meeting link\", or wants to create a Google Meet conference space and share the join link with participants via Gmail."
metadata:
  openclaw:
    category: "recipe"
    domain: "scheduling"
    requires:
      bins: ["gws"]
      skills: ["gws-meet", "gws-gmail"]
---

# Create a Google Meet Conference

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-meet`, `gws-gmail`

Create a Google Meet meeting space and share the join link.

## Steps

1. Create meeting space: `gws meet spaces create --json '{"config": {"accessType": "OPEN"}}'`
2. Copy the meeting URI from the response
3. Email the link: `gws gmail +send --to team@company.com --subject 'Join the meeting' --body 'Join here: MEETING_URI'`

