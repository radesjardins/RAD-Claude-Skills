# rad-google-workspace — Your entire Google Workspace, accessible from Claude Code.

Gmail, Calendar, Drive, Docs, Sheets, Chat, Meet, Tasks, Forms, Classroom, and more — all accessible through natural language or commands. rad-google-workspace provides 93 skills covering direct service access, 41 cross-service workflow recipes, and 10 role-based personas for common job functions. Requires the `gws` CLI.

## What You Can Do With This

- Send emails, schedule meetings, and manage Drive files without leaving your editor
- Run cross-service workflows: convert a Gmail thread to a task, prepare for your next meeting, post-mortem setup, weekly digest
- Automate repetitive Workspace operations: bulk Drive organization, sheet data exports, form response collection
- Operate as a role-based persona — Executive Assistant, Project Manager, IT Admin, and more

## Skill Categories

### Service Skills (44)
Direct API access: Gmail · Calendar · Drive · Docs · Sheets · Slides · Chat · Meet · Tasks · Forms · Keep · Classroom · Admin · People · Events · Model Armor · Apps Script

### Workflow Recipes (41)
Cross-service workflows including: email-to-task, meeting prep, weekly digest, standup report, file announce, expense tracker setup, post-mortem setup, bulk invitations, and more.

### Role-Based Personas (10)
Pre-configured behavioral profiles: Executive Assistant, Team Lead, Project Manager, Sales Ops, IT Admin, HR Coordinator, Content Creator, Event Coordinator, Customer Support, Researcher.

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-google-workspace
```

Requires the `gws` CLI — see [gws installation](https://github.com/googleworkspace/cli).

```
Send an email to alice@example.com
What's on my calendar today?
Prepare me for my next meeting
Run my weekly digest
```

## Attribution

Derivative work based on the [Google Workspace CLI](https://github.com/googleworkspace/cli), Apache License 2.0. Not an officially supported Google product.

## License
Apache-2.0
