# codex-noise-filter

A model-neutral, evidence-driven coding workflow for scoped investigation, safe edits, proportionate validation, and continuity recovery. The stable name is retained for existing installations.

[中文](README.md) · [Distribution and installation](distribution/README.md) · [Official sources and host matrix](references/13-host-compatibility.md)

## v4

One canonical skill and guard produce separate Codex, Claude, Claude Windows, native DeepSeek Harness, portable Agent Plugins, and standard Agent Skills packages. GPT, Claude, MiMo, DeepSeek, and other providers use the integration supported by their **host**, rather than a model-specific copy of the workflow.

Native plugins inject short semantic routing once per session (startup, resume, clear, compaction recovery) instead of on every prompt. Claude registers `PostToolUseFailure` instead of `PostToolUse`. Routing delivery is observable; actual skill selection and adherence still require representative host tests.

Optimization preserves the selected model, reasoning effort, output budget, original tool results, and acceptance criteria. Successful unchanged tool events perform no state writes; historical-state pruning happens only when creating a session record. Guard scanning has global node, depth, character, and input limits. Those limits affect the guard's copy, never the original evidence delivered to the model.

## Build

Python 3.10+ standard library only:

```bash
python3 scripts/build-distributions.py
```

On Windows, use `py -3`. The default output is `dist/release-4.1.0/`, containing six host directories, reproducible ZIP files, a Harness npm tarball, five project entry layouts, and a separate chat instructions template. Existing nonempty output directories are never overwritten; choose a fresh `--output` when rebuilding. The legacy `scripts/build-plugin-package.sh` builds only the Codex marketplace using the same implementation.

See the [installation guide](distribution/README.md) for host-specific commands, archive layouts, upgrades, Python requirements, and duplicate-install checks. Building does not update installed copies or change global settings, API keys, models, or permissions.

## Support boundaries

- Codex local plugin hosts: Codex package, with supported hooks enabled and trusted.
- Claude Code/Desktop Code: native Claude package; POSIX hooks require `python3`, Windows hooks use PowerShell and `py -3`.
- Claude Chat: plugin skills are usable; hooks require a supporting Code/Cowork execution surface. Choose the package for the execution environment, including a Linux Cowork VM.
- DeepSeek Harness Desktop/CLI/Web: native Cordis bundle with skill registration and a stable context snapshot. Desktop activation is separate from CLI.
- Cursor, Gemini CLI, OpenCode, and Copilot App/CLI/IDE: generated `projects/` layouts use their documented skill and instruction paths.
- DeepSeek/MiMo through Codex or Claude Code: use that host's package. Deep Code can use the standard Skill package.
- Agent Plugins hosts: portable package with root `plugin.json`, skills only.
- Other desktop/web/mobile chat apps: use supported project/custom instructions or the [chat template](templates/chat-app-instructions.md). No undocumented lifecycle support or universal automatic activation is promised.

`AGENTS.md`, `CLAUDE.md`, custom subagent definitions, and `agents/openai.yaml` have different purposes. Claude Code can import shared project guidance with `@AGENTS.md` in `CLAUDE.md`; it does not automatically read `AGENTS.md`.

## Validate

```bash
python3 scripts/validate-project.py
python3 scripts/test-continuity-guard.py
python3 scripts/test-distributions.py
python3 scripts/benchmark-hooks.py
bash -n scripts/build-plugin-package.sh
git diff --check
```

An optional `--baseline-ref <trusted-git-ref>` benchmark executes the guard from that reviewed revision in temporary storage. Metrics separate in-process handling from Python process startup. They are local synthetic overhead measurements, not end-to-end model latency or quality results.

The guard stores only fingerprints and bounded metadata in host-provided plugin data directories. It never reads transcripts, stores prompts/tool output, modifies original tool results, or retries external writes. Without a state directory it runs statelessly. Disabled hooks and unavailable tools fall back to instruction-level behavior with explicit limitations.

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Apache-2.0](LICENSE)
