# rad-google-workspace

Google Workspace integration for Claude Code. Requires the `gws` CLI tool.

Provides 42 service skills, 41 workflow recipes, and 10 role-based personas for comprehensive Google Workspace automation.

## Skill Categories

### Service Skills (44)

Direct API access to Google Workspace services:

- **Gmail** — send, read, reply, forward, triage, watch, filter
- **Calendar** — events, agenda, insert, free/busy
- **Drive** — files, folders, shared drives, upload
- **Docs** — read, write, append
- **Sheets** — read, append, write
- **Slides** — read and write presentations
- **Chat** — spaces, messages, send
- **Meet** — conference management
- **Tasks** — task lists and task management
- **Forms** — read and write forms
- **Keep** — note management
- **Classroom** — classes, rosters, coursework
- **Admin** — audit logs and usage reports
- **People** — contacts and profiles
- **Events** — workspace event subscriptions
- **Model Armor** — content safety filtering
- **Apps Script** — script projects, deployments, push local files

### Workflow Recipes (41)

Cross-service productivity workflows including:

- Email to task conversion, meeting prep, weekly digest, standup reports
- Drive file sharing, backup, organization, template creation
- Calendar scheduling, focus time blocking, event creation from sheets
- Form creation, response collection, feedback workflows
- Team announcements, post-mortem setup, bulk invitations

### Role-Based Personas (10)

Pre-configured behavioral profiles: Executive Assistant, Team Lead, Project Manager, Sales Ops, IT Admin, HR Coordinator, Content Creator, Event Coordinator, Customer Support, Researcher.

## Attribution

This plugin is a derivative work based on the [Google Workspace CLI](https://github.com/googleworkspace/cli), licensed under the Apache License 2.0. The original CLI tool definitions have been transformed into Claude Code plugin skill format.

The Google Workspace CLI states: *"This is not an officially supported Google product."*

## Shared Infrastructure

| Skill | Purpose |
|-------|---------|
| `gws-shared` | Authentication patterns, global flags, output formatting |
| `gws-workflow` | Cross-service workflow orchestration |
