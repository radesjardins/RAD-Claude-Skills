# Word Blocklist Reference

Specific words, phrases, and constructions to flag during writing and review. Each entry includes why it's flagged and what to use instead.

**Usage:** Skills load this file to check text against known AI patterns. The `ai-audit` skill uses it for deep pattern scanning. The `write` skill avoids these patterns during generation. The `improve` and `review` skills flag them in existing text.

---

## Severity Levels

- **Always avoid** — these words/phrases have become so strongly associated with AI output that they immediately undermine credibility, regardless of context
- **Context-dependent** — legitimate in specific domains but flagged in general writing
- **Watch** — not automatic flags, but suspicious in clusters or high frequency

---

## Always-Avoid Verbs

| Word | Why flagged | Use instead |
|------|------------|-------------|
| delve | 50% spike post-ChatGPT; the canonical AI tell | explore, examine, dig into, look at, investigate |
| leverage | Became meaningless through AI overuse | use, apply, build on, take advantage of |
| utilize | Almost always replaceable by "use" | use |
| harness | AI default for "use effectively" | use, channel, apply, direct |
| streamline | Vague efficiency claim | simplify, speed up, cut steps from, automate |
| underscore | AI's favorite "emphasize" synonym | emphasize, highlight, show, reveal |
| foster | 10.8x increase post-ChatGPT | encourage, support, build, grow, create |
| navigate | Metaphorical use (navigate challenges) | handle, work through, manage, deal with |
| elevate | Empty intensifier | improve, raise, strengthen |
| empower | Performative; rarely specific | enable, give [someone] the ability to, let |
| spearhead | Grandiose for "lead" | lead, start, drive, run |
| bolster | AI filler for "support" | support, strengthen, reinforce |
| catalyze | Pretentious for "cause" or "start" | cause, trigger, spark, start |
| endeavor | Archaic formality | try, attempt, work to |
| facilitate | Bureaucratic | help, enable, make possible, run |
| embark | "Embark on a journey" is peak AI | start, begin, launch |
| unpack | AI's "let me explain" | explain, break down, examine |
| captivate | Hyperbolic | interest, engage, hold attention |
| resonate | AI default for "connect with" | connect with, matter to, strike a chord with |
| encompass | Unnecessarily formal | include, cover, span |
| revolutionize | Almost never accurate | change, rethink, redesign |
| optimize | Vague efficiency claim | improve, tune, adjust, speed up |
| enhance | Empty intensifier | improve, strengthen, add [specific thing] |
| exemplify | Pretentious for "show" | show, demonstrate, illustrate |
| elucidate | Archaic | explain, clarify, spell out |
| ascertain | Archaic | find out, determine, learn |
| envision | AI planning-speak | imagine, picture, plan |
| unleash | Hyperbolic | release, enable, open up |
| capitalize | AI strategy-speak | take advantage of, use, build on |
| serves as / stands as / represents | AI substitutes for "is" due to repetition penalties | is, acts as, functions as |
| transform | AI "thumbprint" in sales emails | change, reshape, rethink |

## Always-Avoid Adjectives

