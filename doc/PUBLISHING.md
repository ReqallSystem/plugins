# Publishing Reqall Plugins

## Version Checklist

Before publishing any plugin, ensure versions and catalog metadata are consistent across the files that declare or expose them:

| File | Purpose |
|------|---------|
| `package.json` -> `version` | npm registry version |
| `.claude-plugin/plugin.json` -> `version` | Claude Code plugin version, for `claude-plugin` |
| `.codex-plugin/plugin.json` -> `version` | Codex plugin version, for `codex-plugin` |
| `.claude-plugin/marketplace.json` | Claude Code marketplace listing |
| `.agents/plugins/marketplace.json` | Codex marketplace listing |
| `agent-marketplace.json` | Vendor-neutral agent catalog |

Bump package and plugin manifest versions together. When a plugin repo moves, update the corresponding marketplace source URL in this aggregate repo.

---

## @reqall/core

Shared library used by claude-plugin and cursor-plugin.

```bash
cd core
npm run build
npm publish --access public
```

Publish core first; other packages depend on it.

---

## @reqall/auth

```bash
cd auth
npm run build
npm publish --access public
```

---

## @reqall/claude-plugin

```bash
cd claude-plugin

# 1. Bump versions in BOTH files:
#    - package.json
#    - .claude-plugin/plugin.json

# 2. Build
npm run build

# 3. Verify contents
npm pack --dry-run

# 4. Publish to npm
npm publish --access public

# 5. Push to GitHub; the Claude marketplace reads from the git repo
git add -A && git commit -m "v<VERSION>" && git push
```

---

## @reqall/cursor-plugin

```bash
cd cursor-plugin

# 1. Bump version in package.json

# 2. Build
npm run build

# 3. Publish to npm
npm publish --access public

# 4. Push to GitHub
git add -A && git commit -m "v<VERSION>" && git push
```

Note: Uses `@reqall/core: "^2026.2.1"` from npm, not a `file:` reference. If core has breaking changes, update the version range and test first.

---

## @reqall/copilot-plugin

No build step; static config files only.

```bash
cd copilot-plugin

# 1. Bump version in package.json

# 2. Publish to npm
npm publish --access public

# 3. Push to GitHub
git add -A && git commit -m "v<VERSION>" && git push
```

---

## @reqall/codex-plugin

No build step; static Codex plugin files and scripts only.

```bash
cd codex-plugin

# 1. Bump versions in BOTH files:
#    - package.json
#    - .codex-plugin/plugin.json

# 2. Verify contents
npm pack --dry-run

# 3. Publish to npm
npm publish --access public

# 4. Push to GitHub
git add -A && git commit -m "v<VERSION>" && git push
```

After publishing, confirm this aggregate marketplace repo still points to `https://github.com/ReqallSystem/codex-plugin.git`.

---

## @reqall/gemini-plugin

No build step; static config files only.

```bash
cd gemini-plugin

# 1. Bump version in package.json

# 2. Publish to npm
npm publish --access public

# 3. Push to GitHub
git add -A && git commit -m "v<VERSION>" && git push
```

---

## plugins (marketplace aggregate)

This repo defines three catalog surfaces:

| Surface | File | Notes |
|---------|------|-------|
| Claude Code | `.claude-plugin/marketplace.json` | Existing URL-based Claude marketplace; keep this compatible with Claude Code. |
| OpenAI Codex | `.agents/plugins/marketplace.json` | Codex marketplace metadata; entry must point to `https://github.com/ReqallSystem/codex-plugin.git`. |
| Other agents | `agent-marketplace.json` | Vendor-neutral discovery catalog with repositories, packages, and shared MCP/auth metadata. |

```bash
cd plugins

# Update marketplace files if plugin descriptions or sources changed.

git add -A && git commit -m "update marketplace listing" && git push
```

The marketplace ecosystem lists Claude Code, OpenAI Codex, Cursor, GitHub Copilot, and Google Gemini integrations.

---

## Current Versions (local checkout on 2026-06-13)

| Package | package.json | plugin.json |
|---------|-------------|-------------|
| @reqall/core | 2026.3.1 | N/A |
| @reqall/auth | 2026.3.1 | N/A |
| @reqall/claude-plugin | 2026.4.1 | 2026.3.30 |
| @reqall/cursor-plugin | 2026.2.1 | N/A |
| @reqall/copilot-plugin | 2026.2.1 | N/A |
| @reqall/codex-plugin | 2026.4.2 | 2026.4.1 in `../codex-plugin` |
| @reqall/gemini-plugin | 2026.2.1 | N/A |

The Claude package and Claude plugin manifest versions in the local sibling checkout are not currently aligned; sync them before the next Claude plugin publish.
