---
name: keyword-research
description: Discover and prioritize keywords for a topic or business
arguments:
  - name: topic
    description: "The business, topic, or seed keyword to research"
    required: true
---

Perform keyword research for: **$ARGUMENTS**

Use the `keyword-discovery` skill to execute the full pipeline:

1. **Seed Discovery**: Generate seed keywords from the topic, related terms, and question variations
2. **Expansion**: Find long-tail, question-based, and modifier keywords
3. **Intent Classification**: Classify each keyword as Informational, Commercial, Transactional, or Navigational
4. **Topic Clustering**: Organize into pillar topics, subtopics, and long-tail groups
5. **Prioritization**: Score by business relevance, competition, and content gap status

Output a prioritized keyword plan with:
- Top 10 quick wins (low competition, high relevance)
- Top 10 strategic targets (high value, moderate competition)
- Top 10 long-term plays (high competition, high reward)
- Content type recommendation for each keyword
- Topic cluster map showing pillar → subtopic relationships
