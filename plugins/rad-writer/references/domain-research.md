# Research Writing Reference

## Abstract Structure

### The Five-Move Abstract
A well-structured abstract follows five moves, each earning its sentence(s):

1. **Background** (1-2 sentences): Establish the context. What is known. What the field accepts.
   - "Microplastic contamination has been documented in freshwater systems worldwide, yet the mechanisms driving bioaccumulation in filter-feeding organisms remain poorly understood."

2. **Gap** (1 sentence): What is *not* known. What the existing literature fails to address.
   - "No prior study has examined whether microplastic uptake rates vary with particle surface charge under environmentally relevant concentrations."

3. **Method** (1-2 sentences): What you did, compressed to its essence. Not the full methodology — just enough to evaluate the claim.
   - "We exposed Daphnia magna to positively and negatively charged polystyrene microspheres (1-10 μm) at three concentrations (10, 100, 1000 particles/mL) over 96 hours."

4. **Result** (1-2 sentences): The key finding. Not all findings — the one or two that matter most.
   - "Positively charged particles showed 3.2x higher uptake rates (p < 0.001) and significantly longer gut retention times compared to negatively charged particles of identical size."

5. **Implication** (1 sentence): Why this matters. What changes because of this finding.
   - "These results suggest that environmental risk assessments based solely on particle size may substantially underestimate bioaccumulation potential for positively charged microplastics."

### IMRaD Scaffold for Abstracts
A condensed version of the five-move abstract, useful as a quick template: **Context** (1 sentence) -> **Problem** (1 sentence) -> **Methods** (1 sentence) -> **Results** (1-2 sentences) -> **Significance** (1 sentence). Total: 5-6 sentences. This maps directly to the IMRaD structure of the paper itself, making the abstract a fractal of the whole.

### Abstract Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Starting with "In this paper, we..." | "In this paper, we examine the effects of..." | Start with the context or problem, not the paper's existence. This opening fails to introduce narrative tension — the reader needs to care about the problem before they care about your paper. |
| Repeating the title | Title: "Effects of surface charge on microplastic uptake." Abstract: "This study investigates the effects of surface charge on microplastic uptake." | The abstract should add information, not echo the title. |
| Reporting all results | Listing every finding from every experiment | Select the 1-2 results that support the main claim. Details go in the Results section. |
| No gap statement | Jumping from background to method | Without a gap, the reader can't evaluate why this study was necessary. |
| Vague implications | "These findings have important implications for the field." | *Which* implications? For *whom*? State the specific consequence. |
| Including citations | "Previous studies (Smith et al., 2023; Jones, 2022) have shown..." | Abstracts generally do not include citations. State what is known; cite it in the Introduction. |

### Length Guidelines
- Most journals: 150-300 words.
- Structured abstracts (common in medicine): Background, Methods, Results, Conclusions — with explicit labels.
- Conference abstracts: Often 200-500 words with more method detail.
- Always check the target journal's requirements. Exceeding the word limit is an immediate desk-reject risk.

---

## Literature Review: Synthesis vs. Summary

### The Core Distinction
- **Summary** (avoid): "Smith (2020) found X. Jones (2021) found Y. Lee (2022) found Z."
- **Synthesis** (do this): "While early work established that X occurs (Smith, 2020), subsequent studies revealed that the mechanism varies by context: Jones (2021) demonstrated Y under controlled conditions, whereas Lee (2022) found the opposite effect in field settings, suggesting that Z may be a moderating factor."

### Synthesis Strategies

**Thematic Organization**
Group studies by what they argue, not by when they were published or who wrote them.
- **Do this**: "Three competing explanations exist for [phenomenon]: the resource-limitation model (A, B, C), the behavioral adaptation model (D, E), and the hybrid framework proposed by F."
- **Not that**: "A (2018) proposed... B (2019) extended... C (2020) challenged... D (2021) offered a different perspective..."

**Identifying Contradictions**
Where studies disagree is where the interesting science lives.
- "A and B reach opposing conclusions regarding the effect of temperature on X. The discrepancy likely stems from differences in sample preparation: A used field-collected specimens while B used lab-reared populations."

**Tracking Methodological Evolution**
Show how methods have improved and what new methods reveal that old methods couldn't.
- "Early studies relied on gravimetric analysis, which cannot distinguish microplastics from natural particles below 100 μm. The introduction of FTIR spectroscopy (C, 2019) resolved this limitation and revealed contamination rates 2-4x higher than previously reported."

