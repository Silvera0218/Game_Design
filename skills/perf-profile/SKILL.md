---
name: perf-profile
description: "结构化的性能分析工作流程。识别瓶颈，根据预算采取措施，并生成具有优先级排名的优化建议。"
---

## 第一阶段：确定范围

Read 参数：

- 系统名称 → 重点分析该特定系统
- `full` → 在所有系统上运行全面的配置文件

---

## 第 2 阶段：负载性能预算

检查设计文档或 AGENTS.md 中的现有性能目标：

- 目标 FPS（例如，60fps = 16.67ms 帧预算）
- 内存预算（总计和每个系统）
- 加载时间目标
- 绘制通话预算
- 网络带宽限制（如果是多人游戏）

---

## 第 3 阶段：分析代码库

**CPU 分析目标：**
- `_process()` / `Update()` / `Tick()` 功能 — 列出所有功能并估算成本
- 大型集合上的嵌套循环
- 热路径中的字符串操作
- 每帧代码中的分配模式
- 游戏实体上未优化的 search/sort
- 每帧昂贵的物理查询（光线投射、重叠）

**内存分析目标：**
- 大数据结构及其增长模式
- Texture/asset 内存占用估计
- 对象池与 instantiate/destroy 模式
- 泄漏的引用（应该释放但没有释放的对象）
- 缓存大小和驱逐策略

**渲染目标（如果适用）：**
- 绘制调用估计
- 从重叠的透明对象中过度绘制
- 着色器复杂性
- 未优化的粒子系统
- 缺少 LOD 或遮挡剔除

**I/O Targets:**
- Save/load性能
- 资源加载模式（同步与异步）
- 网络消息频率和大小

---

## 第 4 阶段：生成分析报告

```markdown
## Performance Profile: [System or Full]
Generated: [Date]

### Performance Budgets
| Metric | Budget | Estimated Current | Status |
|--------|--------|-------------------|--------|
| Frame time | [16.67ms] | [estimate] | [OK/WARNING/OVER] |
| Memory | [target] | [estimate] | [OK/WARNING/OVER] |
| Load time | [target] | [estimate] | [OK/WARNING/OVER] |
| Draw calls | [target] | [estimate] | [OK/WARNING/OVER] |

### Hotspots Identified
| # | Location | Issue | Estimated Impact | Fix Effort |
|---|----------|-------|------------------|------------|

### Optimization Recommendations (Priority Order)
1. **[Title]** — [Description]
   - Location: [file:line]
   - Expected gain: [estimate]
   - Risk: [Low/Med/High]
   - Approach: [How to implement]

### Quick Wins (< 1 hour each)
- [Simple optimization 1]

### Requires Investigation
- [Area that needs actual runtime profiling to confirm impact]
```

输出带有摘要的报告：前 3 个热点、估计的净空与预算以及建议的下一步行动。

---

## 第五阶段：范围和时间表决策

仅当任何热点的修复工作量评级为 M 或 L 时才激活此阶段。

呈现重要的项目并要求用户为每个项目进行选择：

- **A) 实施优化**（立即修复或安排修复）
- **B) 缩小功能范围**（运行 `/scope-check [feature]` 来分析权衡）
- **C) 接受性能影响并推迟到完善阶段**（记录为已知问题）
- **D) 上报给技术总监以做出架构决策**（运行 `/architecture-decision`）

如果多个项目推迟到波兰语（选择 C），请将它们记录在 `### Deferred to Polish` 下。

该技能是只读的——不写入任何文件。结论：**完成** — 生成性能配置文件。

---

## 第六阶段：后续步骤

- 如果瓶颈需要架构更改：运行 `/architecture-decision`。
- 如果需要缩小范围：运行 `/scope-check [feature]`。
- 要安排优化：运行 `/sprint-plan update`。

### Rules
- 在没有首先测量的情况下永远不要优化——对性能的直觉是不可靠的
- 建议必须包括估计的影响——“让它更快”是不可行的
- 目标硬件上的配置文件，而不仅仅是开发机器
- 静态分析（此技能）识别候选人；运行时分析确认
