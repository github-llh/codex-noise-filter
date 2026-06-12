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
  06-environment-discovery.md
  07-java-backend-architecture.md
  08-java-style-patterns.md
  09-concurrency-async-batch.md
```

`SKILL.md` is intentionally small. It routes the agent to indexed reference files instead of loading every rule at once.

## Efficiency Strategy

- Keep each reference file topic-focused instead of allowing one file to grow to several hundred lines.
- `01-global-engineering-rules.md` only contains globally shared rules.
- Java backend architecture rules live in `07-java-backend-architecture.md` and should be opened only for layering, file placement, comments, or call chains.
- Java style rules live in `08-java-style-patterns.md` and should be opened only for enums, validation, Lombok, Optional, functional style, or repeated logic.
- Concurrency, async, and batch rules live in `09-concurrency-async-batch.md` and should be opened only for high concurrency, idempotency, deadlocks, events, middleware, thread pools, virtual threads, or user-context propagation.
- Maven builds use `03-maven-backend-build.md`; environment discovery uses `06-environment-discovery.md`.
- Routing should cross-check keywords, user intent, and impact area to preserve accuracy without reading every rule file.

## Key Rules

- Reply in Simplified Chinese by default.
- Prefer JetBrains MCP / IDE tools for JetBrains projects.
- Before editing, confirm target files, root cause, minimal fix, and unaffected contracts.
- Confirm call chains and impact before code changes.
- Plan stages must also use the skill index. Plans must list applicable references, touched scope, local-alignment items, and acceptance checks.
- Global/Goal mode must also use the skill index. Each round must restore the goal, applicable references, touched scope, local-alignment items, acceptance checks, and Context Capsule.
- Rules apply to both new code and existing-code edits. Every touched method, class, DTO, SQL, test, and direct call chain must be locally aligned with the rules.
- Discover Maven from `.codex/local-environment.json`, IDE/project configuration, and verified local candidates.
- The currently verified Maven candidate is `/Users/lilinhan/dev/maven-3.9.10/bin/mvn`; the local repository candidate is `/Users/lilinhan/maven-git`.
- Build multi-module Maven projects from the aggregation root with `-pl <module> -am`.
- Before creating files, confirm the target module, layer responsibility, package path, existing peer files, and dependency direction. Interfaces, implementations, entities, and contracts may live in different modules.
- Prefer business enums for stable fixed sets such as status, type, source, action, phase, and result values. Avoid scattered magic strings and numbers.
- Environment- or operations-variable values such as URLs, secrets, toggles, thresholds, time windows, thread pools, cache TTLs, and external-system parameters should live in yml/properties or the configuration center and be injected through typed configuration classes.
- Put simple input validation on DTO/Request classes with Bean Validation annotations. Controllers should only trigger validation and rely on unified exception handling.
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
- Coding rules are embedded in this skill; keep the global `/Users/lilinhan/.codex/AGENTS.md` as a lightweight fallback.
- Before long context compression or window switching, write a Context Capsule with goal, evidence, changes, rollback points, and next step.

## Maven Examples

```bash
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am test
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -DskipTests package
/Users/lilinhan/dev/maven-3.9.10/bin/mvn -Dmaven.repo.local=/Users/lilinhan/maven-git -pl <module-path-or-artifact> -am -Dtest=ClassNameTest#methodName -Dsurefire.failIfNoSpecifiedTests=false test
```

## Environment Discovery

- On first use of Maven, JDK, Node, or package managers, read IDE/project configuration first.
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
- Long-term memory should only store stable preferences and reusable rules, not temporary logs, one-off failures, or unverified guesses.
