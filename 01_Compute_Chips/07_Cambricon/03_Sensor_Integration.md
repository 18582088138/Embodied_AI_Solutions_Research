# 寒武纪 Cambricon — 传感器接入

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 硬件接口
MLU220-SOM列双千兆网口、I2C/SPI/UART/GPIO、PCIe/SDIO及视频/JPEG编解码；本轮产品规格未列完整MIPI/ISP/GMSL2原生摄像头链，不把编解码等同ISP采集。M.2卡通过PCIe接主机。[cambricon-mlu220-som](#cambricon-mlu220-som)[cambricon-mlu220-m2](#cambricon-mlu220-m2)
### 同步与融合
SOM可通过载板/网络输入传感数据，M.2则由主机采集后传到加速器；需确认相机/ToF/IMU/LiDAR驱动、设备时间、PTP、DMA拷贝和推理队列。
缺口：硬件触发、ISP配置、具体Orbbec/RoboSense测试矩阵、六维力接口与完整低延迟融合库。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="cambricon-mlu220-som"></a> **cambricon-mlu220-som**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=56)｜[本地归档](REFERENCES.md#legacy-5596ebfce51310b1)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-mlu220-m2"></a> **cambricon-mlu220-m2**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=57)｜[本地归档](REFERENCES.md#legacy-1bd739a38b050b37)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
