---
name: release-checklist
description: "生成全面的预发布验证清单，涵盖构建验证、认证要求、存储元数据和发布准备情况。"
---

> **仅显式调用**：此技能仅应在用户使用 `/release-checklist` 显式请求时运行。不要根据上下文匹配自动调用。

## 第一阶段：解析参数

Read 目标平台的参数（`pc`、`console`、`mobile` 或 `all`）。如果未指定平台，则默认为 `all`。

---

## 第 2 阶段：加载项目上下文

- Read `AGENTS.md` 用于项目上下文、版本信息和平台目标。
- Read 从 `production/milestones/` 的当前里程碑可以了解此版本中应包含哪些功能和内容。

---

## 第 3 阶段：扫描代码库

扫描未解决的问题：

- 统计 `TODO` 评论
- 统计 `FIXME` 条评论
- 统计 `HACK` 条评论
- 注意它们的位置和严重程度

检查任何测试输出目录或 CI 日志中的测试结果（如果有）。

---

## 第 4 阶段：生成发布清单

```markdown
## Release Checklist: [Version] -- [Platform]
Generated: [Date]

### Codebase Health
- TODO count: [N] ([list top 5 if many])
- FIXME count: [N] ([list all -- these are potential blockers])
- HACK count: [N] ([list all -- these need review])

### Build Verification
- [ ] Clean build succeeds on all target platforms
- [ ] No compiler warnings (zero-warning policy)
- [ ] All assets included and loading correctly
- [ ] Build size within budget ([target size])
- [ ] Build version number correctly set ([version])
- [ ] Build is reproducible from tagged commit

### Quality Gates
- [ ] Zero S1 (Critical) bugs
- [ ] Zero S2 (Major) bugs -- or documented exceptions with producer approval
- [ ] All critical path features tested and signed off by QA
- [ ] Performance within budgets:
  - [ ] Target FPS met on minimum spec hardware
  - [ ] Memory usage within budget
  - [ ] Load times within budget
  - [ ] No memory leaks over extended play sessions
- [ ] No regression from previous build
- [ ] Soak test passed (4+ hours continuous play)

### Content Complete
- [ ] All placeholder assets replaced with final versions
- [ ] All TODO/FIXME in content files resolved or documented
- [ ] All player-facing text proofread
- [ ] All text localization-ready (no hardcoded strings)
- [ ] Audio mix finalized and approved
- [ ] Credits complete and accurate
```

根据参数添加特定于平台的部分：

**For `pc`:**
```markdown
### Platform Requirements: PC
- [ ] Minimum and recommended specs verified and documented
- [ ] Keyboard+mouse controls fully functional
- [ ] Controller support tested (Xbox, PlayStation, generic)
- [ ] Resolution scaling tested (1080p, 1440p, 4K, ultrawide)
- [ ] Windowed, borderless, and fullscreen modes working
- [ ] Graphics settings save and load correctly
- [ ] Steam/Epic/GOG SDK integrated and tested
- [ ] Achievements functional
- [ ] Cloud saves functional
- [ ] Steam Deck compatibility verified (if targeting)
```

**对于 `console`：**
```markdown
### Platform Requirements: Console
- [ ] TRC/TCR/Lotcheck requirements checklist complete
- [ ] Platform-specific controller prompts display correctly
- [ ] Suspend/resume works correctly
- [ ] User switching handled properly
- [ ] Network connectivity loss handled gracefully
- [ ] Storage full scenario handled
- [ ] Parental controls respected
- [ ] Platform-specific achievement/trophy integration tested
- [ ] First-party certification submission prepared
```

**对于 `mobile`：**
```markdown
### Platform Requirements: Mobile
- [ ] App store guidelines compliance verified
- [ ] All required device permissions justified and documented
- [ ] Privacy policy linked and accurate
- [ ] Data safety/nutrition labels completed
- [ ] Touch controls tested on multiple screen sizes
- [ ] Battery usage within acceptable range
- [ ] Background behavior correct (pause, resume, terminate)
- [ ] Push notification permissions handled correctly
- [ ] In-app purchase flow tested (if applicable)
- [ ] App size within store limits
```

**存储和发布部分（所有平台）：**
```markdown
### Store / Distribution
- [ ] Store page metadata complete and proofread
  - [ ] Short description
  - [ ] Long description
  - [ ] Feature list
  - [ ] System requirements (PC)
- [ ] Screenshots up to date and per-platform resolution requirements met
- [ ] Trailers up to date
- [ ] Key art and capsule images current
- [ ] Age rating obtained and configured:
  - [ ] ESRB
  - [ ] PEGI
  - [ ] Other regional ratings as required
- [ ] Legal notices, EULA, and privacy policy in place
- [ ] Third-party license attributions complete
- [ ] Pricing configured for all regions

### Launch Readiness
- [ ] Analytics / telemetry verified and receiving data
- [ ] Crash reporting configured and dashboard accessible
- [ ] Day-one patch prepared and tested (if needed)
- [ ] On-call team schedule set for first 72 hours
- [ ] Community launch announcements drafted
- [ ] Press/influencer keys prepared for distribution
- [ ] Support team briefed on known issues and FAQ
- [ ] Rollback plan documented (if critical issues found post-launch)

### Go / No-Go: [READY / NOT READY]

**Rationale:**
[Summary of readiness assessment. List any blocking items that must be
resolved before launch. If NOT READY, list the specific items that need
resolution and estimated time to address them.]

**Sign-offs Required:**
- [ ] QA Lead
- [ ] Technical Director
- [ ] Producer
- [ ] Creative Director
```

---

## 第 5 阶段：保存清单

向用户提供清单，其中包括：清单项目总数、已知阻止程序的数量（FIXME/HACK 计数、已知错误）。

问：“我可以把这个写到`production/releases/release-checklist-[version].md`吗？”

如果是，则写入文件，并根据需要创建目录。

---

## 第六阶段：后续步骤

- 在继续发布之前，运行 `/gate-check` 以获得正式的阶段门裁决。
- 通过 `/team-release` 协调最终签核。
