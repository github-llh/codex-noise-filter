<div align="center">

# codex-noise-filter

**An evidence-driven coding workflow skill for Codex**

Read less noise · Preserve dirty worktrees · Trace proportionately · Verify for real

[简体中文](README.md) · [Changelog](CHANGELOG.md) · [Distribution](distribution/README.md)

</div>

## Version 2 scope

`codex-noise-filter` supports explanation, diagnosis, review, and implementation in real repositories. It identifies the authorized task mode, narrows evidence from code, diffs, paths, configuration, logs, and failing commands, then closes the task with validation proportional to the touched scope.

Version 2 removes rules that created noise or unrequested side effects:

- No Guard Loop before every tool call.
- No checkpoint after a fixed number of files or tools.
- No mandatory `.codex/local-environment*.json` writes before validation.
- No automatic cleanup of unrelated code smells discovered during reading.
- No guessed third-party host paths or claims about unregistered hooks.
- Call-chain depth is risk-based: simple failures stop at the complete semantic unit; high-risk changes expand to system boundaries.

Root-cause hypotheses, necessary call chains, dirty-worktree protection, external-content safety, failure strategy changes, and sufficient validation remain core behavior.

## Trigger boundary

Use it for:

- Reading, debugging, fixing, refactoring, migrating, and reviewing code.
- Diffs, paths, stack traces, build/test/lint/typecheck/CI output.
- Java/Maven, Python, Vue/React/TypeScript, mini programs, uni-app, and Taro.
- Skill, plugin, AGENTS, hook, MCP, manifest, marketplace, and agentic supply-chain audits.

Do not use it for standalone general knowledge, generic advice without repository context, translation, or ordinary prose editing.

## Workflow

1. Read `SKILL.md` and `references/00-index.md`.
2. Classify the request as answer, diagnosis, review, or implementation.
3. Check the Git root, target module, branch, and dirty worktree.
4. Start from the symptom or desired behavior, read the complete semantic unit, and expand the call chain only as risk requires.
5. Change only the authorized scope and direct dependencies required by the goal.
6. Run the smallest sufficient mix of static checks, target build/tests, and diff review.
7. Deliver the result, material changes, validation, and remaining gaps.

## Install

Repository scope:

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  agents/openai.yaml
  references/
```

User scope: place the complete skill at `$HOME/.agents/skills/codex-noise-filter/`. Skills with the same name are not merged, so inspect duplicate installations if selection is ambiguous.

Explicit invocation:

```text
$codex-noise-filter diagnose and fix this build failure, preserve existing dirty changes, and run sufficient validation.
```

Implicit invocation depends on the `SKILL.md` description. Restart Codex and inspect duplicate copies if an update is not visible.

## Distribution

Build a ready-to-use local marketplace root:

```bash
scripts/build-plugin-package.sh
```

Output:

```text
dist/marketplace/
  marketplace.json
  plugins/codex-noise-filter/
    .codex-plugin/plugin.json
    LICENSE
    skills/codex-noise-filter/
```

The runtime skill contains only `SKILL.md`, `agents/`, and `references/`. Repository documentation, examples, templates, and changelog files are excluded from the packaged skill.

## Validation

```bash
python3 scripts/validate-project.py
bash -n scripts/build-plugin-package.sh
scripts/build-plugin-package.sh
python3 scripts/validate-project.py --plugin dist/marketplace/plugins/codex-noise-filter
python3 scripts/validate-project.py --marketplace-root dist/marketplace
git diff --check
```

The validator uses only the Python standard library and checks frontmatter, naming, description size, direct reference links, local Markdown links, directional control characters, SemVer, manifest shape, and marketplace paths.

## Official sources

- [Build skills](https://developers.openai.com/codex/build-skills)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md)
- [Hooks](https://developers.openai.com/codex/hooks)

## License

[Apache License 2.0](LICENSE)