| Word | Why flagged | Use instead |
|------|------------|-------------|
| pivotal | AI's favorite "important" | important, key, critical, decisive |
| robust | Used for everything from code to breakfast | strong, solid, thorough, reliable |
| innovative | Empty without specifics | new, original, novel, [describe the actual innovation] |
| seamless | SaaS placeholder for missing detail | smooth, easy, simple, integrated |
| cutting-edge | Dated cliché | new, latest, advanced, [describe what's actually new] |
| comprehensive | AI padding | complete, full, thorough, detailed |
| nuanced | 4.8x increase post-ChatGPT | subtle, complex, layered |
| multifaceted | Pretentious for "complex" | complex, varied, many-sided |
| groundbreaking | Almost never true | new, significant, first-of-its-kind |
| transformative | Grandiose | significant, major, substantial |
| holistic | Vague | complete, whole, full-picture, integrated |
| meticulous | AI's "careful" | careful, precise, detailed, thorough |
| intricate | Overwrought | complex, detailed, layered |
| invaluable | Hyperbolic | valuable, essential, useful, important |
| paramount | Unnecessarily formal | most important, top priority, critical |
| exemplary | Performative praise | excellent, outstanding, strong |
| indispensable | Hyperbolic | essential, necessary, critical |

## Always-Avoid Nouns

| Word | Why flagged | Use instead |
|------|------------|-------------|
| landscape | Metaphorical: "the marketing landscape" | field, space, market, industry, world |
| realm | Pretentious | area, field, domain, world |
| tapestry | 7.2x increase in non-textile contexts | mix, combination, range, variety |
| synergy | Corporate cliché | collaboration, combined effect, teamwork |
| testament | "A testament to..." is AI filler | proof, evidence, sign, example |
| paradigm | "Paradigm shift" is almost never true | model, approach, framework, pattern |
| cornerstone | AI's "important thing" | foundation, basis, key part |
| linchpin | Pretentious for "key part" | key, center, core, essential piece |
| bedrock | See cornerstone | foundation, basis, core |
| nexus | Pretentious for "connection" | connection, center, hub, link |
| crucible | Melodramatic | test, challenge, proving ground |
| beacon | "A beacon of hope" — peak AI | example, model, guide, light |
| interplay | AI's "relationship between" | relationship, connection, interaction, tension |
| plethora | Archaic formality | many, plenty, a lot of, abundance |
| myriad | See plethora | many, numerous, countless |
| juxtaposition | Pretentious unless genuinely analytical | contrast, comparison, tension |

## Always-Avoid Adverbs

| Word | Why flagged | Use instead |
|------|------------|-------------|
| arguably | AI hedging | [state the argument directly] |
| undeniably | AI false-confidence | clearly, obviously, [or just assert it] |
| notably | Throat-clearing | [just state the notable thing] |
| remarkably | Empty intensifier | [show why it's remarkable] |
| fundamentally | AI emphasis crutch | at its core, basically, essentially |
| inherently | Over-formal | naturally, by nature, [or cut it] |
| ultimately | AI's paragraph closer | in the end, finally, [or cut it] |
| meticulously | See "meticulous" | carefully, precisely, thoroughly |
| seamlessly | See "seamless" | smoothly, easily, without friction |
| profoundly | Hyperbolic | deeply, significantly, greatly |
| quietly | "Magic adverb" — injects false significance | [cut — describe what's actually quiet] |
| deeply | "Magic adverb" — injects false significance | [cut or use specific depth] |

---

## Always-Avoid Phrases

| Phrase | Why flagged | Use instead |
|--------|------------|-------------|
| It's important to note that | Throat-clearing; just state it | [delete and state the thing] |
| In today's [X] landscape | Dated AI cliché | [cut entirely or be specific about what changed] |
| At the end of the day | Cliché | [cut — the conclusion should be obvious from context] |
| In the realm of | Pretentious filler | in, within, for |
| It's worth mentioning that | If it's worth mentioning, mention it | [delete and state the thing] |
| When it comes to | Filler | for, regarding, with, [or just start with the topic] |
| This is not just X, it's Y | AI contrast framing — manufactured profundity | [state what it actually is] |
| It's not about X, it's about Y | See above | [state your actual point] |
| Let's dive in | AI casual opener | [just start] |
| Without further ado | See above | [just start] |
| But here's the thing | "Tada" intro — false drama | [state the thing] |
| The result? | "Tada" intro | [state the result] |
| And honestly? | False casual vulnerability | [be honest without announcing it] |
| No fluff | Itself is fluff | [be concise without saying you're being concise] |
| Game-changer | Overused to meaninglessness | [describe the actual change] |
| Revolutionizing | Almost never true | changing, improving, rethinking |
| Best-in-class | Unsubstantiated | [provide actual evidence or comparison] |
| Unlocking [value/potential] | AI's favorite metaphor | creating, enabling, finding, building |
| Pave the way for | AI's progress metaphor | enable, lead to, make possible |
| At the forefront of | Grandiose positioning | leading, ahead in, working on |
| Take it to the next level | Vague improvement claim | [describe the specific improvement] |
| Due to the fact that | Bureaucratic | because |
| In light of the fact | See above | because, since, given |
| Navigate the complexities | AI's challenge metaphor | handle, work through, manage |
| Think of it as... / It's like a... | Patronizing "teacher mode" — often less clear than direct explanation | [explain directly] |
| Let's break this down / Let's unpack this | Pedagogical hand-holding even for expert audiences | [just break it down without announcing it] |
| Imagine a world where... | Classic futurism invitation before listing outcomes | [state the actual possibility] |
| Despite its challenges... | Rigid formula: acknowledge problem, immediately dismiss with optimistic pivot | [address challenges substantively or cut] |
| In conclusion / To sum up / In summary | Explicit signposting from rigid template | [write a conclusion that actually concludes] |
| In the ever-evolving landscape | Peak AI temporal filler | [cut entirely] |
| As [industry] continues to evolve | See above | [cut — start with what's actually happening] |

**Formulaic closers (equally telling as openers):**

| Phrase | Why flagged | Use instead |
|--------|------------|-------------|
| I hope this helps! | Template closer | [end with your actual closing thought] |
| Let me know if you need anything else! | Performative availability | [specific offer or nothing] |
| Feel free to reach out! | See above | [specific next step or nothing] |
| Don't hesitate to ask! | See above | [cut — they'll ask if they need to] |
| Is there anything else I can help with? | AI chatbot closer | [not appropriate in written documents] |

---

## Context-Dependent Words

These are legitimate in their home domain. Flag them elsewhere.

| Word | Home domain | Why it's fine there |
|------|------------|-------------------|
| leverage | Finance | Actual financial lever/ratio |
| robust | Engineering, statistics | Technical precision term |
| comprehensive | Research methodology | Describes scope of study |
| implement | Software engineering | Specific technical meaning |
| subsequently | Legal, academic | Precision temporal ordering |
| facilitate | Governance, education | Formal process term |
| stakeholder | Project management | Specific role definition |
| scalable | Engineering | Technical architecture term |
| granular | Data science | Describes data resolution |
| actionable | Business intelligence | Describes data usability |

---

## Watch List (Flag in Clusters)

Individual use is fine. Three or more in a short passage signals AI:

**Intensity words:** significantly, substantial, considerable, extensive, tremendous, immense
**Certainty hedges:** typically, generally, often, tends to, in many cases
**Pseudo-precision:** a wide range of, various, numerous, a variety of, multiple
**Empty connectors:** in terms of, with regard to, in the context of, as it relates to
**Performative urgency:** critical, crucial, vital, essential, imperative (when clustered)

---

## Punctuation Patterns to Flag

### Em Dash Overuse
- More than 2-3 em dashes per page (250 words)
- Em dashes used for semantic bridging in every paragraph
- Replace most with commas, parentheses, periods, or restructured sentences

### Excessive Colons
- Colons used to introduce "ta-da" moments rather than actual lists
- "The answer: [dramatic reveal]" pattern

### Over-Structured Formatting
- Bullet points where prose would be more natural
- Excessive bold text for emphasis
- Tables for information better explained in narrative
- Numbered lists for non-sequential content
