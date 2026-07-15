# Surface Audit Checklist

```text
source:
  skill: SKILL.md
  references: references/
  ui: agents/openai.yaml

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