**Building to the Gap**
The literature review should logically arrive at the gap your study fills. Each paragraph should move closer to the question you're asking.
- Final paragraph of lit review: "Despite advances in understanding X, no study has examined Y under conditions Z. This gap is significant because [reason]. The present study addresses this gap by [approach]."

### Literature Review Anti-Patterns
- **The Wikipedia dump**: Exhaustive coverage of everything ever written, with no argument or direction. A lit review is not a bibliography in prose form.
- **The catalogue anti-pattern**: Dutiful author-by-author listing — "Smith found X. Jones found Y. Lee found Z." — without synthesis or argument. Each paragraph reads like a separate book report. Better: curate sources into roles — **Pioneers** (who established the foundation), **Developers** (who extended or refined it), **Challengers** (who contradicted or complicated it). This reveals gaps organically.
- **The recency trap**: Citing only papers from the last 3 years. Foundational work matters, even if it's 20 years old.
- **The hero narrative**: "Previous researchers failed to consider X, but *our* study brilliantly addresses..." Respectful framing: "Prior work has not yet examined X, which the present study aims to address."
- **Citation clusters without integration**: "(A, 2018; B, 2019; C, 2020; D, 2021; E, 2022)" with no discussion of what each found or how they relate to each other.
- **Leading with author names**: "Smith (2020) found..." puts the scholar before the idea. Lead lit review paragraphs with conceptual claims, not author names: "Surface charge mediates uptake rates more than particle size (Smith, 2020; Jones, 2021)." The idea is the topic sentence; the citation is evidence.

---

## Methodology Writing

### What Methodology Sections Must Do
The reader should be able to replicate your study from the methodology section alone. If they can't, it's incomplete.

### Structure
1. **Research design**: Experimental? Observational? Qualitative? Mixed methods? State it explicitly.
2. **Participants / Samples**: Who or what, how many, how selected, inclusion/exclusion criteria.
3. **Materials / Instruments**: What tools, software, surveys, equipment. Include version numbers, manufacturers, settings.
4. **Procedure**: Step-by-step what you did, in chronological order.
5. **Data analysis**: Statistical tests (with justification), software used, significance thresholds, handling of missing data.

### Methodology Mistakes

| Mistake | Why it matters |
|---|---|
| "We used standard methods" without citing or describing them | Unverifiable. Which standard? Whose version? |
| Missing sample size justification | Underpowered studies produce unreliable results. Report power analysis or precedent. |
| Vague analysis description | "Data were analyzed using appropriate statistical tests" — which tests? Why those? |
| Omitting software versions | Results may not be reproducible with different versions. "R v4.3.1" not just "R." |
| No mention of ethical approval | For human or animal subjects, IRB/IACUC approval is mandatory. State the protocol number. |
| Combining method and results | Keep them separate. Methods say what you *did*; results say what you *found*. |

### The "Future Self" Replication Test
Write every methodological detail as if your future self — working at a different institution, five years from now, without access to your lab notebook — needs to reproduce this study exactly. If you'd need to email someone to fill in a gap, the Methods section is incomplete. This standard catches the most common methodology omissions: instrument settings, software versions, randomization procedures, and environmental conditions.

### Writing Methodology Well
- Use past tense: "Participants were recruited..." not "Participants are recruited..."
- Be specific about quantities: "incubated at 37°C for 24 hours" not "incubated at the appropriate temperature."
- Justify non-obvious choices: "We selected a 96-hour exposure period based on the organism's gut clearance rate (48 hours; Smith, 2020), allowing for two complete clearance cycles."
- Include negative controls and their rationale.

---

## Results vs. Discussion Discipline

### The Boundary
**Results**: What you found. Facts, numbers, statistical outcomes. No interpretation.
**Discussion**: What it means. Interpretation, comparison to prior work, implications, limitations.

### Results Section Rules
- Report findings in logical order (usually matching the order of research questions or hypotheses).
- Lead each paragraph with the main finding, then provide supporting detail.
- **Summarize general patterns first**, then provide specifics. Don't repeat table data in excruciating detail — the table is already there. Instead, narrate the story the data tells: "Uptake rates increased with concentration across all charge conditions (Table 2), but the effect was 3x stronger for positively charged particles."
- **Do this**: "Positively charged particles showed significantly higher uptake rates than negatively charged particles (M = 142.3 vs. 44.7 particles/organism; t(58) = 7.82, p < .001, d = 2.03)."
- **Not that**: "The results were interesting and showed some notable differences between the two conditions that warrant further investigation."
- Refer to figures and tables explicitly: "As shown in Figure 2, uptake rates increased linearly with concentration for positively charged particles (R² = 0.94)."
- Report non-significant results too. They're data, not failures.
- Do not use "significant" to mean "important." In a Results section, "significant" means p < alpha.

