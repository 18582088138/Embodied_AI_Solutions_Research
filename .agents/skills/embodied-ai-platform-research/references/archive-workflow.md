# 统一归档操作与路径管理

## 部署和运行

Python 3.10+；下载器与检查器仅依赖标准库。先运行Skill中的部署器，复制工具到研究根目录的 `toolkit`，创建指定项目目录但不生成空报告或做网络请求。此后只能运行研究根目录中的下载器。平台项目必须位于该根目录下，不能指向根目录本身或toolkit/reference_metrial。

```text
python <skill目录>/scripts/bootstrap_research.py --root <研究根目录绝对路径> --project 01_Compute_Chips/02_Intel
python <研究根目录>/toolkit/download_materials.py --project 01_Compute_Chips/02_Intel --manifest <清单绝对路径> --dimension 01_Hardware_Platform
```

这里Intel只是路径示例，实际用用户目标。`--project`相对下载器所属研究根目录，不相对shell cwd。代理只用用户环境、`REFERENCE_DOWNLOAD_PROXY`或显式参数；不硬编码NVIDIA会话中的代理/用户名/网络地址。

清单放根目录 `toolkit/manifests/<平台>_<章节>.json`。推荐列表，每项 `name`（稳定唯一）、`url`（已定位原始公共URL）、`expected`（html/pdf/json/any）、`used_by`（章节列表）。同网址换name仍复用目录，不需要为每章节下载一份。

```json
[
  {
    "name": "Platform_Product_Datasheet",
    "url": "https://example.org/verified-datasheet.pdf",
    "expected": "pdf",
    "used_by": ["01_Hardware_Platform", "08_Core_Technology_Moat"]
  }
]
```

示例URL不能作为研究引用。实际使用前找到并验证厂商真实链接。每次读取运行返回码和 `_registry/last_run.json`，不能把过程启动视为下载成功。

## 每份资料单独目录

```text
<项目>/reference_metrial/
  index.html
  webpages/<简称--URL哈希>/
    index.html
    original.response
    metadata.json
    text.txt
    assets/styles|images|fonts|scripts|other/
  documents/<简称--URL哈希>/document.pdf + original.response + metadata.json
  data/<简称--URL哈希>/content.<原类型> + original.response + metadata.json
  _registry/materials.json + assets.json + unavailable.json + assets/ + last_run.json
  derived/figures|extracted|qa/
  02_software_depth/index.html + collection.json + <各材料独立目录>/
  08_core/index.html + collection.json + <各材料独立目录>/
```

保留项目现有拼写 `reference_metrial`。HTML不是纯TXT、截图或仅原始链接。保存原始响应字节、版本/采集时间/HTTP/类型/SHA256/缺失资源；本地化前后可见文本一致，CSS递归imports、图片、字体、本地引用一并管理。Windows名称自动截短并附URL哈希，长路径不可用时缩短研究根路径，不能删除哈希。

原件和硬链接资源视为只读。不要手动改CSS/HTML资产来掩盖失败；需要重新本地化用脚本显式修复。官方图从原件产生衍生文件，不覆盖原图。

## 去重、更新与专题目录

- 项目唯一registry按规范URL去重，去fragment、域名/默认端口规整，保留query。不同版本/query/镜像不随意合并；跨项目不自动共用路径。
- HTML页重叠依赖按URL和SHA校验后复用，同卷硬链接，否则本地复制。每页目录仍自包含；同URL跨维度只加别名/used_by。
- 已知失败依赖缓存，不在每章循环请求。默认重用成功/部分静态快照；`--repair-assets`仅用于实际修复缺失，`--refresh`用于明确需要更新正文，不能每次默认refresh。
- 同项目只能一个下载进程；`.reference_download.lock`不能在进程运行时删除。Windowsregistry可能被读取器短暂锁定，工具已有有限重试，不同时改写registry。
- 02独立专题目录：使用 `--collection 02_software_depth`，各篇复用共享registry。最终整理02总览与全部02A/02B等专题实际引用的联合清单再导出；不能只导出最后一篇而遗漏前面专题。各篇和联合导出分别保留去重记录，专题索引链接联合资料目录。新清单覆盖collection视图而不自动合并，行为与08相同。
- 08独立目录：先整理08实际引用来源的完整联合清单，再运行 `--collection 08_core`。同一collection的新清单覆盖索引的视图，不自动合并；因此最终要用总览和全部专题的联合清单，避免只导出08C把08A/B从索引遗漏。旧子目录不会自动删除。

```text
python <根>/toolkit/download_materials.py --project <平台项目相对路径> --manifest <08联合清单> --dimension 08_Core_Technology_Moat --collection 08_core
```

正文08本地参考优先链接collection路径；canonical registry仍是唯一事实登记。反复导出已归档材料应不发网络请求。final运行将 `last_run.json` 复制到对应章节QA（复制前确认本轮已退出，不并行读写）。

历史资料迁移仅在确实需要时用 `--import-dir`，并核对原始文件与URL。用户明确要求删除旧布局并重下载时，先列出准确的绝对目录、验证都在目标项目reference_metrial内，保留仍被其他报告引用的资源，删除所授权旧文件再通过统一脚本下载；不把本地import说成重新下载。普通调研不因Skill自动删除已有资料。

## 成功的含义与不能承诺的内容

`complete_static`：识别到的静态呈现依赖完整；`partial_static`：有呈现资源缺失；`failed`：正文/类型/一致性失败。HTTP200不代表真实文档，必须排除反爬挑战、空正文和LFS占位。

默认冻结可执行scripts，保留源码；`--scripts preserve`可保留执行，但动态API、登录、iframe、视频与交互不保证离线。正文一致不证明像素级一致。受robots、失效或限流影响时在metadata和报告注明；不得换域名/代理绕过限制后宣称完整归档。官方正文可查而依赖缺失时，可引用并清楚披露；正文失败不能引用。

不要无限爬整个站点；所有资料主文件和额外图URL均走此脚本，普通导航链接仍指原站。PDF读取/图像渲染可用环境工具，但不得用第二网络下载器抓原件。

## 验证

部署后可运行 `python -m unittest discover -s <根>/toolkit -p test_download_materials.py`；仅在工具初始化或变更时需要，不每章重复跑同一测试。测试使用本地HTTP服务，验证跨维度/跨运行去重、依赖/字体/图片/CSS循环、robots、类型、挑战页、修复与collection。

报告检查：`python <根>/toolkit/check_report.py --project <项目绝对路径> --report 01_Hardware_Platform.md --baseline <本章开始基线>`。默认trace为 `<项目>/research_state/evidence/01_Hardware_Platform.json`，格式见证据参考。失败候选允许留在公共registry；检查只针对当前引用，因此没有把检索失败误当整项目不可交付。
