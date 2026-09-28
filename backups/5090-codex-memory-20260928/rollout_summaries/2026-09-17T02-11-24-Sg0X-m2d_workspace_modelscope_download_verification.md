thread_id: 01a0ad22-0a18-73f0-a179-639d17ab826b
updated_at: 2026-09-17T13:33:48+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T10-11-24-01a0ad22-0a18-73f0-a179-639d17ab826b.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# Musics2Dance 本地工作区初始化、传输验证与私有数据落地

Rollout context: 用户要求在 `/home/wangyukun/ubt_isaac_sim_ws` 创建 `m2d-ws`，拉取私有 GitHub 仓库并配置本地/集群训练；随后要求评估外网下载速度、限制本地权限、统一训练显示名为 `m2d-train`，并下载/核验 ModelScope 训练产物。

## Task 1: 创建 m2d-ws 并拉取 Musics2Dance

Outcome: partial

Preference signals:
- 用户要求“这个m2d的权限只能给我自己开”以及训练/上传集群时显示为“m2d-train” -> 后续应默认收紧工作区权限，并统一可控制的作业、容器和进程命名；本轮未完成训练启动配置及命名验证。
- 用户关心上百 GB 产物的传输效率 -> 类似任务应先做小规模速度实测，再决定浅克隆、断点续传或近端中转，不应直接走完整 Git 历史和 LFS。

Key steps:
- 找到私有仓库 `lbtwyk/Musics2Dance`，默认分支 `prior-dev`。
- 初次 SSH clone 因 GitHub host key verification 失败，改用 `gh auth setup-git` 后的 HTTPS 拉取。
- 完整历史/LFS 拉取约 207 MiB Git pack，速度约 0.2–1.8 MiB/s，平均约 0.58 MiB/s；香港外网线路明显不适合大规模传输。
- 重新使用 `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --single-branch --branch prior-dev ...`，最终得到干净的 `prior-dev` checkout，commit `24f4f75`；跳过约 8 GB LFS 模型下载。
- 对 `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws` 执行 ACL 清理和 `chmod -R go-rwx`，验证为仅 owner 可访问：`user::rwx`, `group::---`, `other::---`。
- 读取 `AGENTS.md`、`README.md`、`docs/NEW_SERVER_SETUP.md` 等，确认仓库要求 Python 3.11、本地 `.venv311`、Slurm 上进行正式 GPU 工作、实验合同/ledger 优先；本机为 RTX 5090，磁盘空间曾低至约 93 GB，后续约 203 GB。

Failures and how to do differently:
- 不要在香港线路上直接完整 clone + LFS；优先浅克隆并 `GIT_LFS_SKIP_SMUDGE=1`，只按需 `git lfs pull --include=...`。
- 初次拉取期间并发 git clone/switch 产生 `.git/index.lock` 和未完成状态；后续应先确认没有残留 git/git-lfs 进程，再执行切换或清理。
- 本轮没有完成用户要求的本机/集群训练入口，也没有验证 `m2d-train` 在 `nvidia-smi` 中的实际显示；不能把“代码已拉取”描述为“训练已配置”。

Reusable knowledge:
- 仓库 checkout 路径：`/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`。
- Git remote 使用 HTTPS：`https://github.com/lbtwyk/Musics2Dance.git`；GitHub 账户已通过 `gh` 登录。
- 仓库 GitHub API 显示约 497,317 KiB；`prior-dev` 树约 263 MB tracked blobs，多个 `.pt`/缓存文件由 Git LFS 管理。
- 远端分支存在 `prior-dev`、`main` 及多个 migration/codex 分支；默认 HEAD 为 `prior-dev`。
- 正式训练应根据具体实验 spec 和 ledger，不应从 README 片段自行重建命令；Isambard/Slurm 与本机 RTX 5090 是不同运行路径。

References:
- `gh search repos music2dance --owner lbtwyk` 找到 `lbtwyk/Musics2Dance`。
- `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --single-branch --branch prior-dev https://github.com/lbtwyk/Musics2Dance.git Musics2Dance`
- `git lfs ls-files --size` 显示约 8 GB LFS 对象；未自动下载。
- ACL 验证：`getfacl -p /home/wangyukun/ubt_isaac_sim_ws/m2d-ws` -> owner rwx，group/other 无权限。

