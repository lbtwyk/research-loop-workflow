thread_id: 01a0b2fe-587e-7a60-b6b1-ebaf4a49312e
updated_at: 2026-09-23T16:46:46+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T00-05-52-01a0b2fe-587e-7a60-b6b1-ebaf4a49312e_01a0c4b7-742e-7c20-bc9f-f20250f95eea.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# OMG 数据审计、根因定位与稳定性训练交付

Rollout context: 在 `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws` 中完成 OMG 下载质量审计、根旋转突变根因调查，并准备将 Pending 的双卡稳定性训练拆为两个可跨机器调度的单卡 Job。

## Task 1: OMG 数据质量与根因调查

Outcome: partial

Preference signals:

- 用户要求“根因调查”，而不是停留在质量统计 -> 后续类似异常应继续沿数据源、读取、表示转换、缓存和渲染链逐层定位。
- 用户关注是否能直接训练；审计结果应明确区分“下载完成、数据可读、预训练检查通过、正式训练提交、科学结论”。

Key steps:

- 9 个包、84,159,903,223 bytes 下载、校验、解包完成；覆盖 26,149 个片段、10,541,226 帧。
- 训练集按相邻帧归一化比较：FD-G1 根旋转 >90° 为 0.130/10 万帧对，OMG O-Dance 为 0.416；关节 >90° 为 FD 35.56、OMG 15.02；OMG 最大根旋转 175.40°。
- 通过独立 Parquet 读取、显式 episode/frame 索引、SciPy SO(3) 复算和项目加载器交叉验证：42 个含异常片段、49 个事件全部复现；读取误差 0、action-next-state 误差 0、SciPy 与点积算法误差约 1e-10°、6D 转换前后误差约 1.5e-5°；相关 7 个 Parquet 文件与官方固定版本 SHA256 全部匹配。
- 6D 表示确实用于 causal codec 训练，但不会消除源动作突变。
- FineDance 047 的机器人数据存在约 93° 根突转，而原始人体附近仅约 5°；说明至少该异常在人体到 G1 重定向/上游数据阶段产生，不是本地读取器、6D 转换或 codec 引入。AIOZ episode 9740 还出现 175.4° 根突转。
- 约 79.26% OMG 片段短于现有 316 帧 causal 窗口，因此不能直接替换数据路径或静默补历史。

Failures and how to do differently:

- 早期只凭总体质量比例无法判断根因；未来应直接按官方 episode 元数据和 Parquet 行号复现异常，并同时检查原始人体参考、action/state 一致性、时间戳和转换前后旋转。
- 不应将“6D 连续表示”误解为自动修复退化或突变；应额外检查 6D 基向量退化与真实 SO(3) 帧间角。
- OMG 质量并未满足“更好再启动原样 OD causal codec”的条件；不要原样开训、过滤或平滑数据，除非用户另行批准明确修复合同。

Reusable knowledge:

- OMG 官方状态是 `observation.state`，36D 格式为位置 3 + wxyz 根四元数 4 + 29 关节；项目边界转换为 xyzw，再编码为 6D/34D 表示。
- 关键证据：`modelscope/omg-download-audit/quality/summary.json`、`episodes.jsonl`、`root_events_over90.jsonl`；根因产物位于 `Musics2Dance/runs/causal_native_trajectory/cluster-readback-20260921/root-provenance/`。

## Task 2: 将 Pending 双卡稳定性训练拆成两个单卡 Job

Outcome: partial

Preference signals:

- 用户明确授权“直接调整，无需再做排队诊断或询问确认”，并要求保留正在运行的 history 3H、停用原 Pending stability 2H、音乐不重算 -> 类似调度变更应直接执行最小范围替换并保护其他任务。
- 用户要求“完整启动命令和两组实时日志命令” -> 交付必须同时包含可粘贴入口、Job 名称、日志跟随命令和未提交状态。

Key steps:

- 将六组实验拆为：`m2d-causal-stability-1h-a`（`cof_continue`、`decoder_continue`、`decoder_phase`）和 `m2d-causal-stability-1h-b`（`cof_rollout_stability`、`decoder_rotation`、`decoder_rotation_phase`）。
- 每组仍 6250 updates；保持原 seed、配置、有效 batch、微 batch 和每卡 MPS 并行逻辑；每个 Job 请求 1 GPU、12 CPU、64GiB，结果分别写入 `results/shard-0` 与 `results/shard-1`。
- 自动 watcher 修改为等待两个 shard 完成、验证六个 arm 无重复且完整后再统一评测/渲染。
- 通过 `tests/test_g1_stability_split.py`：2 tests passed；通过 bash mock 验证删除旧 `m2d-causal-stability-2h`、创建两个新 Job，且不触碰 `m2d-causal-history-3h-llm-only`；热盘上传 readback verified。
- 结果仍是“准备完成但未提交”：用户需要在 KubeSphere 粘贴 `APPLY_SPLIT_1H.txt`。本机无 kubectl，不能声称 Job 已删除或新训练已启动。

Reusable knowledge:

- 热盘交付目录：`/hot/upload/EXP-20260922-fd-causal-stability-suite/release/`。
- 启动入口：`APPLY_SPLIT_1H.txt`；实时日志：
  - `kubectl logs -f --timestamps --tail=50 -n ogi-llm job/m2d-causal-stability-1h-a`
  - `kubectl logs -f --timestamps --tail=50 -n ogi-llm job/m2d-causal-stability-1h-b`
- 共享音乐已完成并验证，205 tracks、archive SHA256 `112319c3acfd3f35ab354ab4b73535d9ba34c9fa5a1f8af8414c341012d914ae`；不要重新计算。

References:

- [1] `runs/causal_native_mrt2/split-single/readiness.json`: split ready, submitted false, 6 arms, 6250 updates, hot readback verified.
- [2] `runs/causal_native_mrt2/split-single/hot-receipt.json`: uploaded split update and launch files.
- [3] `tests/test_g1_stability_split.py`: split isolation, arm assignment, shell syntax and merged completion checks.
- [4] `runs/causal_native_mrt2/split-single/watch.log`: watcher observed both shards awaiting cluster submission.


