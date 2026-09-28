thread_id: 01a0c869-924b-71d0-9a4b-caf03d445046
updated_at: 2026-09-24T05:57:11+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T17-19-17-01a0c869-924b-71d0-9a4b-caf03d445046.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# UTars/Isaac Sim/VLA 技术交接报告制作与证据补充

Rollout context: 工作目录为 `/home/wangyukun/ubt_isaac_sim_ws`。用户要制作仅覆盖 UTars / Isaac Sim / VLA 的飞书云文档式 tech report，面向下一位接手人，重点说明已补齐的能力、方法 intent 和最终版本，不展开中间迭代或大量不足。

## Task 1: 确定报告范围、篇幅与叙事重点

Outcome: success

Preference signals:
- 用户明确选择“只写 UTars / Isaac Sim / VLA”，排除 Musics2Dance -> 后续报告范围必须保持在仿真数据采集、VLA 训练与闭环验证。
- 用户纠正“太多了，只要几页”“按最终的版本来，不用讲中间迭代的版本” -> 默认采用 3 页左右、最终方案导向的精简结构，避免历史流水账。
- 用户要求“不足要少说，挑重点的贡献说，比如原来我接手的时候没有的东西现在做完了就说这些部分” -> 重点写接手前缺失、完成后的能力和保留的交接资产；不足只保留影响接手的必要边界。
- 用户要求统一“原来缺什么 → 你补了什么 → 现在能做什么”的表达，并准备做成飞书云文档 -> 输出应直接可粘贴，使用简洁标题、图表/视频链接和交接入口。

Key steps:
- 查阅 `HANDOFF.md`、`docs/workspace-status.md`、实验 spec、采集简报和评测报告，归纳自动数据生成、VLA 训练/执行、闭环验证三条主线。
- 将报告压缩为三页结构：自动生成搬箱示范、从仿真数据到 VLA 自主执行、验证与交接成果。
- 识别可视化素材：场景总览、规划流程、调平/阶段截图、成功失败对照、结果表和视频链接。

Reusable knowledge:
- 主工作区：`/home/wangyukun/ubt_isaac_sim_ws`；主要 SDG repo：`syntheticdatageneration`；实验资料集中在 `docs/experiments/`，日志和视频集中在 `0.logs/`。
- 适合报告正文的已完成能力包括：自动搬箱示范生成、下层搬运中的 hold-and-level、HDF5 数据质量筛选、GR00T N1.7 接入与闭环评测、执行/测量问题的对照诊断。

References:
- `/home/wangyukun/ubt_isaac_sim_ws/docs/briefs/handlingbox-data-collection-brief-20260722/README.md`
- `/home/wangyukun/ubt_isaac_sim_ws/docs/experiments/EXP-20260708-utars-sdg-data-collection.md`
- `/home/wangyukun/ubt_isaac_sim_ws/docs/experiments/EXP-20260902-utars-groot-n17-old-upper-new-lower-37mix.md`

## Task 2: 生成正式报告与飞书材料包

Outcome: success

Key steps:
- 生成正式 Markdown 主稿和配套材料包，内容补充了关键机制、公式、论文/软件环境信息及证据链接。
- 验证报告中本地链接无 broken links，Markdown 副本一致，证据引用齐全；材料包共 8 个文件、约 5.5 MB。
- 交付入口为：`docs/briefs/utars-techreport-20260922/REPORT.md` 和 `docs/briefs/utars-techreport-20260922/UTars飞书交接材料.zip`。

Reusable knowledge:
- 最终报告以 Markdown 为准，旧 Word/PDF 不再更新。
- 报告应以最终方案和交接价值为主，而不是罗列所有历史尝试；完整参数和实验流水线可通过现有 spec/log 链接追溯。

References:
- `REPORT.md broken local links: []`
- `飞书正文.md broken local links: []`
- `交接索引.md broken local links: []`
- `环境记录.md broken local links: []`
- `README.md broken local links: []`
- `matching Markdown copies: True`
- `contains all evidence refs: True`

## Task 3: 提供两个掉箱视频下载路径

Outcome: success

Key steps:
- 从同一批 `20260918_success_first_8f8_lower_40ep` 模型评测中选取 episode 001 和 002，均有 `box_dropped_during_sequence` 警告。
- 用户随后要求“给路径，我下载”，已直接返回绝对路径。

References:
- `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/same_shelf_lower_level/runs/full_policy/merged/videos/episode_001/combined.mp4`
- `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/same_shelf_lower_level/runs/full_policy/merged/videos/episode_002/combined.mp4`

## Task 4: 解释“训推不一致”并判断是否解决

Outcome: uncertain

Failures and how to do differently:
- 用户最后询问“训推不一致是什么问题，解决了吗”，rollout 在助手回答前结束，因此不能把该问题视为已解决。未来应明确解释训练数据动作语义、推理时动作衔接/参考状态、控制频率和延迟预算之间的差异，并给出“已修复部分”和“仍未证明”的区分。

Reusable knowledge:
- 已验证的训练/推理一致性问题：N1.7 相对 arm action 需相对当前参考状态解码；RTC continuation 必须把上一段绝对动作转换到新参考、保留实际执行前缀，并按推理延迟规划。旧参考复用会造成 jitter/target drift。
- 已完成的非模型执行修复包括动作接续、状态时钟、位置归一化、底盘/关节同 tick、生效 reset offset、支撑与放置分离测量等；独立复核 PASS，59 项回归测试通过，57 个视频完整解码。
- 但正式下层 40 次评测在 8/frozen8 候选下实际完成仍为 7/40，且 2026-09-22 物理抖动诊断显示阻尼可降低局部物理粗糙度但自主策略候选未改善任务成功率。因此不能简单声称“训推不一致已完全解决”或把剩余失败全部归因于模型。

References:
- `0.logs/n17_v3_execution_closure_20260917/REPORT.md`
- `0.logs/n17_v3_physics_rootcause_20260922/REPORT.md`
- `0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/REPORT.md`
- `docs/experiments/EXP-20260902-utars-groot-n17-old-upper-new-lower-37mix.md`
