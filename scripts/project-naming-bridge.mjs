// Read-only resolver bridge for check-project-naming.py. No live MCP requests.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const { workspace, cases, policiesOnly = false } = JSON.parse(fs.readFileSync(0, 'utf8'));
const load = async p => import(pathToFileURL(path.join(workspace, p)).href);
const policies = {
  core: await load('core/dist/project-policy.js'),
  claude: await load('claude-plugin/dist/src/hooks/project-policy.js'),
  codex: await load('codex-plugin/scripts/lib/project-policy.mjs'),
  grok: await load('grok-plugin/scripts/lib/project-policy.mjs'),
  pi: await load('pi-plugin/extensions/project-policy.ts'),
  cursor: await load('cursor-plugin/dist/project-policy.js'),
  cline: await load('cline_plugin/lib/project-policy.mjs'),
  opencode: await load('opencode_plugin/lib/project-policy.mjs'),
  openclaw: await load('openclaw_plugin/lib/project-policy.mjs'),
};
const publicResolvers = policiesOnly ? {} : {
  'core-public': async c => (await load('core/dist/detect-project.js')).detectProject(c.cwd, c.prompt),
  'codex-public': async c => (await load('codex-plugin/scripts/lib/project.mjs')).resolveProjectName(c.cwd, c.env, c.prompt),
  'grok-public': async c => (await load('grok-plugin/scripts/lib/project.mjs')).resolveProjectName(c.cwd, c.env, c.prompt),
  'claude-public': async c => {
    const common = await load('claude-plugin/dist/src/hooks/common.js');
    const session = `contract-${c.id}`;
    // Claude retains explicit user choices in session state. This is the same
    // state field its UserPromptSubmit hook sets; state lives in the temp tree.
    const hint = common.extractProjectHint(c.prompt);
    if (hint) common.updateState(session, state => { state.prompt_project = hint; });
    return common.projectName({ cwd: c.cwd, session_id: session, prompt: c.prompt });
  },
  'cursor-public': async c => (await load('cursor-plugin/dist/index.js')).detectProject(c.cwd, c.prompt),
};
const results = [];
for (const c of cases) {
  process.env = { ...c.env };
  for (const [host, policy] of Object.entries(policies)) {
    try {
      const binding = policy.resolveProjectBinding(c.cwd, c.use_default_env ? undefined : c.env, c.prompt);
      results.push({ host, id: c.id, ...binding });
    } catch (error) {
      results.push({ host, id: c.id, error: String(error) });
    }
  }
  for (const [host, resolve] of Object.entries(publicResolvers)) {
    try {
      results.push({ host, id: c.id, name: await resolve(c) });
    } catch (error) {
      results.push({ host, id: c.id, error: String(error) });
    }
  }
}
process.stdout.write(JSON.stringify(results));
