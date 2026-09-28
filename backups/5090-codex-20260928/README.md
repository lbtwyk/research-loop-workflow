# Complete 5090 Codex conversations, 2026-09-28

This is an ordinary compressed, unencrypted backup of the complete raw JSONL files for all 97 Codex conversations started from 2026-09-15 through 2026-09-28. It includes tool calls, tool outputs, reasoning records, and embedded non-text content. The archive contains `MANIFEST.json` with SHA-256 checksums for every source file. It is public because this repository is public.

Download all `*.part-*` files and both checksum files. On Mac, run:

```bash
shasum -a 256 -c SHA256SUMS
cat codex-5090-20260928-full-conversations.tar.zst.part-* > codex-5090-20260928-full-conversations.tar.zst
shasum -a 256 -c ARCHIVE_SHA256
zstd -t codex-5090-20260928-full-conversations.tar.zst
mkdir restored
zstd -dc codex-5090-20260928-full-conversations.tar.zst | tar -C restored -xf -
```
