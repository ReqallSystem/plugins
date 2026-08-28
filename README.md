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

Grok Bot (Cursor’s desktop assistant) is **not** Grok Build. Do not run `grok plugin marketplace add`, `grok plugin install`, or edit `~/.grok/config.toml`. There is no Grok Bot marketplace schema in this aggregate; discover the plugin via `agent-marketplace.json` (`reqall-grok-bot`).

Preferred: native MCP OAuth. In Grok Bot, open **Plugins** (or **Customize → MCPs**), add `https://www.reqall.net/mcp`, and finish Authorize. The connector appears as `user-Reqall` when connected.

Optional local plugin (skills + `AGENTS.md` autopilot):

```bash
git clone https://github.com/ReqallSystem/grok-bot-plugin.git
ln -sfn "$PWD/grok-bot-plugin" ~/.cursor/plugins/local/reqall
```

Reload the window. API key Bearer or a token from `reqall login` is fallback only. On Teams / Enterprise, local plugin imports may be disabled by admin policy — use the MCP connector path instead.

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

### Other Agents

`agent-marketplace.json` is a vendor-neutral catalog for agentic systems that want to discover the Reqall ecosystem without depending on the Claude, Codex, or Grok marketplace schemas. It lists the supported agents, source repositories, npm package names, and shared Reqall MCP/auth requirements.

## Plugin Ecosystem

| Package | Platform | Description |
|---------|----------|-------------|
| [@reqall/claude-plugin](https://github.com/ReqallSystem/claude-plugin) | Claude Code | Hooks, skills, and MCP integration |
| [@reqall/codex-plugin](https://github.com/ReqallSystem/codex-plugin) | OpenAI Codex | Lifecycle hooks, skills, MCP/app config, and memory guardrails |
| [@reqall/grok-plugin](https://github.com/ReqallSystem/grok-plugin) | Grok Build | Skills, hooks, and MCP integration |
| [grok-bot-plugin](https://github.com/ReqallSystem/grok-bot-plugin) | Grok Bot | Skills, hosted MCP, and AGENTS.md autopilot (no hooks) |
| [@reqall/cursor-plugin](https://github.com/ReqallSystem/cursor-plugin) | Cursor | Rules-based integration |
| [@reqall/copilot-plugin](https://github.com/ReqallSystem/copilot-plugin) | GitHub Copilot | VS Code configuration |
| [@reqall/gemini-plugin](https://github.com/ReqallSystem/gemini-plugin) | Google Gemini | Extension manifest and commands |
| [hermes-plugin](https://github.com/ReqallSystem/hermes-plugin) | Hermes Agent | Python hooks, skills, plugin HTTP tool, optional host MCP |

### Supporting Packages

| Package | Purpose |
|---------|---------|
| [@reqall/core](https://github.com/ReqallSystem/core) | Shared TypeScript library (project detection, classification, config) |
| [@reqall/auth](https://github.com/ReqallSystem/auth) | CLI authentication (`reqall-auth`) |

All plugins connect to the Reqall MCP server at `https://www.reqall.net/mcp`. Use native OAuth where the host supports it; `REQALL_API_KEY` is the fallback for hosts without a compatible OAuth flow.

## Publishing

See [doc/PUBLISHING.md](doc/PUBLISHING.md) for version management and release workflow.
