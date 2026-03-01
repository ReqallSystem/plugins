# Publishing Reqall Plugins

## Version Checklist

Before publishing any plugin, ensure versions are consistent across all files that declare one:

| File | Purpose |
|------|---------|
| `package.json` → `version` | npm registry version |
| `.claude-plugin/plugin.json` → `version` | Claude Code marketplace version (claude-plugin only) |

Bump both files together.

---

## @reqall/core

Shared library used by claude-plugin and cursor-plugin.

```bash
cd core
npm run build
npm publish --access public
```

**Publish core first** other packages depend on it.

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
#    - package.json        → "version"
#    - .claude-plugin/plugin.json → "version"

# 2. Build
npm run build

# 3. Verify contents (check nothing is missing or extra)
npm pack --dry-run

# 4. Publish to npm
npm publish --access public

# 5. Push to GitHub (marketplace reads from the git repo)
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

**Note:** Uses `@reqall/core: "^0.0.3"` from npm (not file: reference).
If core has breaking changes, update the version range and test first.

---

## @reqall/copilot-plugin

No build step — static config files only.

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

No build step — static config files only.

```bash
cd codex-plugin

# 1. Bump version in package.json

# 2. Publish to npm
npm publish --access public

# 3. Push to GitHub
git add -A && git commit -m "v<VERSION>" && git push
```

---

## @reqall/gemini-plugin

No build step — static config files only.

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

This repo defines the Claude Code marketplace listing via `.claude-plugin/marketplace.json`.

```bash
cd plugins

# Update marketplace.json if plugin descriptions or sources changed

git add -A && git commit -m "update marketplace listing" && git push
```

The marketplace currently lists only the claude-plugin.
To add other plugins, add entries to the `plugins` array in `.claude-plugin/marketplace.json`.

---

## Current Versions (as of 2026-02-28)

| Package | package.json | npm latest | plugin.json |
|---------|-------------|------------|-------------|
| @reqall/core | — | 0.1.0 | — |
| @reqall/claude-plugin | 0.0.9 | 0.0.7 | 0.0.9 |
| @reqall/cursor-plugin | 0.0.3 | 0.0.3 | — |
| @reqall/copilot-plugin | 0.0.3 | 0.0.3 | — |
| @reqall/codex-plugin | 0.0.3 | 0.0.3 | — |
| @reqall/gemini-plugin | 0.0.3 | 0.0.3 | — |