### Discussion Section Rules
- Start by restating the main finding in plain language (not statistics).
- **Compare with existing literature** — this is the Discussion's primary job, not just restating results with added citations. Show how your findings confirm, extend, or contradict prior work, and explain *why* the differences exist.
- Propose mechanisms: Why did you observe what you observed?
- Address limitations honestly. Every study has them. Pretending otherwise damages credibility.
- Distinguish between what the data *show* and what you *speculate*. Use hedging calibration (see next section).
- End with implications and future directions. Be specific: "Future studies should examine X using Y method" not "More research is needed."

---

## Hedging Calibration

### The Spectrum
Scientific writing requires precise calibration of certainty language:

| Certainty level | Language | When to use |
|---|---|---|
| Near-certain | "demonstrates", "shows", "establishes", "confirms" | Replicated findings with large effect sizes and strong methodology |
| High confidence | "indicates", "reveals", "provides evidence that" | Well-designed study with clear results, but not yet replicated |
| Moderate confidence | "suggests", "appears to", "is consistent with" | Reasonable interpretation of data, but alternative explanations exist |
| Tentative | "may", "might", "could potentially", "raises the possibility" | Speculative interpretation, preliminary data, indirect evidence |
| Exploratory | "warrants further investigation", "it remains to be determined" | No direct evidence, but logical inference from adjacent findings |

### Hedging Calibration Technique
Balance one hedging word with a more absolute verb to avoid both over- and under-claiming. Example: "Our results **suggest** that X **decreases** Y" — "suggest" hedges the certainty while "decreases" states a clear directional claim. This creates precise modulation: the reader understands you're confident about the direction but appropriately cautious about the generalizability.

### Hedging Mistakes

**Under-hedging** (claiming too much):
- "This proves that X causes Y." (Single studies rarely prove causation.)
- "Our results definitively show..." (Almost nothing in science is definitive.)
- **Risk**: Reviewers will flag overclaiming immediately. It signals inexperience.

**Over-hedging** (claiming too little):
- "It is possible that these results might potentially suggest that there could be a relationship..."
- "It may perhaps be the case that..."
- **Risk**: Dilutes findings to the point of meaninglessness. If your data show something, say so with appropriate confidence.

### Discipline-Specific Hedging Norms
- **Biomedical sciences**: Conservative hedging is expected. "Associated with" rather than "causes." "Preliminary evidence suggests" is standard even for strong findings.
- **Physics / Engineering**: More direct language is acceptable when results are well-supported. "We show that X..." is normal.
- **Social sciences**: Heavy hedging is the norm. "Our findings suggest..." even for statistically significant results.
- **Humanities**: Less about statistical hedging, more about interpretive framing. "This reading suggests..." / "One possible interpretation is..."

---

## Discipline-Specific Conventions

### STEM
- **Structure**: IMRaD (Introduction, Methods, Results, and Discussion) is near-universal and strictly enforced.
- **Voice**: Neutral, third person, passive voice traditionally preferred ("Samples were collected..."). Some journals now accept first person ("We collected samples..."). Check style guide. No figurative language — metaphors and analogies are rare and reserved for review articles.
- **Citation format**: Numbered (Vancouver) in medicine and engineering; author-date (APA or similar) in biology and psychology.
- **Figures**: Expected and often primary. "A figure is worth a thousand words" is literal in STEM.
- **Supplementary materials**: Common for additional data, extended methods, code.
- **Reproducibility**: Methods must be detailed enough for replication. Data and code sharing increasingly expected.

### Social Sciences
- **Structure**: Modified IMRaD with more flexible organization. Theory sections are common, and heavy theoretical frameworks are expected.
- **Voice**: First person increasingly accepted ("We argue..."). Active voice preferred.
- **Citation format**: APA (psychology, education), ASA (sociology), Chicago (political science).
- **Theory**: Theoretical framing is central. Unlike STEM, where theory is sometimes implicit, social sciences require explicit theoretical positioning.
- **Qualitative data**: Quotes from participants are primary evidence. Presented verbatim with context.
- **Reflexivity**: In qualitative research, the researcher's position and potential biases are acknowledged explicitly.

