---
name: fix-seo
description: Fix a specific SEO issue with guided remediation
arguments:
  - name: issue
    description: "The SEO issue to fix (e.g., 'missing meta descriptions', 'broken links', 'no schema markup', 'slow page speed', 'missing alt text', 'heading hierarchy', 'robots.txt')"
    required: true
---

Fix the specified SEO issue: **$ARGUMENTS**

Follow this process:
1. Identify all instances of this issue in the codebase
2. Explain why this issue matters for rankings (plain English)
3. Show the current state (what's wrong)
4. Apply the fix using the appropriate approach from `references/claude-code-fix-recipes.md`
5. Show the after state (what was fixed)
6. Verify the fix is correct

Reference the relevant skill for deeper context:
- Title/meta/headings → `on-page-optimizer` skill
- Schema/structured data → `schema-architect` skill
- Speed/vitals → `technical-seo` skill
- Broken links → `broken-link-fixer` skill
- Content quality → `content-strategist` skill
