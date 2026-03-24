# Capabilities and Actions Reference — GPT Creator

Detailed guidance for Step 8 (Capabilities and Actions) and the Handling Special Cases
section of the GPT creation workflow.

---

## Capability Configuration by Source Focus Level

- **Knowledge-Only GPTs:** Disable Web Search. Enable Code Interpreter only if the GPT
  needs to process data from uploaded files.
- **Knowledge-First GPTs:** Disable Web Search by default. Enable only if explicitly
  needed for supplementary information.
- **Balanced/Training-Primary GPTs:** Enable Web Search if current information matters.

## Actions Setup

Actions require an OpenAPI schema (JSON format, version 3.1.0) defining the API
endpoints. For each Action, capture:
- What service it connects to
- What operations it needs (read, write, or both)
- Authentication type (none, API key, or OAuth)
- Whether the operation is consequential (requires user confirmation before executing)

**Security warning:** If the GPT has both Actions (external API access) and access to
sensitive knowledge files, warn about the "lethal trifecta" — an AI with access to
private data that also processes untrusted input and can send data externally.

Mitigations:
- Use the `x-openai-isConsequential: true` flag on write operations to require user confirmation
- Limit Action scopes to the minimum necessary operations
- Include explicit instruction protection in the Constraints section
- Consider separating sensitive knowledge into a different GPT that doesn't have Actions
- OWASP ranks prompt injection as the #1 security risk for LLM applications (2025)

---

## Special Cases

### User asks about memory across sessions
Custom GPTs do not retain context from previous sessions — each interaction is
stateless, regardless of whether the user has memory turned on in their ChatGPT
settings. The Memory Card workaround (a plain text file in the knowledge base updated
after each session with a structured summary) is the best no-code approach. See
`references/best-practices.md` for the full pattern.

Separately: Custom GPTs can be @mentioned inside ChatGPT Projects, and Projects do
have cross-session memory for the project context. If the user needs continuity, the
Projects + GPT @mention combination may serve them better than the Memory Card approach
alone.

### User asks about sharing and publishing
Custom GPTs can be shared three ways: private (only the creator), link-only (anyone
with the URL), or public (listed in the GPT Store). For team use on Team/Enterprise
plans, GPTs can be published to an internal workspace directory. Public GPTs are subject
to OpenAI's usage policies. Each user's interactions with a shared GPT are independent.

### User is near the 8,000-character instruction limit
Help identify content that belongs in a knowledge file rather than the instructions.
Reference material, long examples, and detailed reference tables should always live in
knowledge files. Instructions should contain behavior rules, workflow steps, and format
directives — not reference content.

### User asks about instruction confidentiality
By default, GPTs will not reveal uploaded file names. If the user wants to protect the
instruction text itself from being extracted, include the deflection prompt pattern from
`references/best-practices.md` in the Constraints section.

### User asks about capabilities (Web Search, DALL-E, Code Interpreter, Canvas)
These are enabled/disabled per-GPT in the Configure tab under Capabilities. Recommend:
- Enable Web Search only if the GPT needs current information beyond its knowledge files
- Enable Code Interpreter if the GPT needs to run calculations, process data, or generate charts
- Enable DALL-E only if image generation is part of the GPT's purpose
- Disable all unused capabilities to reduce scope creep and off-topic behavior

### User is building a GPT with Actions and sensitive knowledge files
See the Actions Setup section above for the security warning and mitigations.
