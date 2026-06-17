# Security Policy

## Supported Versions

This repository is maintained from the default branch. Security fixes and policy updates target the current default branch unless maintainers state otherwise.

| Version | Supported |
| --- | --- |
| Default branch | Yes |
| Older snapshots, forks, or vendored copies | No |

## Reporting a Vulnerability

Do not open a public issue for sensitive vulnerabilities.

Report security concerns privately through one of these channels:

- GitHub private vulnerability reporting, if enabled for this repository.
- A direct private contact with the repository owner or maintainers.

Please include:

- A short description of the issue.
- Affected files or workflows.
- Steps to reproduce or a minimal proof of concept.
- Potential impact.
- Whether any secret, token, private path, customer data, or production endpoint may have been exposed.

Maintainers should acknowledge valid reports as soon as practical, investigate the scope, and publish a fix or mitigation when appropriate. If the report is not security-sensitive, maintainers may ask you to reopen it as a normal issue.

## Scope

Security reports may include:

- Accidental exposure of credentials, tokens, private endpoints, or sensitive logs.
- Guidance that could encourage unsafe code changes, unsafe command execution, or disclosure of private data.
- Templates or examples that include real secrets or production identifiers.
- Supply-chain concerns in scripts, templates, or generated artifacts.

Reports about general style, incomplete documentation, or normal feature requests should use the issue templates instead.

## 中文说明

安全问题不要直接发公开 issue。请通过 GitHub 私密漏洞上报能力或维护者私下联系方式报告，并包含影响文件、复现步骤、潜在影响和是否涉及密钥、私有路径、客户数据或生产地址。普通文档问题和功能建议请使用 issue 模板。
