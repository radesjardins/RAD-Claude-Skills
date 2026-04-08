# Technical Writing Reference

## What Good Technical Writing Looks Like

### The Diataxis Framework
Technical documentation falls into four distinct types. Each serves a different need and follows different rules. Mixing them is the most common source of bad docs.

#### Tutorials (Learning-Oriented)
**Purpose:** Guide the learner through a series of steps to complete a project. The goal is a successful experience, not comprehensive understanding.

**Do this:**
- Hold the reader's hand. Every step is explicit.
- Include the expected output at each step so the reader can verify they're on track.
- Minimize explanation — just enough to keep moving. Save deep dives for Explanation docs.
- Use a real, meaningful project (not "Hello World" if you can avoid it).
- State prerequisites up front: "This tutorial assumes you have Node.js 18+ and a GitHub account."
- Number every step. Don't use bullets for sequential actions.

**Not that:**
- "You could also use X or Y..." (Options create confusion in tutorials. Make the choice for the reader.)
- "For more on this concept, see..." (Don't send them away mid-tutorial.)
- Long conceptual paragraphs between steps. (Save it for Explanation.)
- Leaving environment setup as "an exercise for the reader."

#### How-To Guides (Problem-Oriented)
**Purpose:** Help someone accomplish a specific task. The reader already knows what they want to do — they need the steps.

**Do this:**
- Title it as a task: "How to configure CORS" not "CORS Configuration"
- Assume the reader has basic competence. Don't re-explain fundamentals.
- Focus on the goal, not the concepts behind it.
- Include common variations: "If you're using Docker, instead do X."
- End when the task is complete. No reflective summary needed.

**Not that:**
- Mixing tutorial hand-holding into a how-to. (The reader is experienced; don't over-explain.)
- Starting with three paragraphs of context before the first step.
- Omitting error states. What happens if step 3 fails?

#### Reference (Information-Oriented)
**Purpose:** Describe the machinery — APIs, configuration options, CLI flags, schemas. The reader consults it, not reads it.

**Do this:**
- Be exhaustive and consistent. Every endpoint, every parameter, every option.
- Use tables for parameter lists: name, type, required/optional, default, description.
- One entry per concept. Don't combine two API endpoints in one section.
- Include type information, constraints, and edge cases.
- Make it scannable: alphabetical order, consistent formatting, deep linking.

**Not that:**
- Narrative explanations in a reference. (Save those for Explanation.)
- Incomplete parameter lists. If a function takes 8 options, document all 8.
- Examples without showing the response/output.
- Mixing "what it does" with "how to use it."

#### Explanation (Understanding-Oriented)
**Purpose:** Help the reader understand why things work the way they do. Provides context, rationale, and mental models.

**Do this:**
- Discuss alternatives and tradeoffs: "We chose X over Y because..."
- Connect concepts to each other. Show how the pieces fit together.
- Use analogies and diagrams.
- Address the "why" questions that the other three types deliberately skip.
- It's OK to be opinionated here. Explain design decisions.

**Not that:**
- Step-by-step instructions in an explanation doc. (That's a tutorial or how-to.)
- A wall of text with no visual breaks or headers.
- "This is left as an exercise for the reader." (Explanations should actually explain.)

### README Patterns for Adoption

A README has about 30 seconds to convince a developer to keep reading. Structure it for scanning, not studying.

**Optimal README structure:**
1. **Title + one-line description.** What is this thing?
2. **Badges.** Build status, version, license — social proof and currency signals.
3. **The "why" paragraph.** Two to three sentences: what problem does this solve, and why is this solution better than alternatives?
4. **Quick start.** The fewest possible steps from `npm install` to "it works." Three commands or fewer.
5. **Usage example.** A realistic code snippet showing the most common use case. Not a contrived toy example.
6. **API / Configuration.** Link to full docs or include a summary table.
7. **Contributing.** How to set up the dev environment, run tests, submit PRs.
8. **License.**

**Do this:** Put a working code example in the first scroll of the README.

**Not that:** Start with a mission statement, philosophy section, and the project's origin story before showing any code.

### Step-by-Step Instruction Writing

#### The Copy-Paste Test
Every code snippet in a tutorial or how-to should work when copied and pasted. Test this literally. Don't include shell prompts (`$`) in copyable commands. Don't include output mixed into the command block.

**Do this:**
```bash
npm install @acme/widget
```

**Not that:**
```bash
$ npm install @acme/widget
npm added 47 packages in 2.1s
```

The `$` and the output are not part of the command. The reader has to manually remove them.

#### One Action Per Step
Each numbered step should contain exactly one action. If a step says "Create the file and add the following configuration," split it into two steps: "Create the file" and "Add the following configuration."

#### Show Expected Results
After significant steps, show what the reader should see. This is their checkpoint. State expected outcomes explicitly: "Hit Enter. Terminal should display 'Build Complete.'" This prevents silent failures — where the step appears to succeed but actually didn't, and the reader only discovers the problem five steps later.

**Do this:**
"Step 3: Start the server.
```bash
npm run dev
```
You should see:
```
Server running at http://localhost:3000
```
"

**Not that:** "Start the server." (The reader starts it, sees an error, and doesn't know if it's expected or not.)

#### Name the File
When showing code that goes in a file, always say which file.

**Do this:** "Add the following to `src/config.ts`:"

**Not that:** "Add the following configuration:" (Where? Which file? New file or existing?)

### API Documentation Best Practices

#### The "Time to First Call" Metric
The single most important metric for API documentation is "time to first call" — how quickly can a developer make their first successful API call? Every design decision in API docs should reduce this number. If a developer can't go from zero to a working request in under 5 minutes, the docs have failed their primary job.

#### Why Stripe's Docs Are Great
Stripe's API docs are the gold standard because they follow consistent patterns:

1. **Three-Pane Layout:** Navigation on the left, descriptions in the middle, code snippets on the right. The reader can scan structure, read explanation, and copy code without scrolling between contexts.
2. **Every endpoint has a runnable example.** Not a theoretical one — a curl command you can copy and run with your API key.
3. **Interactive Sandboxes:** Allow live API calls with pre-filled sample data. The reader experiments without setting up an environment.
4. **Request and response are shown side by side.** You see what you send and what you get back.
5. **Parameters are exhaustively documented** in a consistent table format with types, defaults, and descriptions.
6. **Error responses are documented** as thoroughly as success responses. What goes wrong, and what the error codes mean.
7. **Language-specific examples** in the reader's preferred language, switchable with a tab.
8. **Progressive disclosure.** The simple case is shown first. Advanced parameters and edge cases are expandable or in a separate section.
9. **Human-Readable Object IDs:** Prefixed strings like `cus_123`, `inv_456`, `sub_789` provide instant debugging context. When you see `cus_` in a log, you know it's a customer without looking it up.

#### API Doc Structure Per Endpoint
```
## Endpoint Name
Brief description of what this endpoint does.

### Request
Method + URL
Headers (especially auth)
Path parameters
Query parameters (table: name, type, required, description)
Body parameters (table: name, type, required, description)

### Response
Status code
Response body (annotated JSON with descriptions)

### Errors
Table of possible error codes with descriptions and resolution steps

### Example
Complete request + response example
```

### Code Examples in Documentation

#### The "Single Concept" Rule
Each code snippet should demonstrate one function, one concept, one technique. When a snippet tries to show initialization, configuration, error handling, and a real API call all at once, the reader can't tell which part solves their problem. Break compound examples into focused, sequential snippets.

#### Replace Abstract Placeholders
Use specific, human-readable values instead of abstract placeholders. "Alice sends 50 USD to Bob" is immediately understandable. "User A sends Token X to User B" forces the reader to mentally substitute real values at every step. Concrete examples reduce cognitive load and make edge cases visible.

#### Make Examples Realistic
The example should look like code someone would actually write. Not `foo`, `bar`, `baz`. Not `MyClass`. Use domain-appropriate names.

**Do this:**
```typescript
const user = await db.users.findById(userId);
if (!user) {
  throw new NotFoundError(`User ${userId} not found`);
}
```

**Not that:**
```typescript
const x = await db.things.findById(id);
if (!x) {
  throw new Error("not found");
}
```

#### Show Complete, Runnable Examples
Don't show a code snippet that requires 15 unstated imports to run. Either show the imports or state them explicitly.

**Do this:**
```typescript
import { createClient } from '@acme/sdk';

const client = createClient({ apiKey: process.env.ACME_API_KEY });
const result = await client.users.list({ limit: 10 });
```

**Not that:**
```typescript
const result = await client.users.list({ limit: 10 });
```
(Where does `client` come from? How was it initialized?)

#### Annotate, Don't Over-Comment
Comments in code examples should explain "why," not "what." The reader can read the code. Use self-documenting variable names so the code explains itself; reserve comments for non-intuitive logic, workarounds, and business rules.

**Do this:**
```typescript
// Retry with exponential backoff because the rate limit resets every 60s
const result = await retry(() => client.send(payload), { maxRetries: 3 });
```

**Not that:**
```typescript
// Call the retry function with the client send method
const result = await retry(() => client.send(payload), { maxRetries: 3 });
```

#### Automated Code Validation
Tie code snippets to your CI/CD pipeline. Extract examples into a test suite that runs on every build. Broken examples in published docs destroy developer trust faster than any other documentation failure. If the docs say it works, it must work — today, not when the docs were written.

### Progressive Disclosure
Structure documentation so the reader encounters simple concepts first and complex ones later. Don't front-load every caveat, edge case, and advanced option.

**Levels of disclosure:**
1. **Quick start:** The minimum to get running. Five steps or fewer.
2. **Common usage:** The 80% use case. Configuration options most people need.
3. **Advanced usage:** Edge cases, performance tuning, custom extensions.
4. **Internals / Architecture:** How it works under the hood. For contributors and power users.

Each level should be reachable but not required. A reader who only needs the quick start should never have to scroll past the architecture docs.

#### Types of Progressive Disclosure
- **Staged progressive disclosure:** Complex forms or workflows broken into sequential screens. Each screen handles one decision before moving to the next. Prevents the "wall of options" problem.
- **Contextual progressive disclosure:** Advanced options hidden until conditions are met or the user explicitly requests them. A "Show advanced settings" toggle, or fields that appear only when a related option is selected.

### Visual Aids
- **Diagrams** for architecture, data flow, and system interactions. Use simple boxes-and-arrows. Tools: Mermaid (in Markdown), Excalidraw (for hand-drawn style), draw.io.
- **Screenshots** for UI documentation. Annotate with numbered callouts, not just red circles.
- **Tables** for parameter lists, feature comparisons, and option matrices. Always better than a bulleted list of key-value pairs.
- **Admonitions/Callouts** for warnings, tips, and gotchas. Use consistently: NOTE for helpful context, WARNING for things that can break, TIP for efficiency improvements.

### Tone in Technical Writing

#### Confident Without Arrogant
State things directly. Don't hedge with "you might want to consider potentially using."

**Do this:** "Use environment variables for secrets. Never commit API keys to source control."

**Not that:** "You may want to consider using environment variables, as it is generally considered a best practice to avoid committing sensitive values."

#### Friendly Without Patronizing
Address the reader as a competent adult. Don't use exclamation points to manufacture enthusiasm. Don't say "simply" or "just" before something that isn't simple.

**Do this:** "Configure the database connection string in your `.env` file."

**Not that:** "Simply add your database connection string to the `.env` file and you're all set!"

The word "simply" is patronizing when the reader has been debugging this for an hour. "Just" implies the task is trivial — if it were, they wouldn't be reading the docs.

**Words to avoid in technical docs:**
- "Simply" / "Just" / "Easily" (minimizes difficulty)
- "Obviously" / "Clearly" (if it were obvious, they wouldn't need docs)
- "Please" (docs are instructions, not requests)
- "Note that" (overused; use an admonition callout instead)

### Maintenance and Versioning

#### Version Your Docs With Your Code
Documentation should be versioned alongside the software it describes. When v3 ships, the v2 docs should still be accessible.

**Do this:** Version selector in the docs site. Clear labels on which version a page describes.

**Not that:** One set of docs that gets overwritten with each release. Users on v2 can't find the v2 instructions.

#### Date and Deprecation
- Mark deprecated features clearly with the version they'll be removed in.
- Date "last updated" on pages that describe rapidly changing features.
- When an API changes, keep the old docs available with a banner: "This describes v1. For v2, see [link]."

#### The Freshness Problem
The biggest threat to documentation quality is staleness. A doc that was accurate two releases ago is worse than no doc — it actively misleads.

**Mitigations:**
- Automated testing of code examples (doctest, code snippet extraction into test suites)
- Documentation review as part of the PR process (did the PR change behavior? Update the docs.)
- Quarterly doc audits: read every page and flag anything that feels stale
- "Report a problem" links on every page to crowdsource staleness detection

## Common Mistakes

1. **Mixing Diataxis types.** A tutorial that stops to explain architecture. A reference page that tries to teach concepts. A how-to that starts from zero. Keep the types pure.
2. **Assuming context.** The reader doesn't know what you know. Spell out prerequisites, environment requirements, and assumed knowledge.
3. **Untested code examples.** The snippet looked right when you wrote it. It doesn't compile. Test every example.
4. **Over-documenting the obvious, under-documenting the subtle.** Five paragraphs on how to install Node.js. No mention of the CORS gotcha that trips up every new user.
5. **Wall-of-text syndrome.** No headers, no code blocks, no visual breaks. Technical docs should be scannable, not read like a novel.
6. **Documentation as afterthought.** Written once when the feature shipped, never updated. By v3, the docs describe v1 behavior.
7. **Passive voice.** "The configuration file should be updated." By whom? "Update the configuration file." Active, direct, clear.
8. **Burying the lede.** Three paragraphs of philosophy before "To install: `npm install thing`."
9. **No error documentation.** Happy path only. Real users hit errors. Document them.
10. **Dead links.** Links to pages that have moved or been deleted. Check links regularly.

## Context-Gathering Questions

Before writing technical documentation, clarify:

1. **Which Diataxis type is this?** Tutorial, how-to, reference, or explanation? Don't mix.
2. **Who is the reader?** Beginner developer? Experienced engineer evaluating the tool? Existing user looking up a specific parameter?
3. **What does the reader already know?** State prerequisites explicitly.
4. **What is the reader trying to accomplish?** (For tutorials and how-tos.) Define the end state.
5. **What version of the software?** Docs must be version-accurate.
6. **What languages/platforms does the reader use?** Show examples in their stack.
7. **What are the common failure modes?** Document errors, not just successes.
8. **Is there existing documentation to update, or is this net-new?** Avoid duplicating content.
9. **Where will this doc live?** README, docs site, wiki, inline code comments?
10. **What's the maintenance plan?** Who updates this when the software changes?

## Quality Criteria

- [ ] The doc type is clear (tutorial / how-to / reference / explanation) and doesn't mix types
- [ ] Prerequisites are stated explicitly at the top
- [ ] Every code example is tested, runnable, and copy-pasteable
- [ ] File paths and filenames are specified for every code snippet
- [ ] Steps are numbered (not bulleted) for sequential instructions
- [ ] Expected output is shown after significant steps
- [ ] Error states are documented, not just happy paths
- [ ] Headers create a scannable structure — the reader can find what they need without reading linearly
- [ ] No "simply," "just," "obviously," or other minimizing language
- [ ] Visual aids (diagrams, tables, callouts) are used where they improve comprehension
- [ ] Links work and point to current versions
- [ ] The doc answers the reader's question within the first two scrolls

## AI Pattern Considerations

AI-generated technical documentation tends to:

1. **Over-explain fundamentals.** AI gives three paragraphs on what environment variables are before showing how to set one. The reader of your API docs knows what environment variables are. Skip to the specific configuration.
2. **Generate plausible but untested code.** AI code examples look right but contain subtle errors — wrong method names, incorrect parameter orders, deprecated APIs. Every AI-generated code example must be run before publishing.
3. **Use placeholder values that don't work.** `your-api-key-here`, `https://api.example.com`, `YOUR_PROJECT_ID`. Replace these with realistic-looking (but clearly fake) values: `acme_test_abc123def456`, `https://api.acme.com/v2`.
4. **Default to happy-path only.** AI rarely documents error states, edge cases, or failure modes. Explicitly prompt for error documentation and unusual inputs.
5. **Mix Diataxis types.** AI will write a tutorial that stops for a three-paragraph explanation, then becomes a reference table, then returns to tutorial steps. Constrain it to one type.
6. **Write generic introductions.** "In today's fast-paced development world, testing is more important than ever." Delete the entire first paragraph. Start with the first useful sentence.
7. **Over-use admonitions.** NOTE. TIP. WARNING. NOTE. IMPORTANT. When everything is called out, nothing is called out. Reserve admonitions for genuinely critical information.
8. **Generate symmetrical structure.** Every section has exactly three subsections, each with exactly two code examples. Real documentation is shaped by the content — some features need extensive docs, others need two sentences.
9. **Use "let's" excessively.** "Let's create a new project. Let's add the dependency. Let's configure the database." This isn't a pair programming session. Use imperative: "Create a new project."
10. **Skip the "why."** AI shows what to do but not why you'd do it. "Add `retry: 3` to the config" is incomplete. "Add `retry: 3` to the config to handle transient network failures" gives the reader a reason.
11. **Invent API surfaces.** AI will hallucinate methods, parameters, and configuration options that don't exist. Cross-reference every API claim against the actual source code or published API reference.
12. **Write version-agnostic docs.** AI rarely specifies which version of a library or framework a doc applies to. Pin versions explicitly: "This guide uses Next.js 14.2 and React 18."
