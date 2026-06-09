# codex-noise-filter

A coding-focused Codex skill for reducing noisy context, enforcing call-chain analysis before edits, and embedding the user's global engineering rules inside the skill so they remain available across sessions and windows.

## When To Use

- Coding, debugging, refactoring, migration, and code explanation tasks.
- Multi-file investigation, cross-module backend analysis, Maven builds, and frontend fixes.
- Requests that ask for lower token usage, concise evidence, or reproducible reasoning.

## Layout

```text
SKILL.md
references/
  00-index.md
  01-global-engineering-rules.md
  02-noise-filter-workflow.md
  03-maven-backend-build.md
  04-frontend-rules.md
  05-delivery-templates.md
```

`SKILL.md` is intentionally small. It routes the agent to indexed reference files instead of loading every rule at once.

## Key Rules

- Reply in Simplified Chinese by default.
- Prefer JetBrains MCP / IDE tools for JetBrains projects.
- Before editing, confirm target files, root cause, minimal fix, and unaffected contracts.
- Confirm call chains and impact before code changes.
- Use `/Users/lilinhan/dev/maven-3.9.10/bin/mvn` as the preferred Maven executable.
- Use `/Users/lilinhan/maven-git` as the preferred local Maven repository.
- Build multi-module Maven projects from the aggregation root with `-pl <module> -am`.
- For frontend work, fix layout, component props, state handling, and contracts directly; do not hide backend issues with frontend hardcoding.
- Coding rules are embedded in this skill; keep the global `/Users/lilinhan/.codex/AGENTS.md` as a lightweight fallback.
- Before long context compression or window switching, write a Context Capsule with goal, evidence, changes, rollback points, and next step.

## Maven Examples

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am test
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -DskipTests package
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
```

## Codex Context Management

- Keep `SKILL.md` small and route details through `references/00-index.md`.
- For long tasks, use the sequence: task capsule, call-chain confirmation, minimal edit, lightweight validation, Context Capsule.
- Before switching windows or compacting context, emit a Context Capsule so goals, evidence, rollback points, and next steps are preserved.
- When the user inserts a new goal, treat it as an incremental task first and do not reset confirmed call chains by default.
- The global `AGENTS.md` no longer needs to carry every detail, but it should remain as a fallback entry point.
