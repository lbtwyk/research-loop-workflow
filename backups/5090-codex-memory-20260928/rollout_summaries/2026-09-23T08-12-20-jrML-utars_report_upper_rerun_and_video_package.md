thread_id: 01a0cd52-a44c-7b71-8c87-49b729abc493
updated_at: 2026-09-24T08:50:12+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T16-12-20-01a0cd52-a44c-7b71-8c87-49b729abc493.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# 更新 UTars 技术报告并用修复后推理重测上层任务

Rollout context: 在 `/home/wangyukun/ubt_isaac_sim_ws` 继续整理飞书技术报告。用户要求加入下层 7 条成功视频、1 条失败视频，以及上层成功率；随后明确要求使用最新、正确的推理 pipeline 重新评测上层，并表示“ 不用管严格，只要成功就行”。

## Task 1: 整理报告视频与成功率

Outcome: success

Preference signals:

- 用户要求“7个成功的和一个失败的下层视频，以及之前上层成功视频2个也放上去”，并在未指定上层视频路径时同意由助手从有完整记录的历史评测中选择 -> 类似报告任务应主动整理代表性成功/失败视频，并明确标注批次来源。
- 用户强调“上层的成功率也需要写” -> 报告应同时给出完整批次成功率和视频索引，不能用精选视频数量代替批次分母。

Key steps:

- 从 `actual_completion.json` 选择下层 7 个完整成功种子：`2026080507, 2026080510, 2026080517, 2026080519, 2026080520, 2026080601, 2026080605`。
- 选择下层失败样例 `2026080518`：已释放、未掉箱，但水平偏差 13.9 cm，超过 12 cm 完成阈值。
- 从历史同层评测选择两条无警告成功视频：种子 `2026080516`、`2026080517`，并注明它们属于较早模型，不代表当前模型。
- 创建 `视频索引.md`，为每个视频记录结果、种子、来源及成功率口径。

Reusable knowledge:

- 下层正式完整任务结果是 `7/40 = 17.5%`；抓起为 `39/40`。旧阶段评分不可替代完整完成率。
- 历史同层旧批次有阶段评分 `25/40`、严格阶段评分 `1/40`，但旧流程含倾斜限制和释放判定差异，不能直接称为完整任务成功率。

## Task 2: 使用修复后推理流程重测上层

Outcome: success

Preference signals:

- 用户纠正“新的推理才是对的”，并要求重新评测；随后说“不用管严格，只要成功就行啊” -> 评测主指标应采用“抓起、放回目标层、松手且未掉落”的完整任务完成率，抓起倾斜警告不应单独判失败。
- 用户说“不用一直等” -> 长时间后台评测应放入 tmux，并提供状态/收尾文件，不必持续阻塞等待。

Key steps:

- 使用本机保留的当前 6 万步模型：`ubt_vla_ws/ubt_vla_data/r01-old-new-lower-37mix-60k`。
- 创建评测目录 `0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/`，沿用此前 40 个固定场景种子、固定场景和 900 步上层时长。
- 启用修复后推理设置：8 次推理、8 步 RTC frozen prefix、RTC reference clipping、RTC 开启、每 16 个动作重规划；上层目标插值关闭。
- 先跑首条 smoke 验证：种子 `2026080501` 完成，432 个 applied actions，无 client error；随后后台完成全部 40 条。
- 完成后自动核验 40 个唯一种子、120 个原始 H.264 视频、无客户端错误，并运行报告/材料包更新脚本。

Reusable knowledge:

- 修复后上层同层完整任务结果：`13/40 = 32.5%`。
- 同一批次阶段评分为 `33/40`，但报告主指标使用用户指定的完整完成率 `13/40`。
- 40 条评测无 client error；120 段原始视频完成解码验证。
- 上层新评测成功视频选入材料包的种子为 `2026080501`、`2026080502`；旧历史成功视频仍保留并单独标注。

Failures and how to do differently:

- 初次收尾脚本因 `ffprobe` 不存在失败；改用 GR00T 环境中的 PyAV (`av 16.1.0`) 解码并验证 H.264，最终通过。
- 两次针对 `交接索引.md` 的 `apply_patch` 因上下文不匹配失败；改用 Python 文本替换后成功。未来修改中文报告文件时应先读取精确文本，再做窄范围替换。
- 不应把旧批次 `1/40` 严格阶段评分写成完整成功率；报告已改为区分阶段评分与完整任务成功率。

References:

- 报告主稿：`docs/briefs/utars-techreport-20260922/REPORT.md`
- 飞书正文副本：`docs/briefs/utars-techreport-20260922/飞书正文.md`
- 视频索引：`docs/briefs/utars-techreport-20260922/视频索引.md`
- 材料包：`docs/briefs/utars-techreport-20260922/UTars飞书交接材料.zip`
- 上层评测结果：`0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/actual_completion.json`
- 上层评测报告：`0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/REPORT.md`
- 上层评测 manifest：`0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/manifest.json`
- 收尾状态：`0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/STATUS.md`
- 最终验证：材料包 20 个文件、12 段视频、ZIP `testzip()` 通过；Markdown 副本一致，报告/索引/README 本地链接无断链。
