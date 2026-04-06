# Progressive Summarization — Layer Examples

## Example: Article on Decision-Making

### Layer 1 (Original Excerpt)

The most important factor in making good decisions isn't intelligence or experience — it's
the ability to recognize when you're operating under cognitive bias. Studies from Kahneman
and Tversky showed that even trained statisticians fall prey to anchoring effects when
presented with irrelevant numbers before making estimates. The practical implication is
that you should always generate your own estimate before looking at anyone else's data.
This simple technique — called "pre-commitment" — reduces anchoring bias by 40-60% in
controlled studies. Another effective technique is the "outside view": before evaluating
your specific situation, look at base rates for similar situations. Most people estimate
their project will take 2 weeks; the base rate for similar projects is 6 weeks.

### Layer 2 (Bold Key Points)

The most important factor in making good decisions isn't intelligence or experience — **it's
the ability to recognize when you're operating under cognitive bias**. Studies from Kahneman
and Tversky showed that even trained statisticians fall prey to anchoring effects when
presented with irrelevant numbers before making estimates. **The practical implication is
that you should always generate your own estimate before looking at anyone else's data.**
This simple technique — called **"pre-commitment" — reduces anchoring bias by 40-60%** in
controlled studies. Another effective technique is the **"outside view": before evaluating
your specific situation, look at base rates for similar situations**. Most people estimate
their project will take 2 weeks; **the base rate for similar projects is 6 weeks**.

### Layer 3 (Highlight Best of Bold)

**It's the ability to recognize when you're operating under cognitive bias.**
**==You should always generate your own estimate before looking at anyone else's data.==**
**"Pre-commitment" — reduces anchoring bias by 40-60%.**
**=="Outside view": before evaluating your specific situation, look at base rates.==**
**The base rate for similar projects is 6 weeks.**

### Layer 4 (Executive Summary)

- Pre-commit to your own estimate before seeing others' data — reduces anchoring bias by 40-60%
- Use the "outside view": check base rates for similar situations before evaluating yours
- Good decisions come from recognizing cognitive bias, not from intelligence or experience

---

## Example: Meeting Transcript

### Layer 1 (Raw Transcript Excerpt)

Sarah: So we've been looking at the Q3 numbers and customer churn is up 12% from last
quarter. The biggest driver seems to be onboarding friction — 60% of churned users never
completed the setup wizard. We tried sending reminder emails but open rates were only 8%.

Mike: What about in-app nudges? The Intercom data shows users who get a contextual prompt
within the first 24 hours have a 3x completion rate.

Sarah: That's a good point. The eng team said they could ship that in about two sprints.
The other thing we noticed is that users who connect at least one integration in the first
week have 85% retention at 90 days versus 30% for those who don't.

### Layer 4 (Executive Summary)

- Churn up 12% Q3 — root cause: 60% of churned users never finished setup wizard
- In-app contextual prompts within 24 hours → 3x setup completion (ship in 2 sprints)
- Users who connect 1+ integration in first week: 85% retention vs 30% — this is the key activation metric
- Decision needed: prioritize in-app nudges for next sprint

---

## Format Variations

### Obsidian Format
```markdown
> [!summary] Executive Summary
> - Key insight 1
> - Key insight 2

**Bolded text** for Layer 2
==Highlighted text== for Layer 3
```

### Notion Format
Use Notion's native bold and highlight colors. Place executive summary in a callout block
with the "summary" icon.

### Plain Text Format
```
=== EXECUTIVE SUMMARY ===
- Key insight 1
- Key insight 2

[KEY] Important bolded passage for Layer 2
[!!!] Critical highlighted passage for Layer 3
```
