# rad-gws-core — Essential Google Workspace skills for Claude Code.

Gmail, Calendar, Drive, Docs, Sheets, and Slides — the core Google Workspace services accessible through natural language or commands. rad-gws-core provides 14 focused skills for everyday productivity. Requires the `gws` CLI.

## What You Can Do With This

- Send, read, reply to, and triage emails without leaving your editor
- Create and append to Google Docs
- Read from and append rows to Google Sheets
- Work with Google Slides presentations
- Manage Google Drive files, folders, and permissions
- Manage Google Calendar events, ACLs, and free/busy queries

## Skills (14)

### Email (5)
| Skill | Description |
|-------|-------------|
| `gws-gmail` | Broad Gmail management — messages, threads, labels, drafts, filters |
| `gws-gmail-send` | Send a new email |
| `gws-gmail-read` | Read a message body or headers |
| `gws-gmail-reply` | Reply to a message (threaded) |
| `gws-gmail-triage` | Unread inbox summary |

### Documents (2)
| Skill | Description |
|-------|-------------|
| `gws-docs` | Create, read, and batch-update Google Docs |
| `gws-docs-write` | Append text to a document |

### Sheets (3)
| Skill | Description |
|-------|-------------|
| `gws-sheets` | Create, read, and batch-update Google Sheets |
| `gws-sheets-read` | Read values from a spreadsheet range |
| `gws-sheets-append` | Append rows to a spreadsheet |

### Slides (1)
| Skill | Description |
|-------|-------------|
| `gws-slides` | Create, read, and batch-update Google Slides |

### Core (3)
| Skill | Description |
|-------|-------------|
| `gws-drive` | Manage Drive files, folders, permissions, shared drives |
| `gws-calendar` | Manage calendars, events, ACLs, free/busy queries |
| `gws-shared` | Shared auth, global flags, and security rules for all gws-* skills |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-gws-core
```

Requires the `gws` CLI — see [gws installation](https://github.com/googleworkspace/cli).

```
Send an email to alice@example.com
What's on my calendar today?
Read data from my spreadsheet
Append a note to my Google Doc
```

## Attribution

Derivative work based on the [Google Workspace CLI](https://github.com/googleworkspace/cli), Apache License 2.0. Not an officially supported Google product.

## License
Apache-2.0
