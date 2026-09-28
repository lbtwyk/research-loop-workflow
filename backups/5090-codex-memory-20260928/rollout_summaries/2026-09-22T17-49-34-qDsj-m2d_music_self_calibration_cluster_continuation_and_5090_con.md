thread_id: 01a0ca3c-c380-7931-86b6-f71d26400857
updated_at: 2026-09-23T14:20:19+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T01-49-34-01a0ca3c-c380-7931-86b6-f71d26400857.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# 集群三卡音乐自校准续训与5090控制实验迁移

Rollout context: 在 `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance` 中核对最新三卡音乐自校准实验、加速评测，并将5090上的三组 Future controls 迁移到集群单张80GB卡并行运行。

## Task 1: 核对集群最新三卡训练与续训

Outcome: success

Preference signals:
- 用户明确说“就是最新的三卡实验”并要求“让集群的下个训练赶快跑上” -> 应优先处理最新已批准路线，不自行替换成建议中的其他消融。
- 用户要求保留正在运行任务并推进下一轮；后续确认“还有在5090上跑的，我要在集群上续跑，单卡跑三个” -> 迁移时必须保留已验证进度、预算和随机状态，不重置或缩减实验。

Key steps:
- 通过热盘读回确认三卡固定/动态音乐自校准仍在推进；早期读数为 fixed 718/6250、dynamic 698/6250，H100利用率约95%–98%。
- 已准备并交付12500步续训脚本；后来热盘读回确认 fixed/dynamic 均已启动并达到6358步以上。
- 5090和中转机没有kubectl/集群配置，因此本机无法直接提交或确认Job。

Reusable knowledge:
- 集群与本机必须区分：热盘上传/readback不等于Job提交；只有Pod、Job状态和训练日志才能证明运行。
- 12500续训必须从各自6250最终checkpoint恢复，保留optimizer、RNG和source order；原6250评测不能冒充12500评测。

References:
- Experiment: `EXP-20260922-fd-causal-music-self-calibration`
- Hot paths: `/hot/upload/EXP-20260922-fd-causal-music-self-calibration/training-12500/fixed/status.json`, `.../dynamic/status.json`
- Local status artifact: `runs/causal_music_self_calibration/migrate-1h-20260923/extension-live.json`

## Task 2: 加速6250阶段评测视频

Outcome: success

Key steps:
- 发现集群渲染使用软件OSMesa，导致H卡空闲而视频渲染耗时数小时；5090硬件EGL渲染显著更快。
- 对已生成动作和cases进行只读迁移，不重新生成动作；GPU backend验证为 `NVIDIA GeForce RTX 5090/PCIe/SSE2`。
- 四个剩余120秒、五画面对比视频在5090完成并上传/readback验证；总加速渲染约620.61秒，完整H264/AAC逐帧解码检查通过。
- 评分先于视频发布的改动及缓存已完成视频复用逻辑，并通过测试；但科学接受仍未自动宣称。

Failures and how to do differently:
- 初始本机EGL探测误用软件渲染，且测试 framebuffer 默认宽度不足；设置模型 `offwidth/offheight` 并显式验证 renderer 后才确认硬件路径。
- 不应让集群训练卡等待视频渲染；动作生成、评分、渲染和科学接受应分离。

References:
- `runs/causal_music_self_calibration/render-acceleration/hardware-manifest.json`
- `runs/causal_music_self_calibration/render-acceleration/accelerated-manifest.json`
- `runs/causal_music_self_calibration/render-acceleration/START_12500_NOW.txt`
- 5090 renderer probe: software 60帧约9.69s；RTX5090约0.042s（仅栅格绘制基准）。

## Task 3: 将5090三组Future controls迁移到集群单卡并行

Outcome: partial

Preference signals:
- 用户要求“单卡跑三个” -> 三组必须在同一张足够显存的H卡上并行，不能改成三张卡或只跑其中两组。
- 用户要求“续跑” -> 迁移必须从精确checkpoint恢复，而非从头训练。

Key steps:
- 三组定义：`film_dynamic`、`ca_mean_history`、`film_ca_dynamic`，每组6250更新、seed1234、48 source groups、physical microbatch16。
- 停止5090前保存并验证了：FiLM checkpoint update1563；CA/history checkpoint update1450；第三组从共同parent起点update0。
- 5090最后观测分别约1567和1489，因此集群会重算最后4/39步；这不是额外预算。
- 上传并readback验证约8.31GB checkpoint/calibration资产；本地严格resume检查通过，12项Future-control测试通过。
- 创建并交付单卡Job入口 `APPLY_1H_THREE_CONTROLS.txt`，资源为1 GPU、16 CPU、128GiB，使用MPS在一张至少70GiB H100/H200/H800上并行三组；禁止hostname限制和suspend。

Failure / remaining blocker:
- 交付和本地验证均成功，但截至rollout结束没有集群Job提交证据；必须在集群终端执行脚本后再检查Pod、GPU利用率、三组status和resume进度。
- 迁移后的三路实际显存、并行吞吐和是否能在目标卡稳定运行仍未验证，不能仅凭5090峰值宣称成功。

References:
- `runs/causal_music_self_calibration/migrate-1h-20260923/APPLY_1H_THREE_CONTROLS.txt`
- `runs/causal_music_self_calibration/migrate-1h-20260923/migration-ready.json`
- `runs/causal_music_self_calibration/migrate-1h-20260923/resume-verification.json`
- `runs/causal_music_self_calibration/migrate-1h-20260923/code-delivery.json`
- Job name: `m2d-future-controls-1h`
- Required next check: `kubectl get pods -n ogi-llm -l job-name=m2d-future-controls-1h -o wide` and read hot logs/statuses.

