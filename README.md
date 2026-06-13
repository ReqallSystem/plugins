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

Codex marketplace metadata is provided through `.agents/plugins/marketplace.json`. The entry references the actual Codex plugin repo at `https://github.com/ReqallSystem/codex-plugin.git`, which contains the Codex manifest, MCP/app config, skills, guardrail script, and agent policy docs.

For local development, keep a sibling checkout at `../codex-plugin`; the marketplace itself should continue to link the GitHub source repo.

### Other Agents

`agent-marketplace.json` is a vendor-neutral catalog for agentic systems that want to discover the Reqall ecosystem without depending on the Claude or Codex marketplace schemas. It lists the supported agents, source repositories, npm package names, and shared Reqall MCP/auth requirements.

## Plugin Ecosystem

| Package | Platform | Description |
|---------|----------|-------------|
| [@reqall/claude-plugin](https://github.com/ReqallSystem/claude-plugin) | Claude Code | Hooks, skills, and MCP integration |
| [@reqall/codex-plugin](https://github.com/ReqallSystem/codex-plugin) | OpenAI Codex | Skills, MCP/app config, guardrail script, and agent policies |
| [@reqall/cursor-plugin](https://github.com/ReqallSystem/cursor-plugin) | Cursor | Rules-based integration |
| [@reqall/copilot-plugin](https://github.com/ReqallSystem/copilot-plugin) | GitHub Copilot | VS Code configuration |
| [@reqall/gemini-plugin](https://github.com/ReqallSystem/gemini-plugin) | Google Gemini | Extension manifest and commands |

### Supporting Packages

| Package | Purpose |
|---------|---------|
| [@reqall/core](https://github.com/ReqallSystem/core) | Shared TypeScript library (project detection, classification, config) |
| [@reqall/auth](https://github.com/ReqallSystem/auth) | CLI authentication (`reqall-auth`) |

All plugins connect to the Reqall MCP server at `https://www.reqall.net/mcp` and require a `REQALL_API_KEY`.

## Publishing

See [doc/PUBLISHING.md](doc/PUBLISHING.md) for version management and release workflow.