### Humanities
- **Structure**: Thesis-driven essay format — argument-driven, not method-driven. No IMRaD.
- **Voice**: First person welcomed and expected. Active voice. The scholar's interpretive stance is part of the argument.
- **Citation format**: Chicago/Turabian (footnotes), MLA (in-text parenthetical).
- **Evidence**: Close reading of texts, archival documents, cultural artifacts. The evidence *is* the interpretation.
- **Length**: Often longer than STEM papers. 8,000-12,000 words is common for journal articles.
- **Argumentation**: The contribution is the argument itself, not a data set. Originality of interpretation matters.

### Applied Fields (Engineering, Public Health, Policy, Education)
- **Structure**: Problem-solving focus. Often follows a problem -> analysis -> recommendation flow rather than strict IMRaD.
- **Voice**: Direct, plain language. Avoids both the hedging of social sciences and the abstraction of humanities.
- **Audience**: Practitioners as well as academics. Writing must be accessible to decision-makers who may not be specialists.
- **Recommendations**: Explicit and actionable. Unlike basic research, applied papers are expected to end with direct recommendations, not just "implications for future research."

---

## Common Reviewer Complaints

### Structural Issues
- "The paper lacks a clear contribution statement." **Fix**: State what this paper adds to the field in the Introduction's final paragraph.
- "The literature review is not comprehensive." **Fix**: Doesn't mean cite everything — means cover the relevant strands and identify the gap systematically.
- "Methods are insufficiently detailed for replication." **Fix**: Another researcher in your field should be able to reproduce your study from Methods alone.
- "Results and Discussion are conflated." **Fix**: Separate findings (data) from interpretation (meaning).

### Writing Quality Issues
- "The paper is too long / could be more concise." **Fix**: Cut literature review background that doesn't directly support the gap. Eliminate redundancy between Results and Discussion.
- "The writing is unclear in several places." **Fix**: Usually means overly complex sentences. Simplify. One idea per sentence.
- "The authors overclaim their findings." **Fix**: Calibrate hedging language. Use "suggests" instead of "proves."

### Methodological Issues
- "Sample size is too small / not justified." **Fix**: Include power analysis or justify sample size based on precedent.
- "No control condition / baseline." **Fix**: Even in observational studies, establish what you're comparing against.
- "Statistical tests are inappropriate." **Fix**: Justify test selection. Common errors: using parametric tests on non-normal data, not correcting for multiple comparisons.

### Argumentation Issues
- "The gap is not well-motivated." **Fix**: Explain *why* the gap matters, not just that it exists. What depends on filling it?
- "Alternative explanations are not addressed." **Fix**: In Discussion, explicitly state alternative interpretations and why your interpretation is more supported.
- "The implications are vague." **Fix**: "These findings have implications for..." is a placeholder. State the *specific* implications.

---

## Ethics of AI in Academic Writing

### Current Landscape
- Policies vary wildly by journal, institution, and discipline. Check before using AI assistance.
- Many journals (Nature, Science, ICML) require disclosure of AI tool use in the methods or acknowledgments.
- AI cannot be listed as an author (per ICMJE, COPE, and most major publishers) because it cannot take responsibility for the work.

### Ethical Uses of AI in Academic Writing
- **Grammar and clarity editing**: Using AI to improve sentence-level clarity is generally accepted, similar to using Grammarly or a copyeditor.
- **Literature search assistance**: Using AI to find relevant papers, though citations must be independently verified (AI hallucinates citations).
- **Code generation for analysis**: Using AI to write analysis scripts, with human verification of correctness.
- **Translation**: Using AI to translate writing from the author's native language into the journal's language.
- **Brainstorming and outlining**: Using AI to structure arguments or identify gaps in reasoning.

### Unethical Uses of AI in Academic Writing
- **Generating fabricated citations**: AI invents plausible-looking citations that don't exist. Every citation must be verified by the author.
- **Generating fabricated data or results**: Presenting AI-generated data as experimental findings is fabrication — a cardinal sin of research.
- **Submitting AI-generated text without disclosure**: If the journal requires disclosure and you don't disclose, it's a form of academic dishonesty.
- **Using AI to write peer reviews**: Reviewers are selected for their expertise. Outsourcing review to AI undermines the peer review system.
- **Paraphrasing others' work through AI to avoid plagiarism detection**: Using AI to reword plagiarized content is still plagiarism.

