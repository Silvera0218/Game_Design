---
name: balance-check
description: "分析游戏平衡数据文件、公式和配置，以识别异常值、破坏的进程、退化策略和经济失衡。修改任何与天平相关的数据或设计后使用。当用户说“平衡报告”、“检查游戏平衡”、“运行平衡检查”时使用。"
---

## 第一阶段：确定平衡域

从`$ARGUMENTS[0]`确定平衡域：

- **战斗** → weapon/ability DPS、击杀时间、伤害类型交互
- **经济** → 资源 faucets/sinks、获取率、物品定价
- **进展** → XP/power 曲线、死区、功率峰值
- **战利品** → 稀有度分布、怜悯计时器、库存压力
- **给定文件路径** → 直接加载该文件并从内容推断域

如果没有参数，询问用户要检查哪个系统。

---

## 第 2 阶段：Read 数据文件

来自 `assets/data/` 和 `design/balance/` 的 Read 相关文件用于已识别的域。
记下读取的每个文件 - 它们将出现在报告的“数据源”部分中。

---

## 第三阶段：Read 设计文档

Read GDD 用于从 `design/gdd/` 中了解预期的设计目标，
调谐旋钮和预期值范围。这是“正确”行为的基线。

---

## 第 4 阶段：执行分析

运行特定于域的检查：

**战斗平衡：**
- 计算每个功率层所有 weapons/abilities 的 DPS
- 检查每一层的杀戮时间
- 确定任何主导所有其他选项的选项（绝对更好）
- 检查防御选项是否可以创建不可杀死的状态
- 验证损坏 type/resistance 相互作用是否平衡

**经济平衡：**
- 绘制所有资源水龙头和水槽的流量图
- 项目资源随时间积累
- 检查无限资源循环
- 通过黄金生成验证黄金汇规模
- 检查是否有任何物品永远不值得购买

**进度平衡：**
- 绘制 XP 曲线和功效曲线
- 检查死区（太长时间没有有意义的进展）
- 检查功率峰值（能力突然跳跃）
- 验证内容门与预期的玩家能力相符
- 检查 skip/grind 策略是否打破预期节奏

**战利品余额：**
- 计算获得每个稀有度等级的预期时间
- 检查怜悯计时器数学
- 验证没有战利品在任何阶段都是完全无用的
- 检查库存压力与采购率

---

## 第 5 阶段：输出分析

```
## Balance Check: [System Name]

### Data Sources Analyzed
- [List of files read]

### Health Summary: [HEALTHY / CONCERNS / CRITICAL ISSUES]

### Outliers Detected
| Item/Value | Expected Range | Actual | Issue |
|-----------|---------------|--------|-------|

### Degenerate Strategies Found
- [Strategy description and why it is problematic]

### Progression Analysis
[Graph description or table showing progression curve health]

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|--------------|--------|

### Values That Need Attention
[Specific values with suggested adjustments and rationale]
```

---

## 第 6 阶段：修复和验证周期

提交报告后，询问：

> “您现在想解决这些平衡问题吗？”

If yes:
- 询问首先要解决哪个问题（请参阅按优先级排列的建议表）
- 指导用户更新`assets/data/`中的相关数据文件或`design/balance/`中的公式
- 每次修复后，建议重新运行相关的余额检查，以验证没有引入新的异常值
- 如果修复更改了 GDD 中定义的或由 ADR 引用的调谐旋钮，请提醒用户：
  > “该值在设计文档中定义。在受影响的 GDD 上运行 `/propagate-design-change [path]`，以在提交之前查找下游影响。”

If no:
- 总结未解决的问题并建议将报告保存到 `design/balance/balance-check-[system]-[date].md` 供以后使用

结束于：
> “修复后重新运行 `/balance-check` 进行验证。”
