---
name: recipe-find-large-files
version: 1.0.0
description: "This skill should be used when the user says \"find my largest files\", \"what's taking up space in Drive\", \"show me big files in Google Drive\", \"I'm running out of storage\", \"clean up my Drive space\", or wants to identify the largest Google Drive files that are consuming storage quota."
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-drive"]
---

# Find Largest Files in Drive

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-drive`

Identify large Google Drive files consuming storage quota.

## Steps

1. List files sorted by size: `gws drive files list --params '{"orderBy": "quotaBytesUsed desc", "pageSize": 20, "fields": "files(id,name,size,mimeType,owners)"}' --format table`
2. Review the output and identify files to archive or move

