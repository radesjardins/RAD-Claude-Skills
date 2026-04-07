# rad-writer Implementation Plan

**Date:** 2026-04-06
**Design:** [rad-writer-design.md](2026-04-06-rad-writer-design.md)
**Status:** Approved

---

## Implementation Order

### Phase 1: Scaffold
1. Create directory structure under `plugins/rad-writer/`
2. Create `.claude-plugin/plugin.json`

### Phase 2: Reference Files (knowledge backbone)
3. Create `references/ai-writing-patterns.md` — AI tells, structural patterns, burstiness
4. Create `references/word-blocklist.md` — flagged words/phrases with replacements
5. Create `references/sentence-craft.md` — rhythm, variety, transitions
6. Create `references/voice-profile-schema.md` — profile template and schema
7. Create `references/domain-email.md`
8. Create `references/domain-blog.md`
9. Create `references/domain-web-copy.md`
10. Create `references/domain-business-report.md`
11. Create `references/domain-research.md`
12. Create `references/domain-presentation.md`
13. Create `references/domain-prose.md`
14. Create `references/domain-technical.md`
15. Create `references/domain-social.md`

### Phase 3: Skills
16. Create `skills/write/SKILL.md`
17. Create `skills/improve/SKILL.md`
18. Create `skills/review/SKILL.md`
19. Create `skills/ai-audit/SKILL.md`

### Phase 4: Agents
20. Create `agents/writing-reviewer/AGENT.md`
21. Create `agents/voice-analyst/AGENT.md`

### Phase 5: Documentation & Validation
22. Create `README.md`
23. Add rad-writer to marketplace.json
24. Validate plugin structure

## Notes
- Reference files should be substantive — they're the knowledge backbone, not stubs
- Skills use `${CLAUDE_SKILL_DIR}/references/` to load domain files
- All files follow existing plugin patterns from rad-brainstormer, rad-code-review, rad-seo-optimizer
