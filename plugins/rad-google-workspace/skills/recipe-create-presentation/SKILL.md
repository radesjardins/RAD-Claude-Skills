---
name: recipe-create-presentation
version: 1.0.0
description: "This skill should be used when the user says \"create a presentation\", \"make a new slide deck\", \"start a Google Slides deck\", \"build a slideshow\", \"set up a new presentation\", or wants to create a new Google Slides presentation, add initial slides, and share it with collaborators via Drive."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-slides"]
---

# Create a Google Slides Presentation

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-slides`

Create a new Google Slides presentation and add initial slides.

## Steps

1. Create presentation: `gws slides presentations create --json '{"title": "Quarterly Review Q2"}'`
2. Get the presentation ID from the response
3. Share with team: `gws drive permissions create --params '{"fileId": "PRESENTATION_ID"}' --json '{"role": "writer", "type": "user", "emailAddress": "team@company.com"}'`

