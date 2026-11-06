# 持续调研与分项提交

本项目把 `类别/分项` 作为版本管理单元，例如 `01_Compute_Chips/01_NVIDIA`。本次已获用户授权提交、推送和管理分支；后续每完成一个分项，按以下流程保存。

1. 读取目标分项 README 与 `research_state/progress.json`，确认实际授权范围、完成章节和待核验项。
2. 使用 [仓库调研 skill](.agents/skills/embodied-ai-platform-research/SKILL.md)。新平台先部署工具；现有工具版本不同需先检查兼容，不能覆盖。
3. 报告放在分项根目录，保持既有章节命名；软件与核心技术专题分别用 `02A_…`、`08A_…`，提供专题目录。
4. 原文及依赖归档到分项 `reference_metrial/`，元数据保留 URL、实际采集日期、SHA256、完整度和失败记录。当前整理没有补做研究或重新下载原件。
5. 逐章按 skill 校验，并人工核验关键事实、条件与图像；保留原始审阅状态。运行 `python toolkit/organize_repository.py --build-indexes` 更新导航并检查相对链接。`--normalize` 仅用于一次性导入旧绝对路径资料，不在每轮研究重复运行。
6. 完整原件、网页依赖与媒体只保存本地，由 `.gitignore` 排除；不上传 Git/LFS。运行导航工具时生成 REFERENCES.md / sources.json，并把正文直接引用图表复制到 assets/figures。暂存前确认 sources.json 的 URL、实际日期、本地路径和哈希齐全；clone 不会自动获得原件。
7. `git fetch origin` 后检查分支。通常在 `main` 提交已完成分项；有并行或未完成工作时使用 `research/<分项名>`。保留远端历史。
8. 暂存目标分项，检查内容，再创建一条清晰 commit 并 push。公共工具和根索引的变化独立提交；分项中引用的历史资料副本也要包括。

示例：

```text
git add -- 01_Compute_Chips/01_NVIDIA
git diff --cached --stat
git commit -m "research(01_Compute_Chips/01_NVIDIA): archive reports and references"
git push origin main
```

首次整理的首轮全景报告、关系图谱、旧统计和共享 `_Evidence` 保留作历史证据。当前查阅入口是根与各分项 README；`research-index.json`、`validation.json` 反映整理后的文件和链接。旧章节哈希与核验记录不作为整理后字节未变的证明，迁移前后哈希分别保留。

## 复用 skill

仓库内 skill 位于 `.agents/skills/embodied-ai-platform-research/`，包含 SKILL、参考规范、下载器、部署器与测试。可直接由支持项目 skill 的客户端发现，或将整个目录复制到自己的 skills 目录。Python 3.10+；公共工具仅依赖标准库。

```text
python .agents/skills/embodied-ai-platform-research/scripts/bootstrap_research.py --root . --project 01_Compute_Chips/<序号_平台>
```

这只创建目录并部署工具，不自动发起其他厂商调研。其他研究类别沿用自己的章节维度，复用证据、归档与分项提交规范。
