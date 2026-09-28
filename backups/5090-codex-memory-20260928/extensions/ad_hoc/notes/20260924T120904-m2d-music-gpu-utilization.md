# M2D music preparation priority

User explicitly said on 2026-09-24: "记住音乐处理速度要拉满速度，利用好h卡". For M2D music preprocessing, prioritize measured throughput and H-card utilization, including concurrent independent music tasks within each GPU when resources permit, and reuse loaded models and shared music caches. This preference applies to preparation as well as training. The current C64 FD/OD experiment allows at most three H cards; future GPU limits must follow the then-current user authorization.
