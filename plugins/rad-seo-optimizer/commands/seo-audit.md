---
name: seo-audit
description: Run a comprehensive SEO audit on a website or codebase
arguments:
  - name: target
    description: URL or file path to audit (defaults to current directory)
    required: false
---

Run a comprehensive SEO audit using the `full-seo-audit` skill.

**Target**: $ARGUMENTS (or current working directory if not specified)

Execute the full 6-phase audit pipeline:
1. Technical SEO (crawlability, indexation, Core Web Vitals, mobile, security)
2. On-Page SEO + E-E-A-T (titles, meta, headings, content quality, trust markers)
3. Content & AEO Analysis (quality scoring, AI readiness, semantic structure)
4. Schema & Structured Data (current markup, missing opportunities)
5. Internal Linking & Architecture (orphan pages, link distribution)
6. Competitive Quick-Check (who ranks for target keywords, SERP features)

Generate a scored report (0-100) with prioritized action items, Claude Code fix commands, and a 30/60/90 day roadmap. Save as `seo-audit-report.md`.
