# Reqall Plugins

Marketplace aggregate and ecosystem overview for [Reqall](https://reqall.net), persistent semantic memory for AI coding agents.

## Marketplaces

### Claude Code

Claude Code compatibility is retained through the existing `.claude-plugin/marketplace.json` file. Install with:

```text
/plugin marketplace add ReqallSystem/plugins
/plugin install reqall@reqall-plugins
```

### OpenAI Codex

Codex marketplace metadata is provided through `.agents/plugins/marketplace.json`. The entry references the actual Codex plugin repo at `https://github.com/ReqallSystem/codex-plugin.git`, which contains the Codex manifest, lifecycle hooks, MCP/app config, skills, guardrail scripts, and agent policy docs.

Install the marketplace and plugin from Codex CLI:

```text
codex plugin marketplace add ReqallSystem/plugins
codex plugin add reqall@reqall-plugins
```

The plugin's lifecycle hooks require Node.js 20 or newer on `PATH`. Review and trust the bundled hooks with `/hooks`, authorize the bundled Reqall app when prompted, and start a new thread so Codex loads the installed skills and tools. Native MCP OAuth is the preferred authentication path. If Node.js is unavailable, use the standalone MCP connection instead:

```text
codex mcp add reqall --url https://www.reqall.net/mcp
codex mcp login reqall
```

An API key remains available as a fallback through the `REQALL_API_KEY` environment variable; do not place the token directly in Codex configuration:

```text
codex mcp add reqall --url https://www.reqall.net/mcp --bearer-token-env-var REQALL_API_KEY
```

For local development, keep a sibling checkout at `../codex-plugin`; the marketplace itself should continue to link the GitHub source repo.

### Grok Build

Grok Build marketplace metadata lives in `.grok-plugin/marketplace.json`. Install with:

```text
grok plugin marketplace add ReqallSystem/plugins
grok plugin install reqall --trust
```

`--trust` is required so plugin hooks and the Reqall MCP server activate.

### Grok Bot

Grok Bot (Cursor's desktop assistant) is a separate harness from Grok Build. Discover it via `agent-marketplace.json` (`reqall-grok-bot`). There is no Grok Bot marketplace schema in this repo, and this plugin must **not** be added to `.grok-plugin/marketplace.json` (Grok Build only).

Source: [grok-bot-plugin](https://github.com/ReqallSystem/grok-bot-plugin). Do not install [grok-plugin](https://github.com/ReqallSystem/grok-plugin) or run `grok plugin marketplace add` / `grok plugin install` for Grok Bot.

The package is skills + hosted MCP + `AGENTS.md`. Grok Bot has no hook runtime.

Preferred auth is native MCP OAuth to `https://www.reqall.net/mcp`. In Grok Bot, add that URL from **Plugins** or **Customize → MCPs** and finish the Authorize card. Cursor redirect URIs were registered on the Reqall MCP OAuth client as of 2026-08-28.

Fallback: API key or a token from `reqall login`, stored as `REQALL_API_KEY` (never in chat or committed config).

Local plugin install:

```bash
git clone https://github.com/ReqallSystem/grok-bot-plugin.git
mkdir -p ~/.cursor/plugins/local
ln -sfn "$PWD/grok-bot-plugin" ~/.cursor/plugins/local/reqall
```

Reload the window. Copy or merge `AGENTS.md` into the project root so context-before-work and persist-before-done stay on. For a project-only skill install without the plugin folder:

```bash
mkdir -p .cursor/skills
cp -R /path/to/grok-bot-plugin/skills/* .cursor/skills/
```

### Hermes Agent

Hermes has no third-party marketplace schema in this repo. Discover the plugin via `agent-marketplace.json` (`reqall-hermes`) and install from git into the **current** `$HERMES_HOME`:

```bash
hermes plugins install ReqallSystem/hermes-plugin --enable
python3 "$(hermes plugins path reqall 2>/dev/null || echo ~/.hermes/plugins/reqall)/ensure-install.py"
```

Named profiles are separate homes. Enabling `reqall` in a profile `config.yaml` does **not** copy plugin files. After `ensure-install.py`, restart **that** profile's gateway from an external shell and `/new`.

Secrets: `REQALL_API_KEY` or `MCP_REQALL_API_KEY` in the profile `.env`. Optional host MCP:

```yaml
mcp_servers:
  reqall:
    url: https://www.reqall.net/mcp
    headers:
      Authorization: Bearer ${REQALL_API_KEY}
```

### Cline

Cline CLI / Kanban load the SDK plugin; the VS Code and JetBrains extensions use file hooks:

```text
cline plugin install npm:@reqall/cline-plugin     # CLI
npx @reqall/cline-plugin install                  # VS Code / JetBrains: hooks, skills, rule
npx @reqall/cline-plugin mcp-config               # MCP entry for cline_mcp_settings.json
```

Source: [cline_plugin](https://github.com/ReqallSystem/cline_plugin).

### OpenCode

```text
opencode plugin @reqall/opencode-plugin -g
```

The plugin adds the `reqall` MCP server, skills, commands and instructions through OpenCode's
`config` hook. Source: [opencode_plugin](https://github.com/ReqallSystem/opencode_plugin).

### OpenClaw

```text
openclaw plugins install npm:@reqall/openclaw-plugin --accept-capabilities
openclaw config set plugins.entries.reqall.hooks.allowConversationAccess true
openclaw mcp login reqall
```

Native plugin; it does not claim the `memory` slot. Source: [openclaw_plugin](https://github.com/ReqallSystem/openclaw_plugin).

### Other Agents

`agent-marketplace.json` is a vendor-neutral catalog for agentic systems that want to discover the Reqall ecosystem without depending on the Claude, Codex, or Grok marketplace schemas. It lists the supported agents, source repositories, npm package names, and shared Reqall MCP/auth requirements.

## Plugin Ecosystem

| Package | Platform | Description |
|---------|----------|-------------|
| [@reqall/claude-plugin](https://github.com/ReqallSystem/claude-plugin) | Claude Code | Hooks, skills, and MCP integration |
| [@reqall/codex-plugin](https://github.com/ReqallSystem/codex-plugin) | OpenAI Codex | Lifecycle hooks, skills, MCP/app config, and memory guardrails |
| [@reqall/grok-plugin](https://github.com/ReqallSystem/grok-plugin) | Grok Build | Skills, hooks, and MCP integration |
| [grok-bot-plugin](https://github.com/ReqallSystem/grok-bot-plugin) | Grok Bot | Skills, hosted MCP, and AGENTS.md (no hook runtime) |
| [@reqall/cursor-plugin](https://github.com/ReqallSystem/cursor-plugin) | Cursor | Rules-based integration |
| [@reqall/copilot-plugin](https://github.com/ReqallSystem/copilot-plugin) | GitHub Copilot | VS Code configuration |
| [@reqall/gemini-plugin](https://github.com/ReqallSystem/gemini-plugin) | Google Gemini | Extension manifest and commands |
| [hermes-plugin](https://github.com/ReqallSystem/hermes-plugin) | Hermes Agent | Python hooks, skills, plugin HTTP tool, optional host MCP |
| [@reqall/cline-plugin](https://github.com/ReqallSystem/cline_plugin) | Cline | SDK plugin (CLI), VS Code file hooks, skills, MCP config |
| [@reqall/opencode-plugin](https://github.com/ReqallSystem/opencode_plugin) | OpenCode | Server plugin: MCP, skills, commands, recall and persist hooks |
| [@reqall/openclaw-plugin](https://github.com/ReqallSystem/openclaw_plugin) | OpenClaw | Native plugin: recall, finalize persist pass, skills, MCP |

### Supporting Packages

| Package | Purpose |
|---------|---------|
| [@reqall/core](https://github.com/ReqallSystem/core) | Shared TypeScript library (project detection, classification, config) |
| [@reqall/auth](https://github.com/ReqallSystem/auth) | CLI authentication (`reqall-auth`) |

All plugins connect to the Reqall MCP server at `https://www.reqall.net/mcp`. Use native OAuth where the host supports it; `REQALL_API_KEY` is the fallback for hosts without a compatible OAuth flow.

## Project naming

All agent integrations follow the [project naming contract](doc/PROJECT_NAMING.md):
explicit override, Git origin, labelled selection, portable project metadata,
package identity, workspace-relative path, then reserved machine memory. Reuse
host-provided bindings; never invent a project from a directory basename.
See the contract for compatibility rules and cross-repository conformance checks.

## SLEEP guidance checks

Claude, Codex, Hermes, Grok Build, Grok Bot, Pi, Cline, OpenCode and OpenClaw ship SLEEP skills. Their WORK
review policy follows [the canonical SLEEP documentation](https://github.com/fingerskier/reqall_net/blob/main/doc/SLEEP.md):
compare with intent and existing knowledge, preserve new evidence even when work
aligns, and discard only when no unique durable information remains.

With those nine repositories and `reqall_net` checked out beside this repository,
run `python -B -m unittest discover -s test -p 'test_sleep_guidance.py' -v`.
The offline checks cover instruction parity, judgment examples and Claude's tool
allowlist; they do not evaluate model judgment or perform live SLEEP mutations.
Keep host-specific routing, registration and package tests in each plugin.

## Publishing

See [doc/PUBLISHING.md](doc/PUBLISHING.md) for version management and release workflow.
