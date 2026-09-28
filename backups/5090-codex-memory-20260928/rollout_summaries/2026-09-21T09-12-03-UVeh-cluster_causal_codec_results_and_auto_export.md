thread_id: 01a0c33c-96ce-7991-92b2-b516ea344a29
updated_at: 2026-09-24T06:27:11+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T17-12-03-01a0c33c-96ce-7991-92b2-b516ea344a29.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# 集群 causal codec 结果已验证支持本地主要判断，并接入后续自动导出

Rollout context: 在 `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance` 核对 EXP-20260918-fd-causal-codec-capacity 的集群正式训练结果与本地 RTX5090 单 seed 结果。最初热存储训练目录返回 550 权限错误；用户随后在 KubeSphere 执行导出脚本，代理下载并重新聚合结果。

## Task 1: 读取并比较集群正式 causal codec 结果

Outcome: success

Preference signals:
- 用户要求“以后要自动导出成果到5090可以读取下载的地方，这样你可以直接读或者下载” -> 后续集群训练应默认在结束时把指标、配置、日志导出到 5090 可读取的热存储路径，避免再次要求用户手动进入集群导出。
- 用户关心集群正式训练是否支持本地判断 -> 比较时必须区分本地单 seed、集群三 seed、1024 扩展和旧主线，不能混合配置或扩大结论。

Key steps:
- 确认正式矩阵为 4 配置 × 3 seeds × 100k steps，batch 64、workers 2、183 train / 18 test tracks。
- 用户导出 `cluster-results-20260921.tar.gz` 后，下载 102 个记录文件并解压。
- 独立验证 12 组 completion/evaluation/config；每组 18 条测试曲目、共 51534 frames，重新聚合误差最大仅 `1.46e-11`。
- 集群均值 native MSE：compact256 `0.057629`、multirate256 `0.053709`、multirate512 `0.065307`、multirate512_balanced `0.048242`。

Reusable knowledge:
- 三个 seed 的排序完全支持本地主要判断：balanced512 < multirate256 < compact256 < full512。
- balanced512 相比普通 multirate512 的 native MSE 平均改善 26.13%，joint MAE 改善 12.42%；普通 512 相比 multirate256 的 native MSE 变差 21.59%。
- 集群结果支持“减轻 auxiliary 约束有效、单纯加宽无益”的 reconstruction 结论；不支持物理表现全面改善，因为 foot-skate 方向与本地结果不同且接触指标稀疏。
- 该集群矩阵不包含后来 1024 宽度实验，也没有生成质量或物理执行证据；不能把结论扩展到这些方面。与旧主线的比较约为 balanced MSE 5.92×、joint error 2.38×，但训练/帧截取不完全匹配，只能作参考。

Failures and how to do differently:
- 直接从 FTP 读取 `training/` 和 `supervised-loss/training/` 时遇到 `550 Permission denied`，且无法读取最终指标；不能据此判断训练失败。以后训练流程应自动导出可读记录。
- 当前旧任务未接入自动导出；新 exporter 只会在新代码包部署后生效，强制杀进程或节点掉线时无法执行退出钩子。

References:
- Experiment: `EXP-20260918-fd-causal-codec-capacity`
- Verified report: `docs/experiments/reviews/EXP-20260918-fd-causal-codec-capacity-cluster-results-20260921.md`
- Raw readback: `runs/causal_codec_capacity/cluster-readback-20260921/`
- Verification: `runs/causal_codec_capacity/cluster-readback-20260921/verify_comparison.py`, `verified-comparison.json`
- Exporter: `scripts/export_m2d_results.py`
- Exporter test passed: `tests/test_m2d_result_export.py` (`Ran 1 test ... OK`)

## Task 2: 接入后续集群结果自动导出

Outcome: success

Key steps:
- 新增 `scripts/export_m2d_results.py`，在集群入口正常结束或 Python 异常退出时生成 `results-records.tar.gz` 与 `download-manifest.json`。
- 接入 `run_token_causal_codec_cluster.py`、`run_token_causal_variants_cluster.py`、`run_g1_causal_native_cluster.py`、`run_g1_commit_cluster.py`。
- 指标、配置、日志进入记录包；模型和视频保留原位置并开放读取；runtime、原始数据和代码不纳入记录包。
- 更新 `docs/M2D_HOT_STORAGE.md` 与 `AGENTS.md`，并更新实验最新 artifact。
