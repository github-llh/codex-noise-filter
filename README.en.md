<div align="center">

# codex-noise-filter

**A Codex skill for coding-task noise reduction and indexed rule routing**

Reduce context noise · enforce call-chain checks · load rules progressively · align new and existing code

![Skill](https://img.shields.io/badge/Codex%20Skill-codex--noise--filter-2563eb)
![Routing](https://img.shields.io/badge/Routing-indexed%20references-16a34a)
![Mode](https://img.shields.io/badge/Mode-non--bypassable-f97316)
![Stacks](https://img.shields.io/badge/Stacks-Java%20%7C%20Python%20%7C%20Vue%2FReact%20%7C%20MiniProgram-7c3aed)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)

[Quick Start](#quick-start) · [Why Use It](#why-use-it) · [Usage](#usage) · [Activation Examples](#activation-examples) · [Capabilities](#capabilities) · [Layout](#layout) · [License](#license) · [简体中文](README.md)

</div>

## Quick Start

`codex-noise-filter` is a coding-focused Codex skill. It makes "read rules first, narrow context first, confirm call chains before editing" the default workflow, and uses `references/00-index.md` to progressively load rules for Java backend, Maven, frontend, Python, Mini Programs, concurrency/transactions, and delivery templates.

Use it for:

- Coding, debugging, refactoring, migration, and code explanation tasks.
- Multi-file investigation, cross-module backend analysis, Maven builds, frontend fixes, Mini Program native/uni-app/Taro work, and Python script/service/package/test work.
- Requests that ask for lower token usage, concise evidence, or reproducible reasoning.

## Why Use It

Many coding-task failures are not caused by missing coding ability. They come from scattered context, incomplete call-chain checks, rules that apply only to new code, and existing touched code that keeps accumulating business logic or hardcoded values. `codex-noise-filter` turns those checks into the skill entrypoint so Codex confirms which rules to read, which files to touch, which boundaries to avoid, and how to validate before editing.

| Without it | With it |
| --- | --- |
| Repository-wide scanning can consume context with unrelated files and logs. | Read `references/00-index.md` first and load only task-relevant references. |
| Edits may ignore Controller/Service/DTO/Entity call-chain impact. | Confirm touched scope, call chain, and unaffected contracts before changes. |
| New code follows rules while existing touched code keeps business logic, hardcoding, and repeated setters/ifs. | Apply local rule alignment to both new code and existing touched code. |
| Plan/Goal, resume, or cross-window work can forget constraints. | Plan/Goal/context restoration must still use indexed rules and Context Capsules. |

## Usage

Codex skills can be used from the Codex App, CLI, and IDE extension. Invocation can be explicit by mentioning `$codex-noise-filter`, or implicit when Codex matches a coding task to the `description` in `SKILL.md`.

### Repository Scope

Use this when a team should share the same engineering rules.

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  references/
```

Start Codex from the repository root or a subdirectory. For forced invocation, mention the skill directly:

```text
$codex-noise-filter inspect and fix this Maven backend issue using the indexed workflow.
```

### User Scope

Use this when the skill should apply across multiple repositories. Put this directory in the user-level skills directory supported by your Codex setup. If you use `CODEX_HOME`, place it under that profile's skills directory. Restart Codex if the skill does not appear in the selector.

### Codex App

1. Open the Codex App and select the project directory. Prefer Local mode for local code work.
2. Describe the coding task normally, or mention `$codex-noise-filter` explicitly.
3. To verify activation, ask Codex to print the matched skill, selected references, touched scope, and validation checks first.

Example:

```text
$codex-noise-filter move business logic out of this Controller and list the references you read.
```

### Terminal / CLI

Start Codex from the project root:

```bash
codex
```

In the interactive CLI, use `/skills` to select `codex-noise-filter`, or mention it directly in the prompt:

```text
$codex-noise-filter read the minimum indexed references and review this Java Service change.
```

For longer work, combine it with `/plan` or `/goal`. Plan/Goal mode still must follow this skill's indexing, call-chain, and local-alignment rules.

### IDE Extension

In VS Code, JetBrains IDEs, or similar IDE surfaces, make sure Codex is attached to the target project. For JetBrains projects, this skill prefers JetBrains MCP / IDE tools before Shell. You can start with:

```text
$codex-noise-filter use IDE context to locate the call chain; avoid broad repository scans.
```

### Lightweight Global AGENTS Fallback

The global `AGENTS.md` does not need to duplicate this skill. Keep it small:

```md
# Language Preference
Use Simplified Chinese by default.

# Tooling Preference
Prefer JetBrains MCP / IDE tools in JetBrains projects; prefer rg for search.

# Programming Tasks
Use codex-noise-filter for coding tasks; read SKILL.md and references/00-index.md first.
```

### Verify Activation

After installation, test with:

```text
Tell me whether this task triggers codex-noise-filter. If yes, list the references you will read, the touched scope, the out-of-scope areas, and validation checks.
```

If it does not trigger, common causes are missing code context, the skill not being in a scanned skills directory, a same-name skill conflict, or a Codex session that needs a restart.

## Activation Examples

You can copy these prompts directly:

```text
$codex-noise-filter check whether this Controller contains business logic and move logic that belongs in the Service implementation.
```

```text
$codex-noise-filter use Maven multi-module root build rules to find the smallest validation command for this module.
```

```text
$codex-noise-filter when editing this Service, also check interface comments, transaction boundaries, enum/config extraction, and repeated if/set blocks.
```

```text
$codex-noise-filter fix this Vue/React component issue after confirming framework version, component ownership, state contract, and validation commands.
```

```text
$codex-noise-filter investigate this Python test failure after identifying the virtual environment, dependency manager, targeted test, and lint/type-check path.
```

```text
$codex-noise-filter inspect this Mini Program page after identifying native/uni-app/Taro, subpackage boundaries, dependency ownership, and simulator validation.
```

More scenarios are in [`examples/`](examples/). Team rollout templates are in [`templates/`](templates/).

## Capabilities

| Capability | Description |
| --- | --- |
| Indexed routing | Read `00-index.md` first and open only the required reference files for the task. |
| Non-bypass gates | New code, existing-code edits, Plan, Global/Goal, resumes, and cross-window work must confirm touched scope, call chains, and local alignment. |
| Java backend governance | Keeps controllers thin, requires service-interface comments, aligns entity Lombok usage, and checks transactions, enums, config, validation, and repeated logic. |
| Frontend and Mini Programs | Covers general frontend, Vue 2/3, React, Vite, native Mini Programs, uni-app, Taro, subpackages, simulators, and tests. |
| Environment discovery | Maven/JDK/Node/Python/Mini Program tools are discovered from project config and cache first, then validated into `.codex/local-environment.json`. |
| Context management | Uses Context Capsules for long tasks so goals, evidence, changes, rollback points, and next steps survive context switches. |

## Layout

```text
SKILL.md
CHANGELOG.md
examples/
templates/
references/
  00-index.md
  01-global-engineering-rules.md
  02-noise-filter-workflow.md
  03-maven-backend-build.md
  04-frontend-rules.md
  05-delivery-templates.md
  06-environment-discovery.md
  07-java-backend-architecture.md
  08-java-style-patterns.md
  09-concurrency-async-batch.md
  10-python-development.md
  11-frontend-vue-react.md
  12-miniprogram-development.md
```

`SKILL.md` is intentionally small. It routes the agent to indexed reference files instead of loading every rule at once.

## Efficiency Strategy

- Keep each reference file topic-focused instead of allowing one file to grow to several hundred lines.
- `01-global-engineering-rules.md` only contains globally shared rules.
- Java backend architecture rules live in `07-java-backend-architecture.md` and should be opened only for layering, file placement, comments, or call chains.
- Java style rules live in `08-java-style-patterns.md` and should be opened only for enums, validation, Lombok, Optional, functional style, or repeated logic.
- Concurrency, async, and batch rules live in `09-concurrency-async-batch.md` and should be opened only for high concurrency, idempotency, deadlocks, events, middleware, thread pools, virtual threads, or user-context propagation.
- Python rules live in `10-python-development.md` and should be opened only for `.py`, Python syntax, virtual environments, dependencies, running commands, tests, linting, type checking, or Python performance work.
- Vue/React rules live in `11-frontend-vue-react.md` and should be opened only for Vue 2/3, React, Vite, component syntax, package management, running commands, tests, linting, type checking, or frontend builds.
- Mini Program rules live in `12-miniprogram-development.md` and should be opened only for native WeChat Mini Programs, uni-app, Taro, subpackages, official simulators, `project.config.json`, `app.json`, `pages.json`, `app.config.*`, builds, releases, or tests.
- Maven builds use `03-maven-backend-build.md`; environment discovery uses `06-environment-discovery.md`.
- Routing should cross-check keywords, user intent, and impact area to preserve accuracy without reading every rule file.
- `SKILL.md` hard constraints are always in force. Index performance tuning may reduce unrelated reference reads, but must not reduce mandatory constraints.
- Common tasks should use the quick-decision minimum set first, for example Java Controller/Service edits default to `02 + 07`, and add `08` only when enums, validation, Lombok, Optional, or repeated logic are involved.
- Python tasks default to `02 + 10`; add `06` only when environment paths are unknown, and add other references only when cross-system or frontend/backend call chains require them.
- General layout/state-contract tasks default to `02 + 04`; Vue/React tasks default to `02 + 11`, and add `06` only when environment paths are unknown.
- Mini Program tasks default to `02 + 12`; add `11` when uni-app/Taro touches Vue/React syntax, add `04` for general layout/state contracts, and add `06` only when developer-tool paths are unknown.
- If the touched scope expands during execution, add references through the index. Do not skip non-bypass gates, existing-code local alignment, layering, comments, transactions, concurrency, or business abstraction rules just to read fewer files.

## Key Rules

- Reply in Simplified Chinese by default.
- Prefer JetBrains MCP / IDE tools for JetBrains projects.
- Before editing, confirm target files, root cause, minimal fix, and unaffected contracts.
- Confirm call chains and impact before code changes.
- Regardless of whether the work is new code, an existing-code edit, Plan, Global/Goal mode, auto-resume, context restoration, cross-window continuation, a local patch, or a follow-up fix, coding tasks must run through the skill index, touched-scope confirmation, call-chain confirmation, and local rule alignment.
- Plan stages must also use the skill index. Plans must list applicable references, touched scope, local-alignment items, and acceptance checks.
- Global/Goal mode must also use the skill index. Each round must restore the goal, applicable references, touched scope, local-alignment items, acceptance checks, and Context Capsule.
- Rules apply to both new code and existing-code edits. Every touched method, class, DTO, SQL, test, and direct call chain must be locally aligned with the rules.
- Discover Maven from `.codex/local-environment.json`, IDE/project configuration, and verified local candidates.
- Do not hardcode personal Maven executable or local-repository paths. On first use, discover them from the current machine and project configuration, validate them, write them to this workspace's `.codex/local-environment.json`, and reuse that cache later.
- Build multi-module Maven projects from the aggregation root with `-pl <module> -am`.
- For Python projects, first confirm `requires-python`, `.python-version`, IDE interpreter, `.venv`, or lock files. Reuse the project's existing uv, poetry, pipenv, venv, tox, or nox workflow instead of installing dependencies into global pip.
- Python code should follow existing `pyproject.toml`, Ruff/Black/isort/mypy/pyright/pytest configuration. Add type hints and necessary docstrings for public functions, complex return values, cross-module DTOs, and configuration objects.
- Prefer project commands, `python -m ...`, `uv run ...`, or `poetry run ...` for Python execution. Prefer targeted tests such as `python -m pytest path::test` or existing `tox/nox` commands.
- Python edits should get the lightest relevant validation: syntax/import checks, targeted tests, and touched-scope lint/format/type checks. If validation cannot run, state why.
- Frontend projects must first identify `package.json`, lockfile, `packageManager`, Node version, and build tool. Do not mix npm/yarn/pnpm/bun.
- Vue projects must distinguish Vue 2 from Vue 3 first: Vue 2 defaults to Options API and Vue Test Utils v1, while Vue 3 can use Composition API, `<script setup>`, Pinia, and Vue Test Utils v2.
- React projects must first identify React/React DOM versions, framework, and TypeScript/JSX configuration. Hooks must only run at the top level of components or custom hooks; effects belong in `useEffect`, and pure derived values should not be stored as extra state.
- Before creating Vue/React components, confirm ownership, reuse value, public contract, and test/example entry points. When using components, prefer existing project components and keep props/slots/children/API boundaries small and stable.
- Mini Program projects must first identify whether they are native, uni-app, Taro, or another cross-platform framework. Different build modes use different syntax constraints: uni-app/Taro reuse the matching Vue/React rules, while native Mini Programs follow `Page`, `Component`, `wxml`, `wxss`, `setData`, and official API constraints.
- Mini Program execution should prefer the official developer-tool simulator or existing CLI/CI workflow. Generate the target platform project first, open the correct output directory, and do not maintain `dist/` or `unpackage/dist/` as source code.
- Mini Program subpackages must be evaluated when the main package approaches platform limits, startup slows down, heavy features are local-only, business domains are naturally isolated, or dependencies are only used in one area. Package-size limits must come from current official docs, developer-tool checks, or CI checks, not stale memory.
- Mini Program npm packages, plugins, subpackages, independent subpackages, preload rules, permissions, login, payment, subscribe messages, and web-view usage must follow target-platform official limits while preserving secrets, appids, upload credentials, and allowlist boundaries.
- Mini Program validation should reuse existing `miniprogram-simulate`, `miniprogram-ci`, HBuilderX/uni-app automated tests, Taro/Jest/Vitest/Testing Library, or official simulator checks. High-risk platform capabilities should state whether device validation is still needed.
- Comment rules apply across stacks: place comments at the natural contract location for each technology, such as Java service interfaces, Python docstrings, Vue props/emits/slots, React components/hooks/types, and SQL/config definitions.
- Vue/React edits should run existing `lint`, `typecheck`, `test`, `build`, or targeted test commands. For interaction and layout changes, verify key pages in a browser.
- Before creating files, confirm the target module, layer responsibility, package path, existing peer files, and dependency direction. Interfaces, implementations, entities, and contracts may live in different modules.
- Prefer business enums for stable fixed sets such as status, type, source, action, phase, and result values. Avoid scattered magic strings and numbers.
- Environment- or operations-variable values such as URLs, secrets, toggles, thresholds, time windows, thread pools, cache TTLs, and external-system parameters should live in yml/properties or the configuration center and be injected through typed configuration classes.
- Put simple input validation on DTO/Request classes with Bean Validation annotations. Controllers should only trigger validation and rely on unified exception handling.
- Multi-status, multi-type, multi-source, multi-external-system, repeated workflow, repeated assembly, repeated field mapping, or stable extension-point logic must be evaluated for business abstraction into service methods, domain components, strategies, enum behavior, assemblers/converters, configuration properties, or existing project extension points.
- Avoid long repeated `if`, `set`, conversion, or defaulting blocks where only field names differ. Prefer existing project mapping, validation, enum strategy, conditional update, or helper patterns.
- Use `Optional`, Stream, method references, and functional style for null handling when the Java version and project style support them, but do not overuse them in DTO/entity fields or simple cases.
- When a project already uses Lombok, do not hand-write meaningless getters/setters. Use Lombok for DTO/VO/entity classes following peer-file style, and reuse the existing `@Data` entity convention when the project already has one.
- Keep Java backend controllers thin. Return-data enrichment, list post-processing, URL/name/status filling, database/cache/remote reads, state transitions, and complex branching must move to service implementations, assemblers, or existing business components.
- Service interfaces and all public service methods must have contract comments. When editing existing interfaces, touched methods must be updated too, without waiting for a user reminder.
- When adding or editing response entities, database entities, DTOs, or VOs, update class and key-field comments in the same change, especially for status, type, source, unit, external mapping, compatibility fields, permission semantics, and masking semantics.
- Put transactions on service implementation business-entry methods by default. For precise commit/rollback boundaries, segmented commits, or allowed partial failures, reuse the project transaction manager or functional `TransactionTemplate` style.
- For high concurrency, consider idempotency, lock ordering, deadlock prevention, async eventual consistency, batched execution, and user/tenant/audit context propagation.
- Add reason-focused comments to service interfaces and important implementation methods. Comments should be non-redundant, complete where needed, and orderly.
- For frontend work, fix layout, component props, state handling, and contracts directly; do not hide backend issues with frontend hardcoding.
- Coding rules are embedded in this skill; keep the global `AGENTS.md` under the current Codex home as a lightweight fallback.
- Before long context compression or window switching, write a Context Capsule with goal, evidence, changes, rollback points, and next step.

## Maven Examples

```bash
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am test
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am -DskipTests package
<mavenExecutable> -Dmaven.repo.local=<localRepository> -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
```

## Environment Discovery

- On first use of Maven, JDK, Node, Python, or package managers, read IDE/project configuration first.
- If configuration does not provide a usable path, search common local candidate paths.
- Validate discovered paths with a minimal command, such as `mvn -version`.
- After validation, write the result to `.codex/local-environment.json` and reuse it later.
- If the cache is invalid or project configuration changes, rediscover and update the cache.

## Codex Context Management

- Keep `SKILL.md` small and route details through `references/00-index.md`.
- For long tasks, use the sequence: task capsule, call-chain confirmation, minimal edit, lightweight validation, Context Capsule.
- When editing existing code, locally align the touched scope. Do not refactor the whole module, but do not apply the rules only to newly added lines.
- In Global/Goal mode, restore the Context Capsule before each round. Goal pursuit must not bypass indexing, call-chain checks, or touched-scope alignment.
- Before switching windows or compacting context, emit a Context Capsule so goals, evidence, rollback points, and next steps are preserved.
- When the user inserts a new goal, treat it as an incremental task first and do not reset confirmed call chains by default.
- The global `AGENTS.md` no longer needs to carry every detail, but it should remain as a fallback entry point.
- Long-term memory should only store stable preferences and reusable rules, not machine-private absolute paths, temporary logs, one-off failures, or unverified guesses.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

Apache-2.0 keeps reuse permissive while making copyright, patent grant, contribution submission, and warranty-disclaimer boundaries explicit. For enterprise or regulated use, review it against your organization's open-source compliance process.
