thread_id: 01a0de93-7687-7e72-a4e6-d038bcdecc27
updated_at: 2026-09-27T15:39:19+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-36-41-01a0de93-7687-7e72-a4e6-d038bcdecc27.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# 标准化 G1 模型对比视频宫格流程已实现并接入交付收尾

Rollout context: 用户要求查看近期 5090 M2D 训练对话，建立最多九宫格、每格标注模型方法与模块、每首歌/Beat It/切歌各一条 60 秒有声对比视频，并统一视频目录与默认渲染流程。

## Task 1: 建立统一 60 秒模型宫格与目录

Outcome: success

Preference signals:

- 用户要求“最多比如9个视频”“每个视频都要清晰的标注模型用到的方法和模块”以及“视频目录也要整理好标准化” -> 后续视频交付默认应使用最多九格、可读的方法/模块标签和统一 catalog，而不是只输出散落 MP4。
- 用户要求“作为所有模型训练完后的视频渲染默认流程” -> 训练/评测完成后应自动进入标准视频、宫格、目录和音画核验阶段；缺少模型源视频时保持未完成，不用旧模型替代。

Key steps:

- 检查近期 5090 线程及仓库规范，确认已有标准 35/70 视频套件、Beat It、连续切歌和 `g1_video_catalog.py`。
- 新增 `scripts/build_g1_standard_grid.py`，支持 1–9 个画面、固定歌曲起点/音频/种子/帧数，生成 60 秒 30fps 宫格，写入模型方法和模块标签，并调用完整音视频解码验证。
- 扩展 `scripts/g1_video_catalog.py` 的 5–9 画面位置定义。
- 将宫格自动接入 `run_g1_rf_cof_standard_suite.py`、`run_g1_rf_rollout_local.py` 和 `deliver_g1_granularity_standard.py`；更新 `AGENTS.md` 与 `docs/research/modules/G1_STANDARD_60S_VIDEO_GRID.md`。
- OD 交付配置增加专属标签、FD 基线标签和独立标题；运行中的 OD 标准交付仍继续，另启动 `m2d-od-chunk-grid60` 等待源视频完成后补生成宫格。

Reusable knowledge:

- 标准宫格固定 21 条：15 首 60 秒测试歌、021/127 两首训练展示歌、Beat It 前 60 秒、3 条连续切歌；每条 1800 帧、30fps、歌曲零点起始（Beat It 从既有 120 秒素材截取）。
- `g1_video_catalog.py` 只接受带成功音画解码 receipt 的 MP4，并生成 `public/videos/`、`public/index.html`、`CATALOG.md`、`catalog.csv`、`catalog.json`；工作素材和 `silent.mp4` 不进入正式目录。
- 标准源视频必须先完成并验证歌曲、起点、种子、帧数、连续状态和音频；宫格最多九格，缺源时不能用旧模型视频冒充。

Failures and how to do differently:

- 首次运行宫格脚本被间接导入 `scipy/librosa` 拖慢/中断；随后用 `.venv311` 正确运行并成功完成。未来应优先使用仓库 `.venv311` 和项目内 `_ffmpeg_exe()`。
- 配置扩展后曾出现 `build_g1_standard_grid.py` 缩进错误，已修正并通过 `py_compile`、`bash -n`、JSON 校验和 `git diff --check`。
- 系统无 `ffprobe` 命令；项目验证应使用 `validate_video`/imageio-ffmpeg，而不是假设系统 ffprobe 存在。

References:

- 新入口：`Musics2Dance/scripts/build_g1_standard_grid.py`
- 规范：`Musics2Dance/docs/research/modules/G1_STANDARD_60S_VIDEO_GRID.md`
- 默认要求：`Musics2Dance/AGENTS.md` 中“standard 60-second comparison grid”段落
- 验证命令：`.venv311/bin/python -m py_compile scripts/build_g1_standard_grid.py scripts/run_g1_rf_cof_standard_suite.py scripts/run_g1_rf_rollout_local.py scripts/deliver_g1_granularity_standard.py scripts/finalize_g1_music_self_calibration_12500.py`

## Task 2: 为已完成模型生成并核验标准宫格

Outcome: success

Reusable knowledge:

- 已完成模型组 `runs/latent_chunk_history_20260926/standard-delivery/grid60/` 生成 21 条正式视频，`manifest.json` 和 `public/catalog.json` 均为 `status=complete, count=21`。
- 21 条视频均有预览图、1800 帧且 verification passed；宫格画面数量为 6 或 7，均在九格上限内。
- 组级完成记录：`runs/latent_chunk_history_20260926/standard-delivery/completion.json` 包含 `grid60_videos: 21` 和 public 目录。

References:

- 成品目录：`runs/latent_chunk_history_20260926/standard-delivery/grid60/public/`
- 目录文件：`public/index.html`、`public/CATALOG.md`、`public/catalog.csv`、`public/catalog.json`
- 代表视频：`public/videos/long_012_60s.mp4` 及对应 `.jpg`

## Task 3: OD 完整数据模型宫格交付

Outcome: partial

Failures and how to do differently:

- OD 五组训练仍在进行，已有 175 条标准视频交付守护流程，但本 rollout 结束时 `runs/od_chunk_transfer_20260927/standard-delivery/completion.json` 和 `grid60/manifest.json` 尚不存在；不能声称 OD 宫格完成。
- OD 宫格守护脚本已修正为不再使用 `--skip-grid`，但必须等待 OD 基线和各候选模型各自的标准源视频完成后再运行。

References:

- OD 监控脚本：`runs/od_chunk_transfer_20260927/watch-standard.sh`
- OD 宫格等待脚本：`runs/od_chunk_transfer_20260927/watch-grid60.sh`
- OD 配置：`configs/experiments/20260927-od-chunk-delivery.json`
- 预定 OD 目录：`runs/od_chunk_transfer_20260927/standard-delivery/grid60/`
- 当前仍运行的 tmux 会话：`m2d-od-chunk-standard`、`m2d-od-chunk-grid60`
