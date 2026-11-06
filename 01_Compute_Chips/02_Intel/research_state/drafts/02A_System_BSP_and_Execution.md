# 02A｜系统、BSP、驱动与执行域：从可启动到可复建的机器人环境

截止2026-11-05；本篇为第02章首个独立专题。核验对象是官方Suite固定源码、Intel GPU/NPU公开驱动说明与第01章准确硬件。本文没有安装软件、修改本机驱动或运行模型；“可复建”表示复现所需对象和验证路径已明确，不表示本研究已完成复现。

## 1. 核心问题：芯片被识别并不等于应用可交付

机器人同时依赖OS内核、板级固件、图形计算runtime、NPU编译器、相机驱动、ROS和模型部署包。一台主机能正常显示桌面，只证明部分图形路径工作；NPU没有设备节点、驱动编译器不匹配或ROS包装库链接了不同OpenVINO，仍会使部署失败。Intel的价值是把这些层通过APT仓库、配置脚本、镜像模板和参考Blueprint组织起来，代价是必须维护这套组合的版本关系。不能将“x86支持Ubuntu”扩大为全部Core Ultra、任意内核与全部Suite样例共同验收。[[Intel02A_Install]]、[[Intel02A_Configurations]]。

![Intel官方Suite软件与系统层架构]([[FIG:Intel02_Architecture]])

图1为官方SVG的完整浏览器渲染。蓝色是Intel提供或优化，绿色是ROS等上游软件，灰色是用户本体、传感器和数据。第四层把Ubuntu、RT内核、BSP、传感器驱动和EtherCAT并列，说明这些是AI模型以下的交付依赖。图中同时出现22.04/Humble与24.04/Jazzy，不等于当前每个SKU支持两套环境；准确配置须读以下表格。[[Intel02_Architecture]]。

## 2. 当前配置与旧参考环境须分开

| 对象 | 本轮官方配置 | 关键绑定 | 可以说明 | 不能说明 |
|---|---|---|---|---|
| Core Ultra Series3/Series2 | Ubuntu24.04 64-bit Desktop、ROS2 Jazzy | 配置表包含AMR、固定臂、人形Blueprint | 当前Suite配置入口 | 任意载板、每个模型和旧驱动都验收 |
| Core Series3 | 同上 | 配置表仅列AMR、固定臂 | 软件范围比硬件品牌更窄 | Core5 320可直接复制人形RT/模型配置 |
| 手动安装路径 | OpenVINO2025.3.0；oneAPI2026.1.* | 四个OpenVINO/ROS包同版本pin；ROS节点优先级1002 | 当前安装指南的版本约束 | 通用2026文档API已在此BKC存在 |
| 255H旧人形参考配置 | Ubuntu22.04、ROS2 Humble、ECI6.12.8相关内核 | 准确配置见硬件Blueprint | 历史/特定样例可复建基线 | 当前手动安装支持任意22.04机器 |

前三行来自安装与配置源码，最后一行来自已归档的255H人形Blueprint。手动指南开头只明确Ubuntu24.04，但后文仍保留Humble标签页；本篇不自行把它们归并为新的统一支持承诺。安装指南固定`openvino-libraries-dev`、`openvino`、ROS wrapper和node到2025.3.0，并要求改版本时四者一致。APT的1001/1002优先级可能影响包选择，不能只保存pip版本而忽略系统库；应记录`apt-cache policy`与已安装包清单。[[Intel02A_Install]]、[[Intel02A_Configurations]]、[[Intel_Doc_Humanoid]]。

## 3. GPU执行：Loader、前端、共享核心和内核驱动

GPU公开runtime称NEO，提供OpenCL和Level Zero两个API前端。官方架构把设备枚举、内存管理、命令生成、提交、同步放到`shared/`，前端将API对象映射到共享核心；Linux后端使用i915/xe DRM，Windows是WDDM，共享部分源码但构建路径有区别。用户程序应链接Level Zero loader或OpenCL ICD loader，而非直接链接runtime私有库。Suite安装`libze1`和`libze-intel-gpu1`；显示驱动与GPU计算用户态包不是同一层。[[Intel02A_GPU_Runtime]]、[[Intel02A_GPU_Architecture]]、[[Intel02A_Install]]。

一次计算请求在NEO中经Device、EngineControl、CommandStreamReceiver和OsContext形成硬件命令并提交。MemoryManager属于ExecutionEnvironment，管理GraphicsAllocation、地址空间、驻留与主机指针；一个进程内共享管理器不意味着CPU/GPU/NPU所有buffer天然共享，更不保证跨进程ROS消息零拷贝。设备家族、SKU和stepping通过GfxCoreHelper、ProductHelper、ReleaseHelper等选择能力与workaround，因而相同API也可能在不同SKU产生不同执行路径。应用若依赖私有调试环境变量或内部数据结构，公开README明确它们可能改变，应把稳定API和调试工具分开。[[Intel02A_GPU_Architecture]]、[[Intel02A_GPU_Runtime]]。

分析：GPU计算部署失败应按设备权限→loader枚举→用户态runtime→编译器/内核→模型顺序定位，避免直接将编译错误归因于模型。GPU节点通常为`/dev/dri/renderD*`，容器需显式映射设备和正确组权限；镜像能启动不证明宿主DRM、IGC/GmmLib与容器runtime兼容。正式验证应保存枚举结果、具体PCI ID、驱动包来源和首次编译日志，再检查目标模型及稳定负载。