### Disclosure Best Practices
- If you used AI tools, state which tools, how they were used, and in which sections.
- Example: "ChatGPT (GPT-4, OpenAI) was used for initial literature search queries and grammar editing of the manuscript. All citations were independently verified. All analysis, interpretation, and scientific claims are the work of the authors."
- Keep records of AI interactions in case of audit.

---

## Context-Gathering Questions

Before writing any research document, ask:
1. **What is the target venue?** Journal, conference, thesis chapter? Each has specific formatting, length, and style requirements.
2. **What discipline are we in?** STEM, social science, or humanities? This determines structure, voice, and evidence standards.
3. **What is the specific contribution?** Not the topic — the *contribution*. What does this paper add that didn't exist before?
4. **What stage is the research?** Proposal (future tense), methods paper (justifying approach), empirical paper (reporting results), review paper (synthesizing field)?
5. **Who are the likely reviewers?** What would they expect to see? What would they object to?
6. **What is the target word count?** Journal requirements, conference limits, thesis chapter guidelines.
7. **What citation format is required?** APA, Chicago, Vancouver, MLA, IEEE?
8. **Are there AI disclosure requirements?** Check the journal's policy before using AI tools.

---

## Quality Criteria for Research Writing Review

- [ ] The abstract follows the five-move structure: background, gap, method, result, implication
- [ ] The literature review synthesizes rather than summarizes — studies are in conversation, not in sequence
- [ ] The gap is clearly stated and motivated (why it matters, not just that it exists)
- [ ] Methods are detailed enough for replication, with all tools, versions, and parameters specified
- [ ] Results and Discussion are clearly separated (no interpretation in Results, no new data in Discussion)
- [ ] Hedging is calibrated: claims match the strength of the evidence
- [ ] Every citation is relevant, correctly formatted, and actually supports the claim it's attached to
- [ ] Figures and tables are titled with findings (not descriptions), properly labeled, and referenced in text
- [ ] Limitations are acknowledged honestly and specifically
- [ ] The paper follows the conventions of its target discipline and venue
- [ ] All AI tool use is disclosed per the target venue's policy

---

## AI Pattern Considerations

### Common AI Tells in Research Writing
- **Hallucinated citations**: AI generates author names, titles, and DOIs that look plausible but don't exist. This is the most dangerous AI tell because it constitutes fabrication. Every citation must be independently verified.
- **Generic literature reviews**: "Extensive research has been conducted in this area (Author, Year; Author, Year; Author, Year)." AI fills parentheses with names but doesn't actually engage with what each study found.
- **Overly smooth prose**: Real academic writing has some awkwardness — technical terms that don't flow naturally, sentence structures demanded by precision over elegance. AI-generated academic text is often *too* readable.
- **Missing methodological specifics**: AI describes methods in generalities: "Data were collected using standard protocols" rather than specifying the exact protocol, parameters, and instruments.
- **Balanced to the point of non-contribution**: "Some researchers argue X while others argue Y." AI struggles to take a position. Real research papers take positions.
- **Formulaic transitions**: "Furthermore," "Moreover," "Additionally," "In contrast," used in predictable rotation. Real academic writers use more varied (and sometimes less elegant) transitions.
- **Perfect paragraph structure**: Every paragraph starts with a topic sentence, has 3-4 supporting sentences, and ends with a transition. Real academic paragraphs are less uniform.
- **Lack of field-specific terminology**: AI sometimes uses general language where field-specific terms are expected and more precise.
- **Fabricated statistics in examples**: "Studies show that 73% of..." without a source. In research writing, every statistic must be traced to a specific source.

### Making AI-Assisted Research Sound Authentic
- Verify every citation independently. Search the DOI, check the author's publication list, read the abstract.
- Add field-specific terminology that AI might have generalized. "Machine learning model" might need to be "gradient-boosted decision tree (XGBoost, Chen & Guestrin, 2016)."
- Insert methodological specifics that only someone who did the work would know: instrument serial numbers, exact software versions, quirks in data collection.
- Add honest uncertainty: "We initially attempted X but found it unreliable due to Y, leading us to adopt Z."
- Reference unpublished or in-press work, conference presentations, and personal communications that AI wouldn't have access to.
- Ensure the Discussion section engages *deeply* with 2-3 key papers, not superficially with 20.
- Add limitations that are specific to your study, not generic limitations that apply to any study in the field.
- Use footnotes or parenthetical asides for methodological caveats that only a practitioner would think to include.
