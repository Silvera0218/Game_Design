---
name: security-audit
description: "审核游戏的安全漏洞：保存篡改、作弊向量、网络漏洞、数据暴露和输入验证差距。生成包含修复指导的优先安全报告。在任何公开发布或多人游戏启动之前运行。"
---

# 安全审计

对于任何已发行的游戏来说，安全性都不是可选的。即使是单人游戏也有
保存篡改向量。多人游戏有作弊表面、数据暴露
风险和拒绝服务的可能性。该技能系统地审核
针对最常见的游戏安全故障的代码库，并生成优先级
补救计划。

**运行此技能：**
- 在任何公开发布之前（波兰→发布门所需）
- 在启用任何 online/multiplayer 功能之前
- 在实现任何从磁盘或网络读取的系统之后
- 当报告与安全相关的错误时

**输出：** `production/security/security-audit-[date].md`

---

## 第一阶段：解析参数和范围

**Modes:**
- `full` — 所有类别（发布前推荐）
- `network` — 仅 network/multiplayer
- `save` — 仅保存文件和序列化
- `input` — 仅输入验证和注入
- `quick` — 仅高严重性检查（最快，用于迭代使用）
- 无参数 — 运行 `full`

Read `.codex/docs/technical-preferences.md` 确定：
- 引擎和语言（影响要搜索的模式）
- 目标平台（影响应用的攻击面）
- multiplayer/networking 是否在范围内

---

## 第 2 阶段：生成安全工程师

通过 Task 生成 `security-engineer`。通过：
- 审核scope/mode
- 来自技术偏好的引擎和语言
- 所有源目录的清单：`src/`、`assets/data/`、任何配置文件

安全工程师对 6 个类别进行审核（参见第 3 阶段）。在继续之前收集他们的完整调查结果。

---

## 第三阶段：审核类别

安全工程师评估以下各项。跳过不适用于项目范围的类别。

### 第 1 类：保存文件和序列化安全性
- 加载前是否验证保存文件？ （禁止盲目反序列化）
- 保存文件路径是根据用户输入构建的吗？ （路径遍历风险）
- 保存文件是否经过校验或签名？ （篡改检测）
- 游戏是否信任保存文件中的数值而不进行边界检查？
- 保存加载附近是否有任何 eval() 或动态代码执行调用？

Grep 模式：`File.open`、`load`、`deserialize`、`JSON.parse`、`from_json`、`read_file` — 检查每个模式是否有效。

### 第 2 类：网络和多人游戏安全（如果仅单人游戏，请跳过）
- 游戏状态是服务器上的权威，还是客户端决定结果？
- 传入网络数据包的大小、类型和值范围是否经过验证？
- 玩家位置和状态变化是否在服务器端得到验证？
- 任何网络调用是否有速率限制？
- 身份验证令牌是否正确处理（从不以明文形式发送）？
- 游戏是否在发布版本中公开任何调试端点？

Grep 用于：`recv`、`receive`、`PacketPeer`、`socket`、`NetworkedMultiplayerPeer`、`rpc`、`rpc_id` — 检查每个调用站点用于验证。

### 类别 3：输入验证
- 文件路径中是否使用了玩家提供的字符串？ （路径遍历）
- 是否有任何玩家提供的字符串未经清理就被记录？ （日志注入）
- 使用前是否对数字输入（例如物品数量、字符统计数据）进行边界检查？
- 在写入任何后端之前是否检查 achievement/stat 值？

Grep 用于：`get_input`、`Input.get_`、`input_map`、面向用户的文本字段 — 检查验证。

### 第 4 类：数据暴露
- 是否有任何 API 密钥、凭证或秘密硬编码在 `src/` 或 `assets/` 中？
- 发布版本中是否包含调试符号或详细错误消息？
- 游戏是否将敏感的玩家数据记录到磁盘或控制台？
- 是否有任何内部文件路径或系统信息暴露给玩家？

Grep 适用于：`api_key`、`secret`、`password`、`token`、`private_key`、`DEBUG`、`print(` 面向释放面代码。

### 第 5 类：作弊和防篡改向量
- 游戏关键值是否仅存储在内存中，而不是存储在易于编辑的文件中？
- 是否有任何关键的游戏进度标志（例如“已支付 DLC”）在服务器端进行了验证？
- 是否有针对多人游戏的内存编辑工具（Cheat Engine 等）的保护？
- leaderboard/score 提交内容在接受之前是否经过验证？

