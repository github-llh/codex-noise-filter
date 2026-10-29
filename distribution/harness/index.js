/** 通过 Harness 原生技能注册与上下文快照提供路由，不启动外部进程、不注册 hooks、不改模型或权限。 */
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

export const inject = ['skills', 'systemPrompt'];

const SKILL_ROOT = new URL('./skills/codex-noise-filter/', import.meta.url);
const METADATA = JSON.parse(readFileSync(new URL('./metadata.json', import.meta.url), 'utf8'));
const ROUTING_ORDER = 100;

/** 注册随插件卸载自动清理的贡献：技能正文按需加载，只额外注入一条短路由快照。 */
export function apply(ctx) {
    const document = readFileSync(new URL('SKILL.md', SKILL_ROOT), 'utf8');
    const content = document.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
    const disposeSkill = ctx.skills.register({
        name: 'codex-noise-filter',
        description: METADATA.description,
        content,
        source: 'runtime',
        invocation: {modelInvocable: true, userInvocable: true},
        resourceBase: {kind: 'directory', path: fileURLToPath(SKILL_ROOT)},
    });
    // Harness 仅在快照变化或压缩移除旧快照后写入上下文，正文仍按需加载。
    const disposeContext = ctx.systemPrompt.context({
        name: 'codex-noise-filter:routing',
        order: ROUTING_ORDER,
        text: `${METADATA.activation}\n上下文压缩、恢复、模型切换或网络失败后，按 skill 的连续性规则复核最新目标、工作区、验证和操作回执，再继续下一步。`,
    });
    return () => {
        disposeContext();
        disposeSkill();
    };
}
