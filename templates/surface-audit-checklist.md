# Surface Audit Checklist

```text
source:
  skill: SKILL.md
  references: references/
  ui: agents/openai.yaml

host:
  product: <Codex/Claude Code/Claude Chat/Cowork/Harness/Cursor/Gemini/OpenCode/Copilot/MiMo>
  surface: <desktop/CLI/IDE/web/mobile/remote>
  version: <actual installed version>
  executionEnvironment: <local/SSH/cloud/VM>
  modelProvider: <independent from host capabilities>
  activationEvidence: <discovered/hook executed/skill actually read>

plugin:
  manifest: <path>
  version: <semver>
  skillsPath: <relative path>
  hooksPath: <relative path/none>
  hookTrust: <trusted/pending/disabled/managed-only>
  hookEvents: <event/count>
  contextInjection: <count/last event/last kind/last reasons>
  statePrivacy: <fingerprints and metadata only/violation>
  undeclaredRuntime: <MCP/apps/assets>
  harnessBundle: <dsh.bundle/none>
  projectInstructions: <native instruction path/none>

marketplace:
  root: <path>
  sourcePath: <./relative path>
  policy: <installation/authentication/category>

validation:
  source: <commands/results>
  package: <commands/results>
  duplicateInstalls: <none/paths>
  restartRequired: <yes/no>
```