注意：客户端反作弊基本上无法执行。专注于任何竞争或货币化的服务器端验证。

### 第 6 类：依赖性和供应链
- 是否使用了任何第三方插件或库？列出它们。
- 正在使用的版本中是否有任何插件具有已知的 CVE？
- 插件来源是否经过验证（官方市场、经过审查的存储库）？

Glob for：`addons/`、`plugins/`、`third_party/`、`vendor/` — 列出所有外部依赖项。

---

## 第 4 阶段：对结果进行分类

对于每个发现，分配：

**Severity:**
| Level | Definition |
|-------|-----------|
| **CRITICAL** | 远程代码执行、数据泄露或可轻易利用的作弊行为会破坏多人游戏的完整性 |
| **HIGH** | 保存绕过进程、凭证暴露或服务器端权限绕过的篡改 |
| **MEDIUM** | 影响有限的客户端作弊、信息泄露或输入验证差距 |
| **LOW** | 纵深防御改进 - 强化可减少攻击面，但不存在直接利用 |

**状态：** 开放/已接受风险/超出范围

---

## 第五阶段：生成报告

```markdown
# Security Audit Report

**Date**: [date]
**Scope**: [full | network | save | input | quick]
**Engine**: [engine + version]
**Audited by**: security-engineer via /security-audit
**Files scanned**: [N source files, N config files]

---

## Executive Summary

| Severity | Count | Must Fix Before Release |
|----------|-------|------------------------|
| CRITICAL | [N] | Yes — all |
| HIGH | [N] | Yes — all |
| MEDIUM | [N] | Recommended |
| LOW | [N] | Optional |

**Release recommendation**: [CLEAR TO SHIP / FIX CRITICALS FIRST / DO NOT SHIP]

---

## CRITICAL Findings

### SEC-001: [Title]
**Category**: [Save / Network / Input / Data / Cheat / Dependency]
**File**: `[path]` line [N]
**Description**: [What the vulnerability is]
**Attack scenario**: [How a malicious user would exploit it]
**Remediation**: [Specific code change or pattern to apply]
**Effort**: [Low / Medium / High]

[repeat per finding]

---

## HIGH Findings

[same format]

---

## MEDIUM Findings

[same format]

---

## LOW Findings

[same format]

---

## Accepted Risk

[Any findings explicitly accepted by the team with rationale]

---

## Dependency Inventory

| Plugin / Library | Version | Source | Known CVEs |
|-----------------|---------|--------|------------|
| [name] | [version] | [source] | [none / CVE-XXXX-NNNN] |

---

## Remediation Priority Order

1. [SEC-NNN] — [1-line description] — Est. effort: [Low/Medium/High]
2. ...

---

## Re-Audit Trigger

Run `/security-audit` again after remediating any CRITICAL or HIGH findings.
The Polish → Release gate requires this report with no open CRITICAL or HIGH items.
```

---

## 第 6 阶段：Write 报告

在对话中呈现报告摘要（仅限执行摘要 + CRITICAL/HIGH 结果）。

问：“我可以将完整的安全审核报告写到 `production/security/security-audit-[date].md` 吗？”

Write 仅在批准后。

---

## 第 7 阶段：门集成

此报告是 **抛光 → 发布门** 所需的工件。

修复结果后，重新运行：`/security-audit quick` 以确认 CRITICAL/HIGH 项目在运行 `/gate-check release` 之前已解决。

如果存在关键发现：
> “⛔ 重要的安全发现必须在任何公开发布之前得到解决。在这些问题得到解决之前，请勿继续执行 `/launch-checklist`。”

如果没有 CRITICAL/HIGH 结果：
> “✅ 没有阻止安全发现。报告写入 `production/security/`。运行 `/gate-check release` 时包含此路径。”

---

## 协作协议

- **永远不要假设模式是安全的** - 标记它并让用户决定
- **接受的风险是一个有效的结果** - 对于单独的团队来说，一些低的结果是可以接受的权衡；记录决定
- **多人游戏有更高的标准** - 多人游戏环境中的任何高发现都应被视为关键
- **这不是渗透测试** - 此审核涵盖常见模式；在任何竞争性或货币化多人游戏发布之前，建议由人类安全专业人员进行真正的渗透测试
