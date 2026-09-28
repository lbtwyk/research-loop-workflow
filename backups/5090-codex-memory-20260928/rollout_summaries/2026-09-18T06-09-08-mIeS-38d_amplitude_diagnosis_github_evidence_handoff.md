thread_id: 01a0b322-0e7f-7213-b849-6b547c81ba6a
updated_at: 2026-09-18T08:23:58+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T14-09-08-01a0b322-0e7f-7213-b849-6b547c81ba6a.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# 38D 最新主线动作幅度诊断并完成 GitHub/Web 交接

Rollout context: 在 `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance` 分析用户指出的“最新 38D 主线跳舞幅度小于 34D”问题，随后将证据同步到私有 GitHub 并交给 Web 决策。

## Task 1: 诊断 34D 与最新 38D 的动作幅度差异

Outcome: success

Preference signals:

- 用户明确说明问题来自“最新的 38d 主线”，因此后续比较应优先针对最新 AM/AJ FHC 生成器，而不是笼统归因于最初 38D 表示切换。
- 用户要求“分析是什么导致了这个问题，是38d的问题还是训练出了问题”，说明需要区分表示、codec 还原、生成训练、音乐条件、历史状态和渲染，不能只看综合分数。
- 用户后来要求“实验 证据要传上”，并说明“视频不需要，其他的日志啥的可以” -> 后续交接应上传可复核的测量、日志、脚本、动作记录和静态图，但不上传视频。

Key steps:

- 审计 `EXP-20260904-g1-yaw-anchor-abs-6d` 和 `EXP-20260904-v6f-aq-tmmr-direct-condition`，确认 38D yaw-anchor absolute + B71 是接受的正式表示；34D 只作为内部历史基线。
- 对 18 首 FineDance 测试音乐、24 秒统一窗口、3 个采样 seed、model-preroll 与真实 K64 history 两种启动协议完成 324 段主比较；另完成 57 段音乐/训练 seed/状态控制和两种 codec 的 18 首重建检查。
- 验证表示转换、关节归一化、codec round-trip、官方加载入口与渲染前动作数据；生成动作直接使用保存的关节数据，未发现渲染缩放或表示转换造成的统一幅度压缩。
- 生成并验证 9 条本地视频（每条 720 帧、共 6480 帧），但按用户要求未上传远端。

Reusable knowledge:

- 38D codec 本身能够保留大动作：18 首重建中 34D range/speed 为 96.6%/90.6%，38D 为 97.3%/97.2%，38D 平均关节误差 3.58° 对 34D 的 4.60° 更低；因此低幅度主要出现在自主生成阶段，不是 38D“装不下”动作。
- 全体均值不是全面崩溃：model-preroll 下 34D/38D AM/38D AJ 的关节范围为 77.3%/75.1%/75.4%，速度为 72.9%/69.3%/69.8%；整体 range 和 speed 的 paired 95% 区间均跨零。
- 更一致的差异是 root-local 手腕/脚踝活动范围：model-preroll AM−34D 为 -6.3 个百分点（95% CI [-10.1,-2.2]），AJ−34D 为 -5.3（[-8.2,-2.7]），两者各有 15/18 首低于 34D。
- 036 是明确失败例：model-preroll 下 34D range/speed=53.0%/42.3%，38D AM=28.1%/15.0%，38D AJ=38.5%/26.0%；063 是反例，38D 仍能产生大动作，098 表明范围尚可但速度不足。
- 更准确的未来音乐特征没有修复 036；去掉音乐反而可能让动作更活跃，但不同歌曲方向不一致，因此不能把音乐预测器升级或无音乐作为已证实修复。
- 036 的低活跃现象在 AM/AJ 各三个训练 seed 中重复，说明不是单个 checkpoint 偶然失败；但额外 seed 只覆盖 3 首歌，不能外推为完整 18 首重复实验。
- 生成 latent 伴随低活跃：036 原始 38D q0 重复率约 14.5%，生成 AM/AJ 约 41.8%/25.3%，残差 RMS 从约 0.708 降至 0.224/0.309；这是机制线索，不是跨 codec 的直接质量指标。
- 注入真实状态可恢复段内动作，但造成约 5× 的边界速度跳变，因此不能作为修复方案。
- 结论应保持为：问题更指向自主生成阶段的保守动作和长时间自回归历史维持能力；尚不能唯一归因于 38D 维度、某个 loss、训练步数或训练错误。保留 38D 完整朝向目标，下一步应由用户/Web 选择一个受控的 generator-side intervention 或先做严格 34D/38D 训练消融。

