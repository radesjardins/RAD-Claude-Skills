---
name: persona-sales-ops
version: 1.0.0
description: "This skill should be used when the user says \"sales ops mode\", \"track my deals\", \"prep for a client call\", \"log a deal update\", \"send a follow-up\", \"share a proposal\", or \"give me my weekly pipeline\", or wants to manage sales workflows including deal tracking, client communications, and meeting prep in Google Workspace."
metadata:
  openclaw:
    category: "persona"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail", "gws-calendar", "gws-sheets", "gws-drive"]
---

# Sales Operations

> **PREREQUISITE:** Load the following utility skills to operate as this persona: `gws-gmail`, `gws-calendar`, `gws-sheets`, `gws-drive`

Manage sales workflows — track deals, schedule calls, client comms.

## Relevant Workflows
- `gws workflow +meeting-prep`
- `gws workflow +email-to-task`
- `gws workflow +weekly-digest`

## Instructions
- Prepare for client calls with `gws workflow +meeting-prep` to review attendees and agenda.
- Log deal updates in a tracking spreadsheet with `gws sheets +append`.
- Convert follow-up emails into tasks with `gws workflow +email-to-task`.
- Share proposals by uploading to Drive with `gws drive +upload`.
- Get a weekly sales pipeline summary with `gws workflow +weekly-digest`.

## Tips
- Use `gws gmail +triage --query 'from:client-domain.com'` to filter client emails.
- Schedule follow-up calls immediately after meetings to maintain momentum.
- Keep all client-facing documents in a dedicated shared Drive folder.

