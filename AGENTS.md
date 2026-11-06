# 本仓库工作约定

本文件适用于整个具身智能研究仓库。

- 优先读取目标分项 README、`research_state/progress.json` 和相关证据，续接既有研究。
- 使用仓库自带 `.agents/skills/embodied-ai-platform-research/SKILL.md` 及其参考规范。芯片平台的 01—09 维度按该 skill；其他类别沿用已有维度和统一证据/归档要求，不强套芯片模板。
- 资料通过 `toolkit/download_materials.py` 归档到所属分项 `reference_metrial/`。原件和依赖保持只读；不得以 TXT 替代新下载 HTML/PDF。
- 报告与导航使用仓库内相对链接；JSON 证据路径使用仓库根相对路径，公共工具负责解析。不要写入本机用户名、绝对工作目录或固定代理。
- 原有状态、原件日期、失败记录、章节基线和审阅记录必须保留。首轮简报、深度报告、用户批准和实机验收分别记录。
- 一个分项一个 commit，例如 `research(01_Compute_Chips/01_NVIDIA): organize reports and source catalog`。包含该分项报告、正文图表、来源清单、专题、索引与状态；完整原件留本地，不把其他分项混入。
- 后续每完成一个分项，完成适用校验并审阅 `git diff --cached --stat` 后提交、推送。用户已授权本项目 git push 和 branch 管理；无需重复请求批准。未完成分项需要备份时使用明确标识的工作分支与 WIP commit，不标记为完成。
- 公共 skill、工具、根导航的变更独立提交。推送前 fetch；远端新增提交时保留其历史，禁止默认 force push。不要暂存与本任务无关的用户更改。
- 主仓库只存报告、少量正文图表、来源清单、skill、工具与核验记录。完整原件及网页依赖留本地 `reference_metrial/`，由 .gitignore 排除；不上传 Git LFS。sources.json 保留 URL、本地路径与哈希，报告原件链接指向 REFERENCES.md。不得删除本地原件。
- 校验结构不能代替事实复核或实机测试。路径迁移的哈希变更单独记录，不覆盖历史基线证明。
