---
name: aeo-check
description: Check AI search engine visibility for a brand
arguments:
  - name: brand
    description: "Brand name, product, or URL to check AI visibility for"
    required: true
---

Check AI search visibility for: **$ARGUMENTS**

Use the `aeo-optimizer` skill to perform an AI visibility audit:

1. **Presence Check**: Search AI platforms (via WebSearch) for brand-relevant queries — is the brand mentioned?
2. **Accuracy Check**: Is the information AI shares about the brand correct?
3. **Sentiment Analysis**: Is the tone positive, neutral, or negative?
4. **Competitor Comparison**: Who else gets recommended for the same queries?
5. **Consistency Check**: Do different AI platforms say the same thing about the brand?

Score across 6 dimensions (Presence, Accuracy, Sentiment, Position, Completeness, Consistency).

Output:
- Current AEO visibility score (0-60)
- Platform-by-platform breakdown
- Top 5 quick wins to improve AI visibility
- Long-term AEO strategy recommendations
- Specific content formatting changes to make (with Claude Code commands)