References:

- `docs/experiments/reviews/EXP-20260904-v6f-aq-tmmr-direct-condition-amplitude-audit-20260918.md`
- `runs/amplitude_audit_20260918/analysis/summary.json`
- `runs/amplitude_audit_20260918/analysis/all_324_clips.csv`
- `runs/amplitude_audit_20260918/analysis/fixed_landmarks.json`
- `runs/amplitude_audit_20260918/completion.json`
- `docs/experiments/reviews/EXP-20260904-g1-yaw-anchor-abs-6d-acceptance.md`

## Task 2: GitHub evidence handoff and Web decision entry

Outcome: success

Preference signals:

- 用户要求“更新到github远端，让web端看到所有信息然后给出决策”，随后明确“实验 证据要传上”以及“不需要视频，其他的日志啥的可以” -> GitHub 交接应以完整可复核证据和明确决策问题为中心，不只上传结论文字，也不上传视频。

Key steps:

- 创建分支 `codex/38d-amplitude-audit-20260918`，提交诊断报告、Web decision packet 和实验 spec/ledger 更新。
- 远端 PR：`https://github.com/lbtwyk/Musics2Dance/pull/54`。
- Web 决策 Issue：`https://github.com/lbtwyk/Musics2Dance/issues/53`，标记为 `researchos:waiting-web`。
- 私有证据 release：`https://github.com/lbtwyk/Musics2Dance/releases/tag/amplitude-audit-20260918`，共 13 个附件、约 206 MB，digest 已核对；没有视频附件。
- 在原 Issue #49 留下交叉链接：`https://github.com/lbtwyk/Musics2Dance/issues/49#issuecomment-5727284633`。
- 实验 ledger 保持 `closed/accepted`，未启动新训练、未改变科学结论；更新了 latest artifact 和 next action 指向 Web 决策。

Failures and how to do differently:

- GitHub 大附件上传经代理多次超时；最终通过直连/绕过代理并用 GitHub upload API 验证 digest 完成。未来上传大附件应优先验证代理连接，必要时使用直连 API，并逐个核对 asset size/digest。
- 初始交接包包含视频，用户明确不需要后已删除 release 中视频和 gallery，并同步修改报告、README、证据 archive 与 publication scope。未来应在打包前先确认用户是否需要视频。
- Git commit 初次因未配置身份失败，随后使用 `Yukun Wang` 与 `186519092+lbtwyk@users.noreply.github.com` 完成 scoped commit。

Reusable knowledge:

- 研究交接应将观察、解释和决策请求分开；不要自动替用户接受/拒绝路线或启动重训。
- 交接包保留了 381 个 per-clip JSON、motion traces、日志、诊断脚本、source snapshot、CSV/JSON 汇总、静态图和历史对照资料；没有上传原始数据、checkpoint、credential 或视频。
- 最终远端发布记录：commit `1894755f16caf244b405be8d8a831bffbbe5c6e4`，`assets=13`，`all_digests_verified=true`，`issue_waiting_web=true`，`no_video_assets=true`，`training_launched=false`。

References:

- PR #54: `https://github.com/lbtwyk/Musics2Dance/pull/54`
- Decision issue #53: `https://github.com/lbtwyk/Musics2Dance/issues/53`
- Release: `https://github.com/lbtwyk/Musics2Dance/releases/tag/amplitude-audit-20260918`
- Branch: `codex/38d-amplitude-audit-20260918`
- Commit: `1894755f16caf244b405be8d8a831bffbbe5c6e4`

