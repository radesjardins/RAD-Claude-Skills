---
name: recipe-review-overdue-tasks
version: 1.0.0
description: "This skill should be used when the user says \"show my overdue tasks\", \"what tasks are past due\", \"check my late tasks\", \"find tasks I haven't finished\", \"review my overdue to-dos\", or wants to find Google Tasks items that are past their due date and need attention."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-tasks"]
---

# Review Overdue Tasks

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-tasks`

Find Google Tasks that are past due and need attention.

## Steps

1. List task lists: `gws tasks tasklists list --format table`
2. List tasks with status: `gws tasks tasks list --params '{"tasklist": "TASKLIST_ID", "showCompleted": false}' --format table`
3. Review due dates and prioritize overdue items

