# 统一参考资料下载工具

后续资料统一通过 `download_materials.py` 下载到对应项目的 `reference_metrial`，不向共享 `_Evidence` 新增下载。Python 3.10+，下载器仅依赖标准库。

## 目录管理

```text
reference_metrial/
  index.html                         可点击资料索引
  webpages/
    简称--URL哈希/
      index.html                     本地网页
      original.response              原始HTTP响应字节
      metadata.json                  URL、时间、哈希、别名、维度、缺失依赖
      text.txt                       正文检索文本
      assets/
        styles/                      CSS和递归import
        images/                      图片
        fonts/                       字体
        scripts/                     脚本
        other/                       其他资源
  documents/
    简称--URL哈希/
      document.pdf
      original.response
      metadata.json
  data/
    简称--URL哈希/
      content.json 或 content.txt 等
      original.response
      metadata.json
  _registry/
    materials.json                   名称索引：同URL多个名称共用一个目录
    assets.json                      项目内依赖URL缓存
    unavailable.json                 已知失败依赖，显式修复时才重试
    assets/                          共用资源缓存
    last_run.json                    运行结果及网络请求计数
  derived/
    figures/                         官方PDF渲染图片
    extracted/                       PDF抽取文本
    qa/                              校验结果和离线预览
```

目录简称会根据Windows路径长度预算自动截短，完整名称仍保留在索引及metadata，URL哈希保证唯一性。网页的HTML、CSS、图片和字体均位于自己的子目录，复制整个网页目录即可携带已归档静态资源。缓存和每页资源通过硬链接共享文件内容；硬链接不可用时复制，不再请求网络。CSS相对路径在每页结构内有效。不要手动编辑硬链接资源，因为内容会被多个页面共用。

`original.response`保留原始字节，包括服务器返回的gzip压缩；编码信息见metadata。TXT用于检索，不替代HTML。

## 使用方法

从仓库根目录执行；Python不在PATH时使用可执行文件绝对路径：

```powershell
python Embodied_AI_Solutions_Research/toolkit/download_materials.py `
  --project 01_Compute_Chips/01_NVIDIA `
  --url https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/ `
  --name NVIDIA_Product_Page_Jetson_Thor --expected html `
  --dimension 01_Hardware_Platform
```

批量清单支持名称到URL的JSON对象，推荐列表格式：

```json
[
  {
    "name": "NVIDIA_Product_Page_Jetson_Thor",
    "url": "https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/",
    "expected": "html",
    "used_by": ["01_Hardware_Platform", "02_Software_Stack"]
  }
]
```

```powershell
python Embodied_AI_Solutions_Research/toolkit/download_materials.py `
  --project 01_Compute_Chips/01_NVIDIA `
  --manifest Embodied_AI_Solutions_Research/toolkit/manifests/NVIDIA_materials.json
```

代理通过 `--proxy` 或 `REFERENCE_DOWNLOAD_PROXY` 指定，未指定时遵循系统设置。不要在清单内保存凭据。

## 去重规则

专题需要独立参考文件夹时，给同一批清单增加`--collection 08_core`。工具在`reference_metrial/08_core/`生成独立索引和每份材料子目录，包含HTML、CSS、图片、字体、原始响应及metadata。材料仍由项目唯一registry按URL去重：已有正文不重新下载，同卷优先硬链接共享存储，硬链接不可用时只从本地复制。再次运行不会重复建立相同文件。`collection.json`记录专题路径、规范归档路径和哈希；它是清单视图，不是第二套下载registry。归档文件按只读使用，避免直接修改共享硬链接。更换清单不会自动删除旧子目录，索引只列本次清单，清理需核验明确路径。

- 同一项目以规范化原始URL识别资料：去fragment，统一域名大小写和默认端口；保留query，防止不同版本误合并。
- 相同URL换名称或维度仍指向同一物理目录；metadata记录全部`aliases`和`used_by`。默认重复运行，完整和部分依赖缺失的资料都复用，不再抓正文。
- 不同网页的重叠依赖按URL和SHA256校验后复用，递归CSS依赖也复用；每页仍有自己的资源目录。
- 已知失败依赖跨运行复用失败记录，避免反复请求；修复时才显式重试。文件损坏或缺失时重建；正文原始响应完好时不重新抓正文。`--repair-assets`显式重建页面并重试缺失依赖；`--refresh`显式重新抓正文，完整依赖仍复用。
- 无法仅凭URL判断不同网址内容相同；不随意合并镜像网址、query或不同项目。去重范围是一个项目。
- 同项目进程锁`.reference_download.lock`防止同时启动多个下载器。异常强制终止后，仅在确认原进程退出时清理残留锁。

全部重新下载时先核验精确资料路径，移除旧资料再运行批量命令，不使用`--import-dir`冒充重下载。`--import-dir`仅用于显式迁移已核验快照，并记录迁移来源。

## 一致性与限制

保留原页面结构和静态正文，HTML本地化前后比较可见文本；CSS调整资源引用。普通超链接指向原站，不无限抓取全站。默认冻结可执行脚本，原内容仍保存；`--scripts preserve`可保留执行，但动态API、登录、视频和iframe不保证离线可用。

`complete_static`表示识别到的静态呈现依赖完整；`partial_static`表示呈现资源缺失；`failed`表示正文、类型或一致性检查失败。全部缺失资源及原因保存在metadata，冻结脚本另行标记。静态正文一致不代表动态交互或在线页面像素级一致。`--strict`使部分呈现缺失也返回非零；正文失败始终返回非零。

遵循robots.txt，无法检查时停止访问该域名并记录原因。默认每主机间隔0.3秒，4路并发，单响应100MB、单次新增依赖2500、超时25秒。参数：`--delay`、`--jobs`（1–8）、`--max-mb`、`--max-assets`、`--timeout`。`--expected pdf`防止HTML误当PDF；HTTP200不代表内容已经人工核验。

## 验证和维护

```powershell
python Embodied_AI_Solutions_Research/toolkit/test_download_materials.py
python Embodied_AI_Solutions_Research/toolkit/check_reference_archive.py `
  --project Embodied_AI_Solutions_Research/01_Compute_Chips/01_NVIDIA
```

本地HTTP测试覆盖跨维度和跨运行复用、跨网页依赖去重、CSS循环和相对路径、字体图片、压缩、PDF、robots及缺失资源修复。归档校验不访问网络。

历史三个下载入口已转发统一工具。NVIDIA构建器只更新指定硬件报告，不运行`build_panorama_research.py`。`migrate_nvidia_references.py`为旧布局一次性迁移脚本，不适用于当前结构。
