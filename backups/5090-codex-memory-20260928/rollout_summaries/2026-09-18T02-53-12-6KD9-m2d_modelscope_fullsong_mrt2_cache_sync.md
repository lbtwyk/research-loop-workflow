thread_id: 01a0b26e-aa7e-7512-9bdc-a5d06f11a5e3
updated_at: 2026-09-18T08:57:37+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T10-53-12-01a0b26e-aa7e-7512-9bdc-a5d06f11a5e3.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# ModelScope 全曲 MRT2 缓存已补齐并验证可用于生成器预检

Rollout context: 在 `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws` 中，用户要求在其上传 ModelScope 产物的同时拉取缺失缓存，并确认 COF/token-causal codec 后续训练是否可开始。

## Task 1: ModelScope 缓存同步与生成器训练准备

Outcome: success

Preference signals:
- 用户要求“在那边上传的同时同时拉下来”，且希望长传输后台持续进行 -> 类似任务应并行监控远端清单、只下载新增/缺失文件，不重复传输已验证的大文件。
- 用户强调训练准备必须基于证据，不能把上传进度、文件存在或短流程误报为正式训练就绪 -> 汇报时要明确区分资产已下载、缓存可读、本地预检通过、正式训练未启动和科学结果未接受。
- 用户偏好直接、简洁的中文进度汇报 -> 状态应包含当前阶段、已完成数量、阻塞项和下一步，而不是泛泛描述“仍在运行”。

Key steps:
- 先读取引用任务，确认正式 codec 流程已在本地通过短流程，但生成器训练此前缺少全曲 MRT2 条件缓存。
- 刷新 ModelScope 远端清单：上传过程中 dataset 条目从 5725 个正文件增至 6024 个条目、model 从 35 增至 54 个条目，但新增项最初只是目录项；后续确认两个已知仓库本地均无实际缺口。
- 用户提供全曲缓存仓库 `lbtwyk/musics2dance-fd-mrt2-fullsong-private` 后，下载 8 个压缩卷；全部通过声明大小检查和 `zstd -t`，并提取 1619 个文件。
- 编写/修复 `scripts/build_token_causal_fullsong_music_cache.py`：合并 legacy MRT2 cache、已有 prefix cache，并只对缺失 cutoff 用严格因果 MRT2 runtime 重算；对音频短于动作的 5 条轨迹按 `min(raw_motion_length, floor(audio_frames*30/sample_rate)+15)` 截断，保留 15 帧未来窗口，不补零、不伪造预测。
- 三路并行 worker 完成 201 条轨迹：183 train、18 test；生成顶层 manifest 并做 digest、数组、cutoff、音频边界和 `FutureMusicStore` 实际读取校验。
- 修正 `train_g1_token_causal_generator.py` 的覆盖检查，使其依据缓存 manifest 声明的 paired motion length，而不是盲目使用原始动作长度，避免 041/043/059 等音频尾部不足条目被误报为缺缓存。
- 使用正式 seed-1234 codec checkpoint 做全 201 条轨迹、4 步 CUDA generator preflight；0/2 workers 均读取 16 个真实样本，loss 有限，断点恢复参数误差为 0。

Reusable knowledge:
- 当前完整缓存路径：`modelscope/repro/foredance-mainline-20260912/generator/condition_caches/token_causal_fullsong/`。
- 最终覆盖：train `95,411` 个非零 cutoff，test `6,399` 个非零 cutoff；顶层 manifest 含 201 条轨迹，大小约 5.63 GB。
- provenance：93,874 行来自 legacy cache，3,015 行来自 prefix cache，4,921 行由本地 MRT2 严格因果重算。
- 顶层 manifest SHA256：`9afc8c13f1483df1fa8e5eacd100042a697e927075d511e2d0c77fe49277a769`。
- 生成器预检通过不等于正式训练或质量接受；本 rollout 没有启动正式 generator training，也没有科学结果接受。
- 两个已知 ModelScope 仓库的 transport 完整性不能证明生成器可训练；此前它们只有约 3% 的 prefix coverage。应先做 cutoff coverage 和训练入口实际读取验证。
- ModelScope 下载/上传监控适合使用分页 `HubApi.get_dataset_files(..., page_size=1000)`、按本地大小比较缺口，并对大文件保留断点；不要依赖进度百分比或目录项数量。

Failures and how to do differently:
- 初始判断认为全曲 cache 不在已知仓库中；用户补充私有 full-song 仓库后才获得完整来源。未来应在判定“需要本地重算”前，主动询问/检索其他私有仓库或服务器。
- 首版 cache builder 对动作长度和音频长度不一致的轨迹会触发 EOF；通过 paired-length 规则修复，未来生成音频条件缓存必须先检查音频可覆盖帧数。
- 曾从错误的工作目录调用 `.venv311/bin/python`，导致找不到环境；正确环境是 `Musics2Dance/.venv311`。
- `pytest` 不在 repo 环境中，不能据此宣称单元测试通过；本次采用实际 cache verify、FutureMusicStore readback、generator preflight 和 `py_compile` 验证。

References:
- Cache manifest: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/modelscope/repro/foredance-mainline-20260912/generator/condition_caches/token_causal_fullsong/manifest.json`
- Generator preflight: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/runs/token_causal_dc/full-cache-preflight-20260918/generator/preflight.json`
- Verify log: `modelscope/logs/token-causal-fullsong-verify-20260918.log`
- Full-cache build logs: `modelscope/logs/token-causal-fullsong-worker3b-{0,1,2}-20260918.log`
- Builder: `Musics2Dance/scripts/build_token_causal_fullsong_music_cache.py`
- Generator entrypoint: `Musics2Dance/train_g1_token_causal_generator.py`
- Exact preflight result: `generator_train_resume`, `passed: true`, `resume_max_parameter_error: 0.0`.
