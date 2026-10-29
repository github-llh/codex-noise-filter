/** 测试 Harness bundle 的服务契约与分发结构；不冒充真实 Desktop 端到端验证。 */
import assert from 'node:assert/strict';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import test from 'node:test';

const pluginRoot = resolve(process.argv[2]);
const tarball = process.argv[3] ? resolve(process.argv[3]) : undefined;
const NAME = 'codex-noise-filter';
const BUNDLE_NAME = 'dsh-codex-noise-filter';
const ICON_LIMIT = 256 * 1024;

const manifest = JSON.parse(readFileSync(join(pluginRoot, 'package.json'), 'utf8'));
const registrations = { skills: [], contexts: [] };
const disposed = { skill: false, context: false };
const context = {
  skills: { register(skill) { registrations.skills.push(skill); return () => { disposed.skill = true; }; } },
  systemPrompt: { context(value) { registrations.contexts.push(value); return () => { disposed.context = true; }; } },
};
const plugin = await import(pathToFileURL(join(pluginRoot, 'index.js')));
const cleanup = plugin.apply(context);

test('bundle manifest 声明 dsh.bundle、入口导出与展示资源', () => {
  assert.equal(manifest.name, BUNDLE_NAME);
  assert.equal(manifest.type, 'module');
  assert.equal(manifest.private, true);
  assert.equal(manifest.main, 'index.js');
  assert.equal(manifest.icon, './icon.svg');
  assert.deepEqual(manifest.dsh, { bundle: { patch: './cordis.patch.yml' } });
  for (const [subpath, target] of Object.entries(manifest.exports)) {
    if (subpath.includes('*')) continue;
    assert.ok(existsSync(join(pluginRoot, target)), `${subpath} -> ${target}`);
  }
  assert.equal(manifest.exports['./locale/*.json'], './locale/*.json');
  assert.equal(manifest.exports['./icon'], './icon.svg');
});

test('patch 插入指向本包的可加载条目', () => {
  const patch = readFileSync(join(pluginRoot, 'cordis.patch.yml'), 'utf8');
  assert.match(patch, /- insert:/);
  assert.match(patch, new RegExp(`id:\\s*${NAME}`));
  assert.match(patch, new RegExp(`name:\\s*'?${BUNDLE_NAME}'?`));
});

test('Plugin Manager 展示元数据与图标可用', () => {
  for (const locale of ['en', 'zh']) {
    const meta = JSON.parse(readFileSync(join(pluginRoot, 'locale', `${locale}.json`), 'utf8')).meta;
    assert.equal(typeof meta.title, 'string');
    assert.ok(meta.title.length > 0);
    assert.equal(typeof meta.description, 'string');
    assert.ok(meta.description.length > 0);
  }
  const icon = readFileSync(join(pluginRoot, 'icon.svg'));
  assert.ok(icon.length > 0 && icon.length <= ICON_LIMIT);
  const text = icon.toString('utf8').trim();
  assert.ok(text.startsWith('<svg'));
  assert.ok(text.endsWith('</svg>'));
});

test('files 覆盖全部运行时文件，tarball 打包一致', () => {
  const files = manifest.files;
  for (const entry of ['index.js', 'metadata.json', 'cordis.patch.yml', 'icon.svg', 'locale/*.json', 'skills', 'LICENSE']) {
    assert.ok(files.includes(entry), `files 缺少 ${entry}`);
  }
  for (const entry of ['index.js', 'metadata.json', 'cordis.patch.yml', 'icon.svg', 'locale/en.json', 'locale/zh.json', 'skills']) {
    assert.ok(existsSync(join(pluginRoot, entry)), entry);
  }
  if (!tarball) return;
  assert.ok(existsSync(tarball), 'tarball 不存在');
  const tar = gunzipSync(readFileSync(tarball));
  const names = new Set();
  for (let offset = 0; offset + 512 <= tar.length;) {
    const name = tar.toString('utf8', offset, offset + 100).replace(/\0.*$/, '');
    if (!name) break;
    const size = parseInt(tar.toString('utf8', offset + 124, offset + 136).replace(/\0.*$/, '').trim() || '0', 8);
    names.add(name);
    offset += 512 + Math.ceil(size / 512) * 512;
  }
  for (const entry of files) {
    if (entry === 'skills') {
      assert.ok([...names].some(name => name.startsWith('package/skills/')), 'tarball 缺少 skills 目录');
    } else if (entry.includes('*')) {
      const prefix = `package/${entry.slice(0, entry.indexOf('*'))}`;
      assert.ok([...names].some(name => name.startsWith(prefix)), `tarball 缺少 ${entry}`);
    } else {
      assert.ok(names.has(`package/${entry}`), `tarball 缺少 ${entry}`);
    }
  }
});

test('技能可由名称加载，正文和资源入口完整', () => {
  assert.deepEqual(plugin.inject, ['skills', 'systemPrompt']);
  assert.equal(registrations.skills.length, 1);
  const skill = registrations.skills[0];
  assert.equal(skill.name, NAME);
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
  assert.equal(routing.name, `${NAME}:routing`);
  assert.equal(typeof routing.text, 'string');
  assert.ok(routing.text.length < 800);
  assert.equal(routing.complete, undefined);
  assert.equal(registrations.skills[0].content.includes(routing.text), false);
  assert.deepEqual(Object.keys(context).sort(), ['skills', 'systemPrompt']);
});

test('apply 返回的清理函数释放两项注册', () => {
  assert.equal(typeof cleanup, 'function');
  assert.deepEqual(disposed, { skill: false, context: false });
  cleanup();
  assert.deepEqual(disposed, { skill: true, context: true });
});
