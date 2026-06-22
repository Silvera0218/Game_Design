---
name: asset-audit
description: "审核游戏资产是否符合命名约定、文件大小预算、格式标准和管道要求。识别孤立资产、缺失引用和违反标准的情况。"
# 仅 Read 诊断技能 — 无需专业代理委派
---

## 第一阶段：Read 标准

Read 相关设计文档中的艺术圣经或资产标准以及 AGENTS.md 命名约定。

---

## 第 2 阶段：扫描资产目录

使用Glob扫描目标资产目录：

- `assets/art/**/*` 用于艺术资产
- `assets/audio/**/*` 用于音频资产
- `assets/vfx/**/*` 用于 VFX 资产
- `assets/shaders/**/*` 用于着色器
- `assets/data/**/*` 用于数据文件

---

## 第 3 阶段：运行合规性检查

**命名约定：**
- 艺术：`[category]_[name]_[variant]_[size].[ext]`
- 音频：`[category]_[context]_[name]_[variant].[ext]`
- 所有文件必须小写并带下划线

**文件标准：**
- 纹理：二维的幂，正确的格式（UI 的 PNG，压缩为 3D），在尺寸预算内
- 音频：正确的采样率、格式（SFX 为 OGG，音乐为 OGG/MP3），在持续时间限制内
- 数据：有效 JSON/YAML，符合架构

**孤立资产：** 搜索代码以获取对每个资产文件的引用。标记任何没有引用的内容。

**缺少资产：** 搜索代码以查找资产引用并验证文件是否存在。

---

## 第四阶段：输出审核报告

```markdown
# Asset Audit Report -- [Category] -- [Date]

## Summary
- **Total assets scanned**: [N]
- **Naming violations**: [N]
- **Size violations**: [N]
- **Format violations**: [N]
- **Orphaned assets**: [N]
- **Missing assets**: [N]
- **Overall health**: [CLEAN / MINOR ISSUES / NEEDS ATTENTION]

## Naming Violations
| File | Expected Pattern | Issue |
|------|-----------------|-------|

## Size Violations
| File | Budget | Actual | Overage |
|------|--------|--------|---------|

## Format Violations
| File | Expected Format | Actual Format |
|------|----------------|---------------|

## Orphaned Assets (no code references found)
| File | Last Modified | Size | Recommendation |
|------|-------------|------|---------------|

## Missing Assets (referenced but not found)
| Reference Location | Expected Path |
|-------------------|---------------|

## Recommendations
[Prioritized list of fixes]

## Verdict: [COMPLIANT / WARNINGS / NON-COMPLIANT]
```

该技能是只读的 - 它生成报告但不写入文件。

---

## 第五阶段：后续步骤

- 使用 AGENTS.md 中定义的模式修复命名违规。
- 人工审核后删除确认的孤立资产。
- 运行 `/content-audit` 以根据 GDD 指定的要求交叉检查资产计数。
