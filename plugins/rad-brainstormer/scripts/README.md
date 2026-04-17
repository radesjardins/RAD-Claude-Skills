# Visual Companion Server

A local WebSocket-backed visual companion that the brainstormer skills (`brainstorm-session`, `design-sprint`) can open in a browser to show mockups, architecture diagrams, and side-by-side layout comparisons during interactive ideation.

## Files

| File | Purpose |
|------|---------|
| `server.js` | Stand-alone Node.js HTTP + WebSocket server (no npm dependencies — uses core modules only) |
| `helper.js` | Rendering / framing helper logic used by `server.js` |
| `frame-template.html` | The HTML shell rendered in the browser tab |
| `start-server.sh` | Launcher for bash / zsh / Git Bash |
| `stop-server.sh` | Shutdown helper |

## When Claude uses this

The brainstormer skills offer the visual companion only when the upcoming questions genuinely benefit from visuals:

- **Browser-appropriate:** mockups, wireframes, architecture diagrams, side-by-side option comparisons, layout options
- **Terminal-appropriate:** tradeoff lists, scope decisions, requirements questions, conceptual choices

The offer is a standalone message — Claude will not combine it with a question. If you accept, Claude decides *per question* whether to push the next view to the browser or keep the conversation in the terminal.

## How to run it manually

```bash
cd plugins/rad-brainstormer/scripts
./start-server.sh      # starts on a local port and prints the URL
# ... Claude pushes frames over WebSocket as the session progresses ...
./stop-server.sh       # when you're done
```

The server is entirely local — no outbound network calls, no dependencies beyond Node.js's built-in `http` / `crypto` / `fs` / `path` modules.

## When to skip it

The visual companion is strictly optional. If you are:

- running in `--non-interactive` mode (agent/CI caller)
- on a headless machine with no browser
- working through purely conceptual or text-oriented topics

just decline the offer — the skill falls back to a terminal-only flow with no degradation in brainstorming quality.

## Troubleshooting

- **Port in use** — edit the port constant in `server.js` or set the `PORT` env var before `start-server.sh`.
- **Browser tab doesn't connect** — check that the WebSocket upgrade path in your local network allows `ws://localhost`; corporate proxies sometimes intercept.
- **Server won't stop** — `stop-server.sh` sends SIGTERM; if the process is stuck, `ps` for the node PID and `kill -9`.

## License

Apache-2.0, same as the rest of the plugin.
