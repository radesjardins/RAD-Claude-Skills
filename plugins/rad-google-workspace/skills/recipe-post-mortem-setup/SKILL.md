---
name: recipe-post-mortem-setup
version: 1.0.0
description: "This skill should be used when the user says \"set up a post-mortem\", \"create an incident review\", \"run a post-mortem for this outage\", \"document the incident and schedule a review\", \"start a post-mortem doc\", or wants to create a Google Docs post-mortem document, schedule a review meeting in Google Calendar, and notify the team via Google Chat."
metadata:
  openclaw:
    category: "recipe"
    domain: "engineering"
    requires:
      bins: ["gws"]
      skills: ["gws-docs", "gws-calendar", "gws-chat"]
---

# Set Up Post-Mortem

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-docs`, `gws-calendar`, `gws-chat`

Create a Google Docs post-mortem, schedule a Google Calendar review, and notify via Chat.

## Steps

1. Create post-mortem doc: `gws docs +write --title 'Post-Mortem: [Incident]' --body '## Summary\n\n## Timeline\n\n## Root Cause\n\n## Action Items'`
2. Schedule review meeting: `gws calendar +insert --summary 'Post-Mortem Review: [Incident]' --attendee team@company.com --start '2026-03-16T14:00:00' --end '2026-03-16T15:00:00'`
3. Notify in Chat: `gws chat +send --space spaces/ENG_SPACE --text '🔍 Post-mortem scheduled for [Incident].'`

