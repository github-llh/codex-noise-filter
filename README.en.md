<div align="center">

# codex-noise-filter

**A Codex skill for coding-task noise reduction and indexed rule routing**

Reduce context noise · enforce call-chain checks · load rules progressively · align new and existing code · prevent magic values proactively

![Skill](https://img.shields.io/badge/Codex%20Skill-codex--noise--filter-2563eb)
![Routing](https://img.shields.io/badge/Routing-indexed%20references-16a34a)
![Mode](https://img.shields.io/badge/Mode-non--bypassable-f97316)
![Stacks](https://img.shields.io/badge/Stacks-Java%20%7C%20Python%20%7C%20Vue%2FReact%20%7C%20MiniProgram-7c3aed)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)

[Quick Start](#quick-start) · [Why Use It](#why-use-it) · [Usage](#usage) · [Activation Examples](#activation-examples) · [Capabilities](#capabilities) · [Layout](#layout) · [Community Health](#community-health) · [License](#license) · [简体中文](README.md)

</div>

## Quick Start

`codex-noise-filter` is a coding-focused Codex skill. It makes "read rules first, narrow context first, confirm call chains before editing" the default workflow, and uses `references/00-index.md` to progressively load rules for Java backend, Maven, frontend, Python, Mini Programs, concurrency/transactions, and delivery templates.

Use it for:

- Coding, debugging, refactoring, migration, and code explanation tasks.
- Pasted error logs, stack traces, build/test failures, IDE screenshots, code snippets, or diffs where Codex should infer whether to debug, fix, or validate.
- Multi-file investigation, cross-module backend analysis, Maven builds, frontend fixes, Mini Program native/uni-app/Taro work, and Python script/service/package/test work.
- Signals that the task needs lower token usage, concise evidence, reproducible reasoning, narrower file reads, or preserved evidence chains.

## Why Use It

Many coding-task failures are not caused by missing coding ability. They come from scattered context, incomplete call-chain checks, rules that apply only to new code, and existing touched code that keeps accumulating business logic or hardcoded values. `codex-noise-filter` turns those checks into the skill entrypoint so Codex confirms which rules to read, which files to touch, which boundaries to avoid, and how to validate before editing.

| Without it | With it |
| --- | --- |
| After pasting an error log, you still have to explain "debug/fix this" repeatedly. | Infer a debugging task from logs, stack traces, paths, commands, and the current repository, then find the root cause before applying the smallest fix and validation. |
| Repository-wide scanning can consume context with unrelated files and logs. | Read `references/00-index.md` first and load only task-relevant references. |
| Edits may ignore Controller/Service/DTO/Entity call-chain impact. | Confirm touched scope, call chain, and unaffected contracts before changes. |
| New code follows rules while existing touched code keeps business logic, hardcoding, and repeated setters/ifs. | Apply local rule alignment to both new code and existing touched code. |
| Strings, numbers, statuses, and thresholds may be written first and extracted only after review. | Run a style precheck before writing code: classify literals, reuse existing enums/constants/config/dictionaries/SDK constants, then decide whether a local literal is acceptable. |
| Obvious hardcoding, repeated logic, or layering issues in screenshots, snippets, or call-chain-related files may get blocked by an over-narrow "minimal change" reading. | Judge call-chain depth, file count, contract risk, and validation path automatically; when the closure is low-risk, write it into the task capsule, apply the matching reference, and fix it locally. |
| Build commands may be guessed from habit, such as `npm run build`, system `python`, or the current shell's `mvn`, then require manual environment hints after failure. | Match toolchains, commands, and cache entries from Java/Maven, Python, Node/frontend, and Mini Program project configuration; if a failure looks environment-related, recompute the cache and retry once. |
| Plan/Goal, resume, or cross-window work can forget constraints. | Plan/Goal/context restoration must still use indexed rules and Context Capsules. |

## Usage

Codex skills can be used from the Codex App, CLI, and IDE extension. Day-to-day activation should not depend on mentioning `$codex-noise-filter`; code, logs, stack traces, command output, screenshots with errors, paths, project structure, resume state, or rule-failure signals should be enough for the skill to treat the request as a coding task.

### Repository Scope

Use this when a team should share the same engineering rules.

```text
<repo>/.agents/skills/codex-noise-filter/
  SKILL.md
  references/
```

Start Codex from the repository root or a subdirectory. Mentioning the skill is only an additional signal, not an activation prerequisite:

```text
$codex-noise-filter inspect and fix this Maven backend issue using the indexed workflow.
```

### User Scope

Use this when the skill should apply across multiple repositories. Put this directory in the user-level skills directory supported by your Codex setup. If you use `CODEX_HOME`, place it under that profile's skills directory. Restart Codex if the skill does not appear in the selector.

### Codex App

1. Open the Codex App and select the project directory. Prefer Local mode for local code work.
2. Describe the coding task normally. Mentioning `$codex-noise-filter` is optional and only adds another signal.
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

In the interactive CLI, use `/skills` to select `codex-noise-filter`. Mentioning it in the prompt is only an additional signal:

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

### Automatic Activation Signals

These inputs should enter the indexed workflow without requiring an explicit skill mention:

- Java/Maven: `Exception`, `Caused by`, `BUILD FAILURE`, `Failed to execute goal`, `Compilation failure`, `NullPointerException`.
- Python: `Traceback`, `pytest`, `AssertionError`, `ModuleNotFoundError`, `ImportError`.
- Node/Vue/React: `npm ERR`, `pnpm ERR`, `yarn error`, `TypeError`, `ReferenceError`, `vite`, `webpack`.
- Mini Programs: `project.config.json`, `miniprogram-ci`, `setData`, `app.json`, `pages.json`, `TARO_ENV`, `mp-weixin`.
- Ambiguous but contextual Chinese prompts: `报错了`, `失败了`, `为什么不行`, `还是这样`, `处理一下`, `看下这个`.

## Activation Examples

You can copy these prompts directly:

```text
I pasted a Maven BUILD FAILURE. Find the root cause directly; if this repository has enough context, apply the smallest fix and rerun the smallest validation command.
```

```text
What is causing this Python Traceback? Use the current project's virtual environment and test configuration, and fix it if the cause is clear.
```

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
$codex-noise-filter inspect this Mini Program page after identifying native/uni-app/Taro, subpackage boundaries, dependency ownership, and the default build validation path.
```

More scenarios are in [`examples/`](examples/). Team rollout templates are in [`templates/`](templates/).

## Capabilities

| Capability | Description |
| --- | --- |
| Indexed routing | Read `00-index.md` first and open only the required reference files for the task. |
| Intent inference | Infer debugging, fixing, validation, or explanation intent from logs, stack traces, screenshots, paths, command output, code snippets, resume state, and risk signals from the evidence itself. |
| Non-bypass gates | New code, existing-code edits, Plan, Global/Goal, resumes, and cross-window work must confirm touched scope, call chains, and local alignment. |
| Smart window expansion | When editing code or judging strong-rule issues, local read windows are only the starting point; automatically expand by each stack's syntax for Java, Python, Vue/React, Mini Programs, SQL, config, scripts, and tests to cover full semantic units, contracts, direct calls, and nearby peer patterns. |
| Git history regression guard | When edits touch old logic, public contracts, historical compatibility, or high-risk boundaries, read the smallest useful git history evidence to compare commit intent, blame ranges, and key-token evolution before changing behavior. |
| Strong-rule auto escalation | When the touched scope, direct call chain, or related files that must be read for the task already hit hardcoding, repeated logic, hardcoded config, layering mistakes, comment-contract gaps, or security-boundary gaps, judge whether a low-risk closure exists; write it into the task capsule and fix it directly when it does, and record risk only when it does not. |
| Intelligent coding style gate | Before writing code, proactively identify magic strings, magic numbers, status/type/source values, thresholds, time windows, config keys, route/event/storage keys, and repeated mappings; prefer existing enums, constants, config, dictionaries, generated types, SDK constants, and design tokens. |
| Abstraction timing | When public interfaces, public methods, public classes, helpers, hooks/composables, schemas, mappers/converters, strategies, generics, or `any` boundaries appear, judge shared semantics, stable variation points, dependency direction, contract risk, and validation first; frontend `any` is limited to minimal bridge exceptions, while backend shared abstractions should prefer clear business interfaces or bounded generics. |
| Cross-stack shared governance | Every stack first checks shared rules for file ownership, commands, validation, security boundaries, hardcoded values, repeated logic, and comment placement, then applies stack-specific implementation details. |
| Java backend governance | Keeps controllers thin, requires service-interface comments, aligns entity Lombok usage, and checks transactions, enums, config, validation, and repeated logic. |
| Default validation across stacks | Java, Python, frontend, Mini Programs, and other stacks default to non-interactive syntax, compile, type-check, or build validation, without browser clicking, desktop operations, simulators, real devices, or external-system integration. |
| Frontend and Mini Programs | Covers general frontend, Vue 2/3, React, Vite, native Mini Programs, uni-app, Taro, subpackages, builds, and tests. |
| Environment discovery | For builds, compilation, tests, runs, previews, or pre-release checks, read stack-specific project facts such as `pom.xml`, `pyproject.toml`, `package.json`, and Mini Program config, then validate and reuse `.codex/local-environment.json`; if the cache does not satisfy the command or a failure looks environment-related, discover local candidates, update the cache, retry the original command, and protect it with a root `/.codex/` ignore rule. |
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
  13-read-expansion-and-history.md
  14-environment-cache-by-stack.md
```

`SKILL.md` is intentionally small. It routes the agent to indexed reference files instead of loading every rule at once.

## Efficiency Strategy

- Keep each reference file topic-focused instead of allowing one file to grow to several hundred lines.
- `01-global-engineering-rules.md` only contains globally shared rules, including file ownership, commands, validation, security boundaries, hardcoded values, repeated logic, and comment placement.
- `02-noise-filter-workflow.md` only contains cross-stack execution gates, context budgets, call-chain checks, and touched-scope alignment. Smart read expansion and Git history regression guards live in `13-read-expansion-and-history.md`, while stack-specific differences route to the matching reference files.
- Java backend architecture rules live in `07-java-backend-architecture.md` and should be opened only for layering, file placement, comments, or call chains.
- Java style rules live in `08-java-style-patterns.md` and should be opened only for enums, validation, Lombok, Optional, functional style, or repeated logic.
- Concurrency, async, and batch rules live in `09-concurrency-async-batch.md` and should be opened only for high concurrency, idempotency, deadlocks, events, middleware, thread pools, virtual threads, or user-context propagation.
- Python rules live in `10-python-development.md` and should be opened only for `.py`, Python syntax, virtual environments, dependencies, running commands, tests, linting, type checking, or Python performance work.
- Vue/React rules live in `11-frontend-vue-react.md` and should be opened only for Vue 2/3, React, Vite, component syntax, package management, running commands, tests, linting, type checking, or frontend builds.
- Mini Program rules live in `12-miniprogram-development.md` and should be opened whenever the task evidence involves native WeChat Mini Programs, uni-app, Taro, subpackages, `project.config.json`, `app.json`, `pages.json`, `app.config.*`, builds, releases, tests, or simulator/real-device workflows.
- Maven builds use `03-maven-backend-build.md`; environment discovery starts with `06-environment-discovery.md`, and stack-specific cache rules live in `14-environment-cache-by-stack.md`. `06` only handles discovery order, minimal validation, local cache structure, and `.codex/` ignore maintenance, not each stack's full runbook.
- Routing should cross-check task intent, code evidence, impact area, and risk signals to preserve accuracy without waiting for fixed prompt words or reading every rule file.
- `SKILL.md` hard constraints are always in force. Index performance tuning may reduce unrelated reference reads, but must not reduce mandatory constraints.
- Common tasks should use the quick-decision minimum set first, for example Java Controller/Service edits default to `02 + 07`, and add `08` only when enums, validation, Lombok, Optional, or repeated logic are involved.
- Python tasks default to `02 + 10`; before syntax checks, runs, tests, lint, or type checks, add `06 + 14` to create or reuse the Python environment cache. Add other references only when cross-system or frontend/backend call chains require them.
- General layout/state-contract tasks default to `02 + 04`; Vue/React tasks default to `02 + 11`, and add `06 + 14` before builds, type checks, lint, or tests to create or reuse the Node/frontend environment cache.
- Mini Program tasks default to `02 + 12`; add `11` when uni-app/Taro touches Vue/React syntax, add `04` for general layout/state contracts, and add `06 + 14` before builds, compilation, or CI to create or reuse the Mini Program environment cache. Discover developer-tool paths only when the current task goal itself includes simulator, preview, upload, real-device, or release workflows and the permission boundary is clear.
- If the touched scope expands during execution, add references through the index. Do not skip non-bypass gates, existing-code local alignment, layering, comments, transactions, concurrency, or business abstraction rules just to read fewer files.

## Key Rules

- Reply in Simplified Chinese by default.
- Prefer JetBrains MCP / IDE tools for JetBrains projects.
- Before editing, confirm target files, root cause, minimal fix, and unaffected contracts.
- Confirm call chains and impact before code changes.
- Read windows are only an initial budget. Before editing code or judging strong rules, infer the semantic boundary automatically from file type, framework configuration, and the matching reference. Java, Python, Vue/React, Mini Programs, SQL, config, scripts, and tests each use their own syntax and abstraction rules to expand to full logic, contracts, direct calls, and nearby peer patterns. Only report a gap when the boundary or business semantics cannot be inferred.
- When edits affect behavior semantics, public contracts, historical compatibility, regression risk, or old-logic refactors, automatically read the smallest useful git history evidence with `git log`, `git blame`, `git show`, `git diff`, and `git log -S/-G`. Scope history reads to touched files, semantic units, key tokens, and direct call chains; do not scan the full repository history or use git commands that mutate the worktree.
- Minimal change is not a reason to ignore strong-rule hits. If hardcoding, repeated logic, hardcoded config, layering mistakes, or comment/security gaps are already inside the touched scope, direct call chain, or related files that must be read for the task, judge low-risk closure first, write it into the task capsule, and fix locally when it holds.
- Regardless of whether the work is new code, an existing-code edit, Plan, Global/Goal mode, auto-resume, context restoration, cross-window continuation, a local patch, or a follow-up fix, coding tasks must run through the skill index, touched-scope confirmation, call-chain confirmation, and local rule alignment.
- Plan stages must also use the skill index. Plans must list applicable references, touched scope, local-alignment items, and acceptance checks.
- Global/Goal mode must also use the skill index. Each round must restore the goal, applicable references, touched scope, local-alignment items, acceptance checks, and Context Capsule.
- Rules apply to both new code and existing-code edits. Every touched method, class, DTO, SQL, test, and direct call chain must be locally aligned with the rules.
- Before toolchain commands, read stack-specific project configuration and validate `.codex/local-environment.json`: Java/Maven uses `pom.xml`, `.mvn/*`, wrapper, and Java/Maven version constraints; Python uses `pyproject.toml`, lock files, requirements, tox/nox, and virtual environments; frontend uses the target `package.json`, lockfile, `engines`, `packageManager`, and scripts; Mini Programs use `project.config.json`, `app.json`, `pages.json`, `manifest.json`, Taro/uni-app config, and any required `package.json`.
- Do not hardcode personal Maven executables, JDKs, local repositories, Python interpreters, Node package managers, Mini Program build scripts, or developer-tool paths. Use the cache directly when it satisfies the current command; discover local candidates only when the cache is missing, invalid, or mismatched with project configuration, then write validated values back and retry the original build/test/run command with the new cache.
- After updating `.codex/local-environment.json`, automatically check whether the Git root `.gitignore` covers `/.codex/`; add it when missing and verify it with `git check-ignore -v`.
- Build multi-module Maven projects from the aggregation root with `-pl <module> -am`.
- File ownership, commands, validation strategy, security boundaries, hardcoded values, repeated logic, and comment placement are shared across stacks. Judge them through `01-global-engineering-rules.md` first, then apply Java/Python/Vue/React/Mini Program syntax and project conventions.
- Before writing code, run the intelligent style precheck: classify new or retained strings, numbers, statuses, types, sources, protocol fields, error codes, config keys, route/event/storage keys, thresholds, time windows, and repeated mappings, then decide whether they belong in enums, constants, config, dictionaries, SDK constants, generated types, design tokens, or local literals.
- For Python projects, first confirm `requires-python`, `.python-version`, IDE interpreter, `.venv`, or lock files, and write or reuse the Python environment cache. Reuse the project's existing uv, poetry, pipenv, venv, tox, or nox workflow instead of installing dependencies into global pip.
- Python code should follow existing `pyproject.toml`, Ruff/Black/isort/mypy/pyright/pytest configuration. Add type hints and necessary docstrings for public functions, complex return values, cross-module DTOs, and configuration objects.
- Prefer project commands, `python -m ...`, `uv run ...`, or `poetry run ...` for Python execution. Prefer targeted tests such as `python -m pytest path::test` or existing `tox/nox` commands.
- Python edits should get the lightest relevant validation: syntax/import checks, targeted tests, and touched-scope lint/format/type checks. If validation cannot run, state why.
- Frontend projects must first identify `package.json`, lockfile, `packageManager`, Node version, and build tool. Do not mix npm/yarn/pnpm/bun.
- Before frontend compilation/builds, read the target `package.json` scripts, dependencies, `engines`, `packageManager`, and lockfile, match the Node version, package manager, and build script, then write them to `.codex/local-environment.json`; reuse the cache when it still matches the current package and command. If compilation fails and the failure may be caused by environment, dependency version, or script mismatch, reread project config and local tools, update the cache, and retry once.
- After Java, Python, frontend, Mini Program, or other stack tasks, do not run runtime, interactive, or screen-level validation by default: do not start a browser, use Browser/Computer Use, click through the desktop, open Mini Program simulators or real devices, or manually call external systems/API pages. Treat passing syntax checks, compilation, type checks, builds, or equivalent non-interactive commands as the default acceptance. Run browser, screenshot, page-click, visual-regression, E2E, simulator, real-device, external-service, or desktop-screen validation only when the current task goal itself requires that evidence and the permission boundary is clear.
- Vue projects must distinguish Vue 2 from Vue 3 first: Vue 2 defaults to Options API and Vue Test Utils v1, while Vue 3 can use Composition API, `<script setup>`, Pinia, and Vue Test Utils v2.
- React projects must first identify React/React DOM versions, framework, and TypeScript/JSX configuration. Hooks must only run at the top level of components or custom hooks; effects belong in `useEffect`, and pure derived values should not be stored as extra state.
- Before creating Vue/React components, confirm ownership, reuse value, public contract, and test/example entry points. When using components, prefer existing project components and keep props/slots/children/API boundaries small and stable.
- Mini Program projects must first identify whether they are native, uni-app, Taro, or another cross-platform framework. Different build modes use different syntax constraints: uni-app/Taro reuse the matching Vue/React rules, while native Mini Programs follow `Page`, `Component`, `wxml`, `wxss`, `setData`, and official API constraints.
- Mini Program validation should use the environment cache to match framework, platform, source root, output root, Node package manager, and existing CLI/CI build or compile commands by default. Do not open official developer-tool simulators, output directories, or real devices unless the current task goal itself requires that operational evidence and the permission boundary is clear.
- Mini Program subpackages must be evaluated when the main package approaches platform limits, startup slows down, heavy features are local-only, business domains are naturally isolated, or dependencies are only used in one area. Package-size limits must come from current official docs, developer-tool checks, or CI checks, not stale memory.
- Mini Program npm packages, plugins, subpackages, independent subpackages, preload rules, permissions, login, payment, subscribe messages, and web-view usage must follow target-platform official limits while preserving secrets, appids, upload credentials, and allowlist boundaries.
- Mini Program validation defaults to passing build/compile checks. Use `miniprogram-simulate`, `miniprogram-ci`, HBuilderX/uni-app automation, official simulators, or real devices only when the current task goal itself requires operational evidence and the permission boundary is clear.
- Comment rules apply across stacks: place comments at the natural contract location for each technology, such as Java service interfaces, Python docstrings, Vue props/emits/slots, React components/hooks/types, frontend exported interfaces/types and api clients, and SQL/config definitions. New edits, modifications, reads, searches, lint/format/type-check fixes, screenshot reviews, and diff reviews must trigger comment checks when they expose clear contract gaps.
- Frontend and Mini Program property typing is an automatic strong rule: when defining props, properties, events, slots, page params, request/response models, or public component APIs, projects that support TypeScript, JSDoc, PropTypes, Vue prop types, native Mini Program `properties.type`, or framework types must declare explicit types. Do not use bare `any`, `as any`, `Record<string, any>`, or broad objects to hide contract problems.
- Abstraction timing is an automatic gate: during additions, edits, reads, searches, lint/type-check fixes, screenshot/diff reviews, or call-chain checks, public interfaces, public methods, public classes, public files, helpers, hooks/composables, schemas, mappers/converters, strategies, generics, `any`, or `Object` boundaries must be evaluated before extraction. Frontend abstractions may isolate `any` only in minimal bridge layers such as untyped third-party code, framework pass-throughs, or migration buffers; backend abstractions should prefer clear business interfaces, explicit helpers, compile-time mappers/converters, or bounded generics instead of `Object`, reflection, or overly complex generics.
- Hardcoding rules apply across stacks: fixed closed sets use the stack's enum/union/dictionary pattern, technical standards use framework constants, environment or operations-variable values use configuration, and runtime-maintained business values use dictionaries, database tables, or configuration centers.
- Repeated-logic rules apply across stacks: when branches, mappings, validation, defaulting, or display assembly differ only by fields or stable cases, evaluate a stack-native mapper, converter, schema, strategy, hook/composable, or helper.
- Vue/React edits should run existing `typecheck`, `build`, `lint`, or equivalent syntax/compile commands. Do not verify key pages in a browser or click through the UI by default.
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

- For builds, compilation, tests, runs, previews, or pre-release checks, first identify the workspace root and `.codex/local-environment.json`.
- If an existing cache still passes minimal validation and satisfies the current command, reuse it without searching local paths again.
- Java/Maven cache entries are keyed by `pom.xml`, `.mvn/*`, wrapper, Java/Maven version constraints, aggregation root, and module path, and record the JDK, Maven, local repository, selected command, and verification command.
- Python cache entries are keyed by `pyproject.toml`, lock files, requirements, tox/nox, version files, and virtual environments, and record the interpreter, manager, lockfile, selected command, and verification command.
- Frontend cache entries are keyed to the target `package.json` and record `packageRoot`, `packageManager`, Node version requirements, lockfile, scripts, selected build command, and verification command; `npx` is only a command runner, not the package manager.
- Mini Program cache entries are keyed by `project.config.json`, `pages.json`, `manifest.json`, Taro/uni-app config, and any required `package.json`, and record framework, platform, source root, output root, build command, and required developer-tool verification status.
- If the cache is missing, invalid, or project configuration changed, search common local candidate paths.
- Validate discovered paths with a minimal command, such as `mvn -version` or `JAVA_HOME=<jdk> mvn -version` for Maven projects with a target JDK.
- After validation, write the result to `.codex/local-environment.json`, retry the original command with the new cache, and ensure the root `.gitignore` contains `/.codex/`.

## Codex Context Management

- Keep `SKILL.md` small and route details through `references/00-index.md`.
- For long tasks, use the sequence: task capsule, call-chain confirmation, minimal edit, lightweight validation, Context Capsule.
- When editing existing code, locally align the touched scope. Do not refactor the whole module, but do not apply the rules only to newly added lines.
- When a code snippet, IDE screenshot, or call-chain read exposes an obvious rule violation, locate the real file and direct call chain first. If impact is shallow, file count is small, and compatibility is clear, write it into the task capsule, apply the matching reference, and fix it instead of only listing a follow-up.
- In Global/Goal mode, restore the Context Capsule before each round. Goal pursuit must not bypass indexing, call-chain checks, or touched-scope alignment.
- Before switching windows or compacting context, emit a Context Capsule so goals, evidence, rollback points, and next steps are preserved.
- When the user inserts a new goal, treat it as an incremental task first and do not reset confirmed call chains by default.
- The global `AGENTS.md` no longer needs to carry every detail, but it should remain as a fallback entry point.
- Long-term memory should only store stable preferences and reusable rules, not machine-private absolute paths, temporary logs, one-off failures, or unverified guesses.

## Community Health

This project includes the community files recognized by GitHub Community Standards:

- [Code of Conduct](CODE_OF_CONDUCT.md): participation expectations and maintainer enforcement boundaries.
- [Contributing Guide](CONTRIBUTING.md): skill-specific change rules, bilingual README sync, and pull request checks.
- [Security Policy](SECURITY.md): private reporting guidance and supported scope.
- [Issue templates](.github/ISSUE_TEMPLATE): separate bug reports from feature requests and remind reporters to remove sensitive data.
- [Pull request template](.github/PULL_REQUEST_TEMPLATE.md): requires scope, synchronization notes, and validation results.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

Apache-2.0 keeps reuse permissive while making copyright, patent grant, contribution submission, and warranty-disclaimer boundaries explicit. For enterprise or regulated use, review it against your organization's open-source compliance process.
