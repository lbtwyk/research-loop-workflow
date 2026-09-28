thread_id: 01a0c36e-f518-7801-8bb2-f9ca761f5cdd
updated_at: 2026-09-24T06:27:09+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T21-19-48-01a0c36e-f518-7801-8bb2-f9ca761f5cdd_01a0c41f-6c44-7be2-a94e-094e4d91055f.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# 审核 causal-native 训练路线并验证音乐未来校准是否会被绕过

Rollout context: 在 `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance` 中，用户担心校准机制可能导致生成器通过忽略未来音乐来“hacking”。代理审计了 1024 causal codec、历史校准器、正式 6250 步 fixed/dynamic 训练结果，并运行了固定历史下的 Future 干预和完整短片补充对照。

## Task 1: 审核 causal-native / train-test-mismatch 路线

Outcome: partial

Preference signals:
- 用户要求从“第一性原理、成熟度和 novelty”重新判断旧 ES/GAN 是否适配新版 causalcodec，说明未来研究建议必须区分旧 codec 假设与当前 causal D+C 接口，不能直接迁移旧结论。
- 用户反复要求不要把局部收益包装成完整方法成功，并关注旋转、活跃度、D/C 分工和真实部署语义；类似任务应主动报告系统比较与单因素消融的边界。

Key steps:
- 审计 `EXP-20260921-fd-causal-native-trajectory-training`、1024 codec、generator、trajectory objective 和热盘结果。
- 确认新版 codec/generator 的 causal 历史接口：D/C 都读取完整 K64 历史；H4/C4、NFE10；codec 冻结；实际部署从歌曲起点自主生成。
- 发现 native base/CoF 活跃度显著改善，但生成旋转退化仍存在；真实 decoder 前缀下仍会出现异常，因此不能把问题全归因于长链 exposure bias。
- 结论保持谨慎：CoF/ES/GAN 机制上可迁移，但新版接口改变了旧 B71/物理闭环语义；必须用当前 codec、当前历史和当前解码路径重新证明。

Failures and how to do differently:
- 追加 CoF 是同目标低学习率续训，不是“无 CoF vs 有 CoF”消融；未来报告必须避免这种命名误导。
- 1024 codec 50k→100k 测试重建改善很小，不能仅凭训练 loss 继续扩长 codec；应优先分离 decoder 旋转退化、生成器目标和数据异常。
- 旧 codec 的 GAN/ES 配方不能直接当作公平基线；固定 codec、共同起点、相同自主 rollout、相同评分窗口和明确 proof role 是必要条件。

Reusable knowledge:
- 1024 causal codec 的关键接口：38D native、D512+C16、30Hz、一个 latent 对应两帧；decoder receptive field 约 62 tokens，generator 使用 K64 历史。
- 生成旋转异常与 6D 正交化退化相关；所有 >90° 生成突转都伴随至少一个 6D 基向量长度低于 0.2。严格 FP32、chunk/full decode、GPU graph 和真实 decoder cache 检查未发现转换或渲染 bug。
- 训练数据审计发现 G1/人体数据中确有跳变及部分跨 split 重复音频，但尚不能解释全部自由生成翻转。

References:
- `docs/research/CAUSAL_CODEC_COMMIT_TRAINING_MIGRATION_20260921.md`
- `docs/research/CAUSAL_CODEC_GENERATION_READINESS_20260921.md`
- `docs/experiments/EXP-20260921-fd-causal-native-trajectory-training.md`
- `docs/experiments/reviews/EXP-20260921-fd-causal-native-rotation-and-training-audit.md`
- `runs/causal_native_trajectory/cluster-readback-20260921/rotation-audit/`

## Task 2: 验证校准机制是否通过忽略 Future hacking

Outcome: partial

Preference signals:
- 用户明确担心“校准机制会不会 hacking 导致不用未来”，说明未来类似门控/校准实验必须同时做“输入敏感性”和“下游质量收益”两类验证，不能只看 reliability 非零。
- 用户希望区分“模型使用了未来”与“未来帮助了动作质量”；未来类似分析应保留这个两阶段结论，不把敏感性误报为有效性。

Key steps:
- 确认校准器在舞蹈训练前拟合并冻结，训练不能通过调低校准器权重逃避 Future；实际训练使用的 calibration artifact 与本地读回版本逐项匹配，权重最大差约 `3.3e-15`，官方测试标签未用于拟合。
- 在同一动态 6250 checkpoint、同一生成历史、decoder boundary、Past、Style 和随机数下，18 首歌共 54 个状态进行 Future-only 干预：
  - 重复原输入：逐值一致，0/54 状态变化。
  - 关闭未来：54/54 状态变化，平均下一段关节角差约 7.28°，44/54 状态离散 D 改变。
  - 替换为另一首歌未来：54/54 状态变化，约 7.80°，48/54 状态离散 D 改变。
  - 关闭过去音乐：约 8.76°，证明 Past 和 Future 都参与作用。
- 完成五种完整短片推理补充，每种 54 条：原 dynamic、关闭 Future、换错 Future、去历史反馈、Future 全信任。原 dynamic 音乐匹配 0.1088，关闭 Future 0.0991，换错 Future 0.1008；方向支持 Future 有用，但歌曲级统计不显著。
- 正式 fixed/dynamic 训练对照显示 dynamic 没有稳定优于 fixed：短片 MMR 0.1060 vs 0.1092，动态版 >90° 突转 2 vs 6，但配对检验未通过多重比较校正。
- 历史反馈对可靠度预测本身有强证据：排除训练集重复音频的 13 首诊断歌曲，预测误差下降约 27.8%，12/13 首改善；但这尚未转化为舞蹈质量收益。

Failures and how to do differently:
- 仅观察平均 Future attention/reliability 非零不足以排除 bypass；必须做 matched-state zero/swap intervention。
- 仅观察关闭 Future 后动作变化也不能证明 Future 使质量变好；必须继续做 matched full-rollout quality comparison，并把强干预的 OOD 限制写清楚。
- 不应把“可靠度估计更准”写成“舞蹈更好”；当前最强结论只到机制层，完整 downstream claim 仍未成立。

Reusable knowledge:
- 当前 Future 路径确实被生成器使用，不支持“完全忽略未来”的假设。
- 当前证据仍不能证明校准后的自纠正稳定改善动作；甚至去除历史反馈的补充推理中音乐匹配均值更高，不能据此认定反馈有害，但必须如实保留。
- 未来最关键的 proof role 是验证：正确未来相对无未来/错未来带来稳定动作收益；预测失准时，历史反馈相对当前信息基线减少损失。不要用最低 reliability 约束强迫模型使用 Future。
- 正式 6250 结果：fixed/dynamic 两组均完成；新训练组合相对旧方案关节急促变化约下降 11.6%，但该收益 fixed 也有，不能归因于动态自纠正。

References:
- `docs/experiments/reviews/EXP-20260922-fd-causal-music-self-calibration-results-20260923.md`
- `runs/causal_music_self_calibration/results-check-20260923/future-dependence.json`
- `runs/causal_music_self_calibration/results-check-20260923/future-only-rollout/`
- `runs/causal_music_self_calibration/results-check-20260923/feedback-window-analysis.json`
- `runs/causal_music_self_calibration/results-check-20260923/significance.json`
- Verification command: `.venv311/bin/python scripts/experiment_ledger.py lint` returned `0 error(s), 5 warning(s)`.

