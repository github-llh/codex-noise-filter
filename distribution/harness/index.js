/** 通过 Harness 原生技能注册与上下文快照提供路由，不启动外部进程。 */
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

export const name = 'codex-noise-filter';
export const inject = ['skills', 'systemPrompt'];

const SKILL_ROOT = new URL('./skills/codex-noise-filter/', import.meta.url);
const METADATA = JSON.parse(readFileSync(new URL('./metadata.json', import.meta.url), 'utf8'));
const ROUTING_ORDER = 100;

/** 注册随插件卸载自动清理的贡献，不修改其他插件、模型或权限。 */
export function apply(ctx) {
    const document = readFileSync(new URL('SKILL.md', SKILL_ROOT), 'utf8');
    const content = document.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
    ctx.skills.register({
        name,
        description: METADATA.description,
        content,
        source: 'runtime',
        invocation: {modelInvocable: true, userInvocable: true},
        resourceBase: {kind: 'directory', path: fileURLToPath(SKILL_ROOT)},
    });
    // Harness 仅在快照变化或压缩移除旧快照后写入上下文，正文仍按需加载。
    ctx.systemPrompt.context({
        name: `${name}:routing`,
        order: ROUTING_ORDER,
        text: `${METADATA.activation}\n上下文压缩、恢复、模型切换或网络失败后，按 skill 的连续性规则复核最新目标、工作区、验证和操作回执，再继续下一步。`,
    });
}