## 4. NPU执行域：编译器、用户态驱动、内核与固件

NPU官方overview的链条是OpenVINO NPU plugin→Level Zero loader→`intel-level-zero-npu`与`intel-driver-compiler-npu`→`intel_vpu.ko`→`intel-fw-npu`。用户态库名为`libze_intel_npu.so`，driver compiler为`libnpu_driver_compiler.so`；旧VPU命名仍留在Linux内核。不能因为安装OpenVINO Python包就认为NPU固件和设备访问已完成。[[Intel02A_NPU_Overview]]、[[Intel02A_NPU_Driver]]。

官方overview记录Panther Lake从v1.28.0、Wildcat Lake从v1.32.0加入支持；这是该驱动家族的版本起点，不是Suite当前整机BKC、所有kernel版本和所有模型的最低充分条件。尤其手动指南按“Core Ultra”判断是否安装NPU，而新版driver已列Wildcat Lake，Core5 320的ARK也有NPU：文档存在适用范围差异，不能把旧判断自动变成Core Series3没有NPU。量产应读取准确release的kernel/firmware/compiler组件矩阵，本文没有从分支README反推安装包版本。[[Intel02A_NPU_Overview]]、[[Intel02A_Install]]、[[Intel_ARK_Core5320]]。

设备节点为`/dev/accel/accel0`，安装指南要求render组与udev权限。`modinfo intel_vpu`回答模块是否存在，加载与设备节点回答运行层是否就绪；OpenVINO的`available_devices`才回答插件是否能枚举目标设备，最后的模型编译/推理才验证算子与执行。日志的DEVICE、DRIVER、CACHE分类和驱动验证程序可辅助排障；官方说明不带YAML时某配置检查会失败，不能把所有测试的非零退出一概解释成硬件故障。固件重载、udev规则和容器访问须考虑重启后状态。[[Intel02A_NPU_Overview]]、[[Intel02A_Install]]。

## 5. 镜像和实时内核：产物及更新边界

Image Composer的ISO用于交互式安装，raw用于存储/虚拟机直接部署。Suite指南列Go1.24+、mmdebstrap、systemd-ukify等依赖，分别构建工具和live-installer，再用`ubuntu24-x86_64-robotics-jazzy-iso.yml`模板生成镜像。这能减少逐机配置差异，但模板是输入，不是包版本锁文件；仓库变化、APT解析和外部资源变化仍可产生不同镜像。应保存模板、工具revision、包列表、下载源、构建日志与最终SHA256。本文不执行写盘命令，也不把可启动ISO称为已实现OTA回退。[[Intel02A_ImageComposer]]。

RT内核从ECI仓库安装`eci-customizations`及`linux-intel-rt`，前沿芯片可涉及`linux-intel-rt-experimental`，需同时核验firmware与GRUB实际启动项。源码指南要求通过uname确认PREEMPT_RT，Secure Boot冲突可采用签名内核路径；本研究没有改变安全设置。LTS与experimental是不同更新责任，后者支持新硅片不等于有同等长期维护保证。板级BIOS、相机桥接、NIC和驱动仍以准确整机为准，不能把一个通用Linux包称为完整生产BSP。[[Intel02A_RTKernel]]、[[Intel_Doc_RT_Tuning]]。

## 6. 许可、机制对照与可复建验收

| 层次 | 已核验许可/交付证据 | 尚需确认的资产 | 验收动作 |
|---|---|---|---|
| Suite公开根代码 | 根Apache2.0 | 子目录、外部SDK、模型/数据 | 保存各组件许可，不以根许可统包 |
| GPU/NPU公开驱动代码 | README明确MIT、文件SPDX | 发行包、固件、外部编译器及通知 | 准确release的软件清单和第三方声明 |
| Ubuntu/RT镜像 | 开源内核构建与Canonical商标说明 | 镜像再发行、包许可、签名与服务 | SBOM、签名、升级及恢复演练 |
| 安全指南入口 | Suite指向Open Edge Platform安全文档 | 精确板卡IFWI、TME/TPM/安全配置 | 核对正式平台手册，本篇不宣称认证 |

表中证据来自根LICENSE、驱动README和系统指南；失败的猜测LICENSE路径没有进入有效来源。安全入口只证明指向哪些建议，不足以证明任一机器人已开启可信启动、磁盘加密或具备功能安全。[[Intel_Robotics_License]]、[[Intel02A_GPU_Runtime]]、[[Intel02A_NPU_Driver]]、[[Intel02A_RTKernel]]、[[Intel02A_Security]]。

与Jetson等整套BSP路线作机制对照：Intel的模块化Linux仓库和上游ROS便于复用x86开发资产，但宿主内核、GPU/NPU用户态和模型插件的组合由集成者锁定；将它视作一种维护分工分析，不输出跨平台性能排名。下一专题接收的是可枚举CPU/GPU/NPU、准确OS/kernel/driver/firmware清单及有权限的设备；交付给模型层的是runtime能力，而非跨设备通用engine。验收依次验证包来源与版本、重启后节点权限、设备枚举、一个固定shape模型、并发热稳态、更新后的恢复和失效诊断；所有步骤应留日志，不能以单次安装成功替代长期运行证据。