## Task 2: 下载并核验 ModelScope 主线与复现数据

Outcome: success

Key steps:
- 主线数据下载到 `modelscope/mainline/`，约 20 GB；35 个非空文件全部存在且大小正确。
- 复现数据下载到 `modelscope/repro/`；首次下载结束后发现 2 个 404 缺失文件，随后通过 ModelScope API 清单确认它们仍存在并单独补下。
- 清单发生变化，又发现 512 个新增缺失文件；重新下载完整 snapshot 后最终远端清单为 5725 个 blob。
- 对复现库 5725 个文件逐个核验：`missing=0`, `size_bad=0`, `hashed=5725`, `hash_bad=0`。
- 三个训练输入压缩包通过 `zstd -t` 完整性检查：`data-finedance.tar.zst`、`data-finedance_g1_yaw_anchor_abs_6d_rvqvae_dataset_backups.tar.zst`、`data-finedance_g1_fkbeats.tar.zst`。
- 下载进程已结束，无 `.incomplete` 文件；磁盘剩余约 203 GB。
- 复现库 README 仍声明“Upload is incomplete”，因此只能确认本机与当前 ModelScope 源端一致，不能宣称源端计划中的所有产物或完整训练链路已经发布/就绪。

Failures and how to do differently:
- 不要把下载进度 100% 当作数据完整性；ModelScope 下载结束时仍可能有 404/失败文件。
- 源端清单可能在下载期间新增文件；完成后必须重新拉取远端清单并做逐文件 size + SHA256 校验。
- `modelscope download` 对单文件重试有效；清单较大时用 `HubApi.get_dataset_files(... page_size=1000)` 分页核对。

Reusable knowledge:
- ModelScope repro repo：`lbtwyk/musics2dance-foredance-repro`，revision `master`。
- ModelScope mainline repo：`lbtwyk/musics2dance-foredance-mainline`，revision `master`。
- Repro 最终状态：5725 blobs，全部存在、大小匹配、SHA256 全部匹配。
- Mainline `transport-manifest.json` 声明 27 个文件、19,554,072,322 bytes；实际 35 个非空文件全部存在且大小匹配；`inference_verified=false` 仍成立。
- 本机 ModelScope 路径由 workspace `AGENTS.md` 约定为 `modelscope/repro/` 和 `modelscope/mainline/`；这些是私有数据，不得公开或暴露令牌。

References:
- `modelscope/repro/README.md`：明确写有“Upload is incomplete until a verified completion manifest is published here.”
- 最终校验输出：`blobs 5725 missing 0 size_bad 0 hashed 5725 hash_bad 0`。
- 主线校验输出：`entries 54 files 35 missing [] wrong []`。
- 完整性命令：`zstd -t .../data-finedance.tar.zst .../data-finedance_g1_yaw_anchor_abs_6d_rvqvae_dataset_backups.tar.zst .../data-finedance_g1_fkbeats.tar.zst`。

## Task 3: 记忆备份导入

Outcome: success

Key steps:
- 从私人 HF bucket `hf://buckets/wyksdsg/musics2dance-server-private/20260908/agents/agent-context-private.tar.gz` 恢复 64 个历史记忆文件到 `/home/wangyukun/.codex/memory-imports/isambard-20260908/`，未覆盖现有本机记忆。
- 将适用于当前 M2D 的边界和历史结论写入 `/home/wangyukun/.codex/memories/extensions/ad_hoc/notes/20260917T100047Z-import-isambard-m2d-memory.md`。
- 旧服务器路径和状态被明确标记为历史参考，要求重新检查当前 checkout、ledger、合同和 live artifacts。

Preference signals:
- 用户纠正“不是，我的意思是拉下来更新本地记忆” -> 用户希望从指定私有备份导入本地，不要反向上传；今后涉及备份同步必须先确认方向。

References:
- 本地导入目录：`/home/wangyukun/.codex/memory-imports/isambard-20260908/`。
- 导入摘要文件：`/home/wangyukun/.codex/memories/extensions/ad_hoc/notes/20260917T100047Z-import-isambard-m2d-memory.md`。
