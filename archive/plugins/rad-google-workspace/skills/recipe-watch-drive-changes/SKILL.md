---
name: recipe-watch-drive-changes
version: 1.0.0
description: "This skill should be used when the user says \"watch a Drive folder for changes\", \"notify me when files change\", \"subscribe to Drive change events\", \"set up Drive change notifications\", \"monitor a Drive folder\", or wants to subscribe to Google Workspace event notifications for changes to a Google Drive file or folder via Pub/Sub."
metadata:
  openclaw:
    category: "recipe"
    domain: "engineering"
    requires:
      bins: ["gws"]
      skills: ["gws-events"]
---

# Watch for Drive Changes

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-events`

Subscribe to change notifications on a Google Drive file or folder.

## Steps

1. Create subscription: `gws events subscriptions create --json '{"targetResource": "//drive.googleapis.com/drives/DRIVE_ID", "eventTypes": ["google.workspace.drive.file.v1.updated"], "notificationEndpoint": {"pubsubTopic": "projects/PROJECT/topics/TOPIC"}, "payloadOptions": {"includeResource": true}}'`
2. List active subscriptions: `gws events subscriptions list`
3. Renew before expiry: `gws events +renew --subscription SUBSCRIPTION_ID`

