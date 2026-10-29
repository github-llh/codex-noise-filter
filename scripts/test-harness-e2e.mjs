#!/usr/bin/env node
/** 用 DeepSeek Harness 安装内的真实 cordis Loader 与 skills/systemPrompt 服务加载 harness bundle。
 *  从 Desktop 安装的 app.asar 提取包树到临时目录，按 patch 条目导入 bundle，验证注册、装配与释放。
 *  用法: node scripts/test-harness-e2e.mjs [pluginRoot] [--asar <path>]
 *  不安装插件、不改用户配置、不调用模型；不能替代真实 Desktop 安装验收。 */
import assert from 'node:assert/strict';
import { openSync, readSync, closeSync, mkdirSync, writeFileSync, symlinkSync, rmSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { mkdtempSync } from 'node:fs';

const pluginRoot = resolve(process.argv[2] ?? 'dist/release-4.1.0/harness/codex-noise-filter');
const asarFlag = process.argv.indexOf('--asar');
const ASAR = asarFlag === -1 ? defaultAsarPath() : resolve(process.argv[asarFlag + 1]);
const BUNDLE_NAME = 'dsh-codex-noise-filter';
const ROOTS = ['@deepseek-ai/cordis', '@deepseek-ai/cordis-plugin-loader', '@deepseek-ai/dsh-skill', '@deepseek-ai/dsh-system-prompt'];

function defaultAsarPath() {
  if (process.platform === 'darwin') return '/Applications/DeepSeek Harness.app/Contents/Resources/app.asar';
  if (process.platform === 'win32') return join(process.env.LOCALAPPDATA ?? '', 'Programs', 'DeepSeek Harness', 'resources', 'app.asar');
  return '/opt/DeepSeek Harness/resources/app.asar';
}

/** 读取 embedded asar（header 位于文件头部）的文件表与数据区。 */
function readAsar(archive) {
  if (!existsSync(archive)) throw new Error(`找不到 DeepSeek Harness 安装: ${archive}（用 --asar 指定）`);
  const fd = openSync(archive, 'r');
  const prefix = Buffer.alloc(16);
  readSync(fd, prefix, 0, 16, 0);
  const payloadSize = prefix.readUInt32LE(8);
  const stringSize = prefix.readUInt32LE(12);
  const jsonBuf = Buffer.alloc(stringSize);
  readSync(fd, jsonBuf, 0, stringSize, 16);
  closeSync(fd);
  const files = new Map();
  (function walk(node, base = '') {
    for (const [name, entry] of Object.entries(node.files ?? {})) {
      const path = base ? `${base}/${name}` : name;
      if (entry.files) walk(entry, path);
      else files.set(path, entry);
    }
  })(JSON.parse(jsonBuf.toString('utf8')));
  const dataBase = 12 + payloadSize;
  return {
    read(path) {
      const entry = files.get(path);
      if (!entry) return null;
      const handle = openSync(archive, 'r');
      const buffer = Buffer.alloc(Number(entry.size));
      readSync(handle, buffer, 0, Number(entry.size), dataBase + Number(entry.offset));
      closeSync(handle);
      return buffer;
    },
  };
}

/** 按依赖图提取包树，使 bundle 与 DSH 服务在同一 node_modules 下解析。 */
function extractTree(asar, destination) {
  const queue = [...ROOTS];
  const done = new Set();
  while (queue.length) {
    const name = queue.shift();
    if (done.has(name)) continue;
    done.add(name);
    const base = `dsh/node_modules/${name}`;
    const manifestBuf = asar.read(`${base}/package.json`);
    if (!manifestBuf) throw new Error(`app.asar 中缺少包 ${name}`);
    const manifest = JSON.parse(manifestBuf.toString('utf8'));
    const target = join(destination, name);
    mkdirSync(dirname(join(target, 'package.json')), { recursive: true });
    writeFileSync(join(target, 'package.json'), manifestBuf);
    const entries = new Set();
    if (typeof manifest.main === 'string') entries.add(manifest.main.replace(/^\.\//, ''));
    for (const value of Object.values(manifest.exports ?? {})) {
      if (typeof value === 'string') entries.add(value.replace(/^\.\//, ''));
      else if (value && typeof value === 'object') {
        for (const condition of ['default', 'import', 'module', 'require']) {
          if (typeof value[condition] === 'string') entries.add(value[condition].replace(/^\.\//, ''));
        }
      }
    }
    for (const entry of entries) {
      if (entry.includes('*') || !/\.(m?js|cjs)$/.test(entry)) continue;
      const buffer = asar.read(`${base}/${entry}`);
      if (!buffer) throw new Error(`app.asar 中缺少文件 ${name}/${entry}`);
      mkdirSync(dirname(join(target, entry)), { recursive: true });
      writeFileSync(join(target, entry), buffer);
    }
    for (const dep of Object.keys(manifest.dependencies ?? {})) queue.push(dep);
    for (const dep of Object.keys(manifest.peerDependencies ?? {})) if (dep.startsWith('@deepseek-ai/')) queue.push(dep);
  }
}

const workspace = mkdtempSync(join(tmpdir(), 'dsh-harness-e2e-'));
try {
  extractTree(readAsar(ASAR), join(workspace, 'node_modules'));
  symlinkSync(pluginRoot, join(workspace, 'node_modules', BUNDLE_NAME), 'dir');
  const { Context } = await import(join(workspace, 'node_modules/@deepseek-ai/cordis/lib/index.js'));
  const Loader = (await import(join(workspace, 'node_modules/@deepseek-ai/cordis-plugin-loader/lib/index.js'))).default;
  const dshSkill = (await import(join(workspace, 'node_modules/@deepseek-ai/dsh-skill/lib/index.js'))).default;
  const dshSystemPrompt = (await import(join(workspace, 'node_modules/@deepseek-ai/dsh-system-prompt/lib/index.js'))).default;

  const root = new Context();
  await root.plugin(Loader);
  await root.plugin(dshSkill);
  await root.plugin(dshSystemPrompt);

  const id = await root.loader.create({ id: 'codex-noise-filter', name: BUNDLE_NAME });
  assert.equal(id, 'codex-noise-filter');
  await root.loader.await();
  const entry = root.loader.resolve(id);
  assert.ok(entry.fiber, 'patch 条目已导入并启动');
  console.log('✔ loader 条目导入并挂载:', id);

  const catalog = await root.skills.list({ cwd: process.cwd() });
  const summary = catalog.find((skill) => skill.name === 'codex-noise-filter');
  assert.ok(summary, '技能出现在合并目录');
  assert.equal(summary.invocation.modelInvocable, true);
  assert.equal(summary.invocation.userInvocable, true);
  assert.equal(summary.source, 'runtime');
  assert.equal(summary.resourceBase.kind, 'directory');
  console.log('✔ skills.list 摘要:', summary.name);

  const loaded = await root.skills.get('codex-noise-filter', { cwd: process.cwd() });
  assert.ok(loaded, '技能可按名称加载');
  assert.ok(loaded.content.trimStart().startsWith('# codex-noise-filter'));
  assert.ok(loaded.content.includes('references/00-index.md'));
  console.log('✔ skills.get 正文长度:', loaded.content.length);

  const assembly = await root.systemPrompt.assemble();
  const routing = assembly.contexts.find((context) => context.name === 'codex-noise-filter:routing');
  assert.ok(routing, '短路由进入系统提示装配');
  assert.ok(routing.text.length < 800);
  console.log('✔ systemPrompt 装配包含路由快照，长度:', routing.text.length);

  await entry.fiber.dispose();
  const after = await root.skills.list({ cwd: process.cwd() });
  assert.ok(!after.some((skill) => skill.name === 'codex-noise-filter'), '释放后技能注销');
  console.log('✔ dispose 后技能已清理');
  await root.fiber.dispose();
  console.log('E2E 通过');
} finally {
  rmSync(workspace, { recursive: true, force: true });
}
