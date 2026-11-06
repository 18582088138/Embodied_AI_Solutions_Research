# 公共资料工具

Python 3.10+，仅依赖标准库。新增调研先读仓库 `.agents/skills/embodied-ai-platform-research/SKILL.md` 与 `CONTRIBUTING.md`。

- `download_materials.py`：唯一项目资料下载入口，按 URL 去重，保存原件、依赖、哈希和失败记录。
- `check_report.py`：逐篇报告结构、引用/图源、字节哈希、HTML 文本与历史基线检查。
- `archive_paths.py`：JSON 路径存为仓库根相对路径，加载时基于本工具位置解析，支持 clone 到新目录。
- `organize_repository.py --build-indexes`：重建根/类别/分项 README 和当前索引，检查报告链接。仅一次性旧资料导入使用 `--normalize`；它会记录迁移前哈希并改变 authored links，不编辑原始响应或依赖。
- `verify_repository.py`：离线核查已成功归档正文、原始响应和依赖的 SHA256；保留失败候选。
- `prepare_git_sources.py`：生成来源目录与机器清单，将报告引用图表复制到 assets/figures，原件链接转为来源清单链接。
- `test_*.py`：本地 HTTP fixture、去重和路径可移植测试。

```text
python toolkit/download_materials.py --project 01_Compute_Chips/<目标分项> --manifest <清单.json> --dimension 01_Hardware_Platform
python toolkit/check_report.py --project 01_Compute_Chips/<目标分项> --report 01_Hardware_Platform.md --baseline <本章基线.json>
python toolkit/organize_repository.py --build-indexes
python toolkit/verify_repository.py
python -m unittest discover -s toolkit -p "test_*.py"
```

02 与 08 专题联合归档分别使用 `--collection 02_software_depth`、`--collection 08_core`。同一 collection 的最终清单需覆盖全部专题实际引用来源。重用已归档材料不默认 refresh；项目只允许运行一个下载进程。

原平台专用清单已整理到各分项 `research_state/manifests/`；历史生成/审查脚本在各分项 `research_state/legacy_tooling/`，只供追溯，不作新研究入口。公共历史脚本在 `toolkit/legacy/`；原 README 在 `docs/history/`。迁移映射见 `docs/organization/relocated_tools.json`。

网页可包含静态依赖缺失、动态 API 或嵌入媒体限制；查看 metadata 的实际状态。原始响应和依赖不可原地编辑；Git 配置 `-text` 保留字节，完整原件与依赖由 .gitignore 排除，只在本地保存；clone 不会得到这些原件。完整核验需使用拥有本地 reference_metrial 的目录。
