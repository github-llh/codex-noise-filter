/** 测试 Harness 适配器的服务契约；不冒充真实 Desktop 端到端验证。 */
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import test from 'node:test';

const pluginRoot = resolve(process.argv[2]);
const plugin = await import(pathToFileURL(join(pluginRoot, 'index.js')));
const registrations = { skills: [], contexts: [] };
const context = {
  skills: { register(skill) { registrations.skills.push(skill); } },
  systemPrompt: { context(value) { registrations.contexts.push(value); } },
};
plugin.apply(context);

test('技能可由名称加载，正文和资源入口完整', () => {
  assert.deepEqual(plugin.inject, ['skills', 'systemPrompt']);
  assert.equal(registrations.skills.length, 1);
  const skill = registrations.skills[0];
  assert.equal(skill.name, 'codex-noise-filter');
  assert.equal(skill.invocation.modelInvocable, true);
  assert.equal(skill.invocation.userInvocable, true);
  const root = skill.resourceBase.path;
  const original = readFileSync(join(root, 'SKILL.md'), 'utf8');
  assert.equal(skill.content, original.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ''));
  for (const match of skill.content.matchAll(/\]\((references\/[^)]+)\)/g)) {
    assert.ok(existsSync(join(root, match[1])), match[1]);
  }
});

test('只注册稳定的短上下文快照，没有覆盖完整 prompt 或新增事件处理器', () => {
  assert.equal(registrations.contexts.length, 1);
  const routing = registrations.contexts[0];
  assert.equal(typeof routing.text, 'string');
  assert.ok(routing.text.length < 800);
  assert.equal(routing.complete, undefined);
  assert.equal(registrations.skills[0].content.includes(routing.text), false);
  assert.deepEqual(Object.keys(context).sort(), ['skills', 'systemPrompt']);
});
