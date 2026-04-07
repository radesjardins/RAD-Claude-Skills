# RAD Brainstorm — Claude.ai Skills

Collaborative ideation using proven methodologies (SCAMPER, Six Hats, Reverse Brainstorming, Five Whys, and more), structured divergent/convergent phases, creative unblocking, idea evaluation, and design sprint. Adapted from the [rad-brainstormer plugin](../../plugins/rad-brainstormer/) for Claude.ai.

## Two Options

### Option A: Complete Suite (recommended)

One skill with everything. Import `dist/rad-brainstorm-complete.zip` via **Settings > Customize > Skills**.

Includes the full SKILL.md (facilitation, ideation techniques, evaluation frameworks, design sprint) plus 5 resource files (methodology catalog, evaluation frameworks, facilitation principles, creative unblocking, domain research guide).

### Option B: Modular Skills

Import only the phases you need. Each is a separate ZIP in `dist/`:

| ZIP File | What It Does | Use When You Want To... |
|----------|-------------|------------------------|
| `rad-brainstorm-ideate.zip` | Facilitated brainstorming + all divergent techniques | Generate ideas, get unblocked, explore options |
| `rad-brainstorm-evaluate.zip` | Evaluation frameworks + idea stress-testing | Prioritize, compare, and select from existing ideas |
| `rad-brainstorm-design.zip` | Design sprint for specs | Turn a chosen idea into a complete design document (software) |

Modular skills detect each other when multiple are imported and offer natural transitions (ideate → evaluate → design).

## How to Import

**As a Skill (recommended):** Go to **Settings > Customize > Skills** on Claude.ai. Upload the `.zip` file(s).

**As Project Knowledge:** Create a Claude.ai Project, add the `.md` file(s) directly as Project Knowledge.

**As a conversation attachment:** Attach the `.md` file to any conversation for one-off use.

## Example Prompts

### Brainstorming / Ideation
- "Let's brainstorm ideas for [topic]"
- "I'm stuck and don't know where to start"
- "Help me think through [problem]"
- "I need more options for [decision]"
- "What should I build?"

### Evaluation / Decision-Making
- "Help me evaluate these ideas"
- "Which of these options is best?"
- "Compare these approaches"
- "Run a pre-mortem on this idea"

### Design Sprint
- "Design this feature for me"
- "Create a spec for [idea]"
- "I've decided what to build — help me design it"
- "Write a design doc for [project]"

## How It Works

The brainstormer follows proven facilitation principles:

- **Anti-anchoring**: Draws out YOUR ideas first before offering its own (AI suggestions cause design fixation in humans)
- **Phase discipline**: Never mixes divergent thinking (generating ideas) with convergent thinking (evaluating ideas)
- **One question at a time**: Prevents cognitive overload — asks one focused question, waits for your answer
- **Domain-aware**: Can research unfamiliar domains via web search before brainstorming
- **Adaptive**: Detects when you're stuck and switches techniques; stays out of the way when you're in flow
- **Artifacts**: Produces idea boards, comparison tables, evaluation matrices, and design specs as downloadable artifacts
