---
name: launch-checklist
description: "完整的发布准备验证涵盖每个部门：代码、内容、商店、营销、社区、基础设施、法律和 go/no-go 签名。"
---

> **仅显式调用**：此技能仅应在用户使用 `/launch-checklist` 显式请求时运行。不要根据上下文匹配自动调用。

## 第一阶段：解析参数

Read 启动日期或 `dry-run` 模式的参数。空运行模式会生成清单，无需创建签核条目或写入文件。

---

## 第 2 阶段：收集项目背景

- Read `AGENTS.md` 用于技术堆栈、目标平台和团队结构
- Read `production/milestones/` 的最新里程碑
- Read `production/releases/` 中任何现有的发布清单
- Read `design/live-ops/content-calendar.md` 中的内容日历（如果存在）

---

## 第 3 阶段：扫描代码库健康状况

- 统计 `TODO`、`FIXME`、`HACK` 评论及其位置
- 检查生产代码中是否存在任何 `console.log`、`print()` 或调试输出
- 检查占位符资源（搜索 `placeholder`、`temp_`、`WIP_`）
- 检查硬编码的 test/dev 值（本地主机、测试凭据、调试标志）

---

## 第 4 阶段：生成启动清单

```markdown
# Launch Checklist: [Game Title]
Target Launch: [Date or DRY RUN]
Generated: [Date]

---

## 1. Code Readiness

### Build Health
- [ ] Clean build on all target platforms
- [ ] Zero compiler warnings
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Performance benchmarks within targets
- [ ] No memory leaks (verified via extended soak test)
- [ ] Build size within platform limits
- [ ] Build version correctly set and tagged in source control

### Code Quality
- [ ] TODO count: [N] (zero required for launch, or documented exceptions)
- [ ] FIXME count: [N] (zero required)
- [ ] HACK count: [N] (each must have documented justification)
- [ ] No debug output in production code
- [ ] No hardcoded dev/test values
- [ ] All feature flags set to production values
- [ ] Error handling covers all critical paths
- [ ] Crash reporting integrated and verified

### Security
- [ ] No exposed API keys or credentials in source
- [ ] Save data encrypted
- [ ] Network communication secured (TLS/DTLS)
- [ ] Anti-cheat measures active (if multiplayer)
- [ ] Input validation on all server endpoints (if multiplayer)
- [ ] Privacy policy compliance verified

---

## 2. Content Readiness

### Assets
- [ ] All placeholder art replaced with final assets
- [ ] All placeholder audio replaced with final audio
- [ ] Audio mix finalized and approved by audio director
- [ ] All VFX polished and performance-verified
- [ ] No missing or broken asset references
- [ ] Asset naming conventions enforced

### Text and Localization
- [ ] All player-facing text proofread
- [ ] No hardcoded strings (all externalized for localization)
- [ ] All supported languages translated and verified
- [ ] Text fits UI in all languages (text fitting pass complete)
- [ ] Font coverage verified for all supported languages
- [ ] Credits complete, accurate, and up to date

### Game Content
- [ ] All levels/maps playable from start to finish
- [ ] Tutorial flow complete and tested with new players
- [ ] All achievements/trophies implemented and tested
- [ ] Save/load works correctly for all game states
- [ ] Difficulty settings balanced and tested
- [ ] End-game/credits sequence complete

---

## 3. Quality Assurance

### Testing
- [ ] Full regression test suite passed
- [ ] Zero S1 (Critical) bugs open
- [ ] Zero S2 (Major) bugs open (or documented exceptions)
- [ ] Soak test passed (8+ hours continuous play)
- [ ] Multiplayer stress test passed (if applicable)
- [ ] All critical user paths tested on every platform
- [ ] Edge cases tested (full storage, no network, suspend/resume)

### Platform Certification
- [ ] PC: Steam/Epic/GOG SDK requirements met
- [ ] Console: TRC/TCR/Lotcheck submission prepared
- [ ] Mobile: App Store/Play Store guidelines compliant
- [ ] Accessibility: minimum standards met (remapping, text scaling, colorblind)
- [ ] Age ratings obtained (ESRB, PEGI, regional)

### Performance
- [ ] Target FPS met on minimum spec hardware
- [ ] Load times within budget on all platforms
- [ ] Memory usage within budget on all platforms
- [ ] Network bandwidth within targets (if multiplayer)
- [ ] No frame hitches in critical gameplay moments

---

## 4. Store and Distribution

### Store Pages
- [ ] Store page copy finalized and proofread
- [ ] Screenshots current and per-platform resolution
- [ ] Trailers current and approved
- [ ] Key art and capsule images finalized
- [ ] System requirements accurate (PC)
- [ ] Pricing configured for all regions
- [ ] Pre-purchase/wishlist campaigns active (if applicable)

### Legal
- [ ] EULA finalized and approved by legal
- [ ] Privacy policy published and linked
- [ ] Third-party license attributions complete
- [ ] Music/audio licensing verified
- [ ] Trademark/IP clearance confirmed
- [ ] GDPR/CCPA compliance verified (data collection, consent, deletion)

---

## 5. Infrastructure

### Servers (if multiplayer/online)
- [ ] Production servers provisioned and load-tested
- [ ] Auto-scaling configured and tested
- [ ] Database backups configured
- [ ] CDN configured for content delivery
- [ ] DDoS protection active
- [ ] Monitoring and alerting configured

### Analytics and Monitoring
- [ ] Analytics pipeline verified and receiving data
- [ ] Crash reporting active and dashboard accessible
- [ ] Server monitoring dashboards live
- [ ] Key metrics tracked: DAU, session length, retention, crashes
- [ ] Alerts configured for critical thresholds

---

## 6. Community and Marketing

### Community Readiness
- [ ] Community guidelines published
- [ ] Moderation team briefed and tools ready
- [ ] Discord/forum/social channels set up
- [ ] FAQ and known issues page prepared
- [ ] Support email/ticketing system active

### Marketing
- [ ] Launch trailer published
- [ ] Press/influencer review keys distributed
- [ ] Social media launch posts scheduled
- [ ] Launch day blog post/dev update drafted
- [ ] Patch notes for launch version published

---

## 7. Operations

### Team Readiness
- [ ] On-call schedule set for first 72 hours post-launch
- [ ] Incident response playbook reviewed by team
- [ ] Rollback plan documented and tested
- [ ] Hotfix pipeline tested (can ship emergency fix within 4 hours)
- [ ] Communication plan for launch issues (who posts, where, how fast)

### Day-One Plan
- [ ] Day-one patch prepared (if needed)
- [ ] Server unlock/go-live procedure documented
- [ ] Launch monitoring dashboard bookmarked by all leads
- [ ] War room/channel established for launch day

---

## Go / No-Go Decision

**Overall Status**: [READY / NOT READY / CONDITIONAL]

### Blocking Items
[List any items that must be resolved before launch]

### Conditional Items
[List items that have documented workarounds or accepted risk]

### Sign-Offs Required
- [ ] Creative Director — Content and experience quality
- [ ] Technical Director — Technical health and stability
- [ ] QA Lead — Quality and test coverage
- [ ] Producer — Schedule and overall readiness
- [ ] Release Manager — Build and deployment readiness
```

---

## 第 5 阶段：保存清单

向用户呈现已完成的清单和摘要（总项目、阻塞项目计数、条件项目计数、不完整部分的部门）。

如果未处于空运行模式，请询问：“我可以将其写入 `production/releases/launch-checklist-[date].md` 吗？”

如果是，则写入文件，并根据需要创建目录。

---

## 第六阶段：后续步骤

- 在启动前运行 `/gate-check` 以获取正式的 PASS/CONCERNS/FAIL 判决。
- 通过 `/team-release` 协调签核。
