<div align="center">

# codex-noise-filter

**An evidence-driven coding workflow skill for Codex**

Read less noise · Delegate minimally · Recover continuity automatically · Verify for real

[简体中文](README.md) · [Changelog](CHANGELOG.md) · [Distribution](distribution/README.md)

</div>

## Version 3 scope

`codex-noise-filter` supports explanation, diagnosis, review, and implementation in real repositories. It identifies the authorized task mode, narrows evidence from code, diffs, paths, configuration, logs, and failing commands, then closes the task with validation proportional to the touched scope. Version 3 adds plugin-bundled continuity hooks; Version 3.1 strengthens compaction recovery and bounded audit counters; Version 3.2 adds workload-aware, single-level delegation based on independence, context isolation, write conflicts, and total coordination cost.

Subagents stay off by default. The main agent delegates the minimum number of bounded lanes only when parallelism or context isolation clearly outweighs startup, handoff, verification, and extra-token costs. The main agent remains the sole orchestrator; subagents do not spawn descendants or duplicate the main agent's active scope.

Version 3 preserves the noise and side-effect boundaries established in version 2:

- No Guard Loop before every tool call.
- No checkpoint after a fixed number of files or tools.
- No mandatory `.codex/local-environment*.json` writes before validation.
- No automatic cleanup of unrelated code smells discovered during reading.
- No guessed third-party host paths; automatic behavior is claimed only for packaged, validated, host-enabled hooks.
- Call-chain depth is risk-based: simple failures stop at the complete semantic unit; high-risk changes expand to system boundaries.

Root-cause hypotheses, necessary call chains, dirty-worktree protection, external-content safety, failure strategy changes, and sufficient validation remain core behavior. Continuity state is limited to the plugin-owned `PLUGIN_DATA` directory and contains only irreversible fingerprints, model metadata, known reasons, and bounded event/injection counters. It never copies prompts, transcripts, raw tool output, logs, credentials, customer data, or workspace paths.

Across all supported stacks, new or modified comments, docstrings, Javadoc, JSDoc/TSDoc, and template notes default to Simplified Chinese. Business states, protocol keys, thresholds, timeouts, routes, events, and style tokens must follow the repository's established enum, constant, type, configuration, dictionary, or design-token patterns instead of remaining as magic values.

## Trigger boundary

Use it for:

- Reading, debugging, fixing, refactoring, migrating, and reviewing code.
- Diffs, paths, stack traces, build/test/lint/typecheck/CI output.
- Java/Maven, Python, Vue/React/TypeScript, mini programs, uni-app, and Taro.
- Skill, plugin, AGENTS, hook, MCP, manifest, marketplace, and agentic supply-chain audits.
- Task recovery after context compaction, session resume or reconnection, model switches, working-directory changes, and network or transport failures.

Do not use it for standalone general knowledge, generic advice without repository context, translation, or ordinary prose editing.

## Workflow

1. Read `SKILL.md` and `references/00-index.md`.
2. Classify the request as answer, diagnosis, review, or implementation.
3. Check the Git root, target module, branch, and dirty worktree.
4. Assess workload once at task definition or a material structure change; stay single-agent unless the benefit gate passes.
5. Start from the symptom or desired behavior, read the complete semantic unit, and expand the call chain only as risk requires.
6. Change only the authorized scope and direct dependencies required by the goal.
7. Run the smallest sufficient mix of static checks, target build/tests, and diff review.
8. After a continuity event, automatically rebuild the single next step from current instructions, worktree evidence, persisted files, and active tools.
9. Deliver the result, material changes, validation, and remaining gaps.

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

A direct Skill install provides instruction-level recovery only. Use the Plugin package below for automatic lifecycle triggers. Under Codex's official security model, non-managed command hooks require a one-time trust review when first enabled or changed. After that review, supported continuity events need no user reminder. If hooks are disabled, managed-only policy skips plugin hooks, or the current surface lacks an event, the workflow falls back to instruction-level recovery.

## Distribution

Build a ready-to-use local marketplace root:

```bash
scripts/build-plugin-package.sh
```

Output:

```text
dist/marketplace/
  .agents/plugins/marketplace.json
  plugins/codex-noise-filter/
    .codex-plugin/plugin.json
    hooks/
      hooks.json
      continuity_guard.py
    LICENSE
    skills/codex-noise-filter/
```

Install from the repository root and confirm discovery:

```bash
codex plugin marketplace add ./dist/marketplace
codex plugin add codex-noise-filter@codex-noise-filter-local
codex plugin list
```

Then start a new Codex task and run `/hooks` to confirm the Plugin hooks are listed and complete the initial trust review. Installing only the same-named Skill does not register Plugin hooks.

Inspect the latest execution and context-injection evidence:

```bash
STATE_DIR="$HOME/.codex/plugins/data/codex-noise-filter-codex-noise-filter-local/continuity"
LATEST_STATE="$(ls -t "$STATE_DIR"/*.json | head -n 1)"
python3 -m json.tool "$LATEST_STATE"
```

Inspect `event_counts`, `context_injection_count`, `last_context_event`, `last_context_kind`, and `last_context_reasons`. Successful routine events may stay silent; context is injected only for compaction, resume, model/workspace changes, or network failures.

The runtime Plugin also includes the continuity hooks. Its Skill payload contains only `SKILL.md`, `agents/`, and `references/`. Repository documentation, examples, templates, tests, and changelog files are excluded from the runtime package.

## Validation

```bash
python3 scripts/validate-project.py
python3 scripts/test-continuity-guard.py
bash -n scripts/build-plugin-package.sh
scripts/build-plugin-package.sh
python3 scripts/validate-project.py --plugin dist/marketplace/plugins/codex-noise-filter
python3 scripts/validate-project.py --marketplace-root dist/marketplace
git diff --check
```

The validator and hook tests use only the Python standard library and check frontmatter, naming, description size, direct reference links, local Markdown links, directional control characters, SemVer, manifest shape, hook events/paths/timeouts, and marketplace paths.

## Official sources

- [Build skills](https://developers.openai.com/codex/build-skills)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md)
- [Hooks](https://developers.openai.com/codex/hooks)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)

## Additional primary references

- [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- [GitHub Copilot Hooks](https://docs.github.com/en/copilot/concepts/agents/hooks)
- [OpenCode Plugins](https://opencode.ai/docs/plugins/)
- [Anthropic multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

## License

[Apache License 2.0](LICENSE)
