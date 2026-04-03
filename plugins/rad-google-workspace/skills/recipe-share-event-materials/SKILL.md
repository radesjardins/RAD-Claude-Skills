---
name: recipe-share-event-materials
version: 1.0.0
description: "This skill should be used when the user says \"share meeting materials with attendees\", \"send files to everyone on the invite\", \"share docs with meeting participants\", \"distribute materials to calendar guests\", \"give meeting attendees access to files\", or wants to share Google Drive files with all attendees pulled from a Google Calendar event."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-calendar", "gws-drive"]
---

# Share Files with Meeting Attendees

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-calendar`, `gws-drive`

Share Google Drive files with all attendees of a Google Calendar event.

## Steps

1. Get event attendees: `gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'`
2. Share file with each attendee: `gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{"role": "reader", "type": "user", "emailAddress": "attendee@company.com"}'`
3. Verify sharing: `gws drive permissions list --params '{"fileId": "FILE_ID"}' --format table`

