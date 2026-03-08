# Reqall Plugins

Claude Code marketplace aggregate and ecosystem overview for [Reqall](https://reqall.net) — persistent semantic memory for AI coding agents.

## Marketplace

This repo defines the Claude Code marketplace listing via `.claude-plugin/marketplace.json`. Install with:

```
/plugin marketplace add ReqallSystem/plugins
/plugin install reqall@reqall-plugins
```

## Plugin Ecosystem

| Package | Platform | Description |
|---------|----------|-------------|
| [@reqall/claude-plugin](https://github.com/ReqallSystem/claude-plugin) | Claude Code | Hooks, skills, and MCP integration |
| [@reqall/cursor-plugin](https://github.com/ReqallSystem/cursor-plugin) | Cursor | Rules-based integration |
| [@reqall/copilot-plugin](https://github.com/ReqallSystem/copilot-plugin) | GitHub Copilot | VS Code configuration |
| [@reqall/codex-plugin](https://github.com/ReqallSystem/codex-plugin) | OpenAI Codex | Guardrail script and agent policies |
| [@reqall/gemini-plugin](https://github.com/ReqallSystem/gemini-plugin) | Google Gemini | Extension manifest and commands |

### Supporting Packages

| Package | Purpose |
|---------|---------|
| [@reqall/core](https://github.com/ReqallSystem/core) | Shared TypeScript library (project detection, classification, config) |
| [@reqall/auth](https://github.com/ReqallSystem/auth) | CLI authentication (`reqall-auth`) |

All plugins connect to the Reqall MCP server at `https://www.reqall.net/mcp` and require a `REQALL_API_KEY`.

## Publishing

See [doc/PUBLISHING.md](doc/PUBLISHING.md) for version management and release workflow.
