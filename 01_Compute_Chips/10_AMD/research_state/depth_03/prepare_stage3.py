import pathlib,json,hashlib
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];R=D.parents[3];items=[]
def add(n,u):items.append(dict(name=n,url=u,expected='html',used_by=['03_Sensor_Integration']))
base='https://xilinx.github.io/kria-apps-docs/kr260/ros2_multinode_communication_via_tsn/0_3/build/html/docs/'
for n,f in [('AMD_TSN_Intro','introduction.html'),('AMD_TSN_HW','hw_arch_platform.html'),('AMD_TSN_SW','sw_arch_platform.html'),('AMD_TSN_Deploy','app_deployment.html')]:add(n,base+f)
base='https://xilinx.github.io/kria-apps-docs/kr260/build/html/docs/'
add('AMD_PTP_Issues',base+'gps_1588_ptp/src/known-issues.html');add('AMD_MV_Sensor',base+'10gige_vision_camera/src/sensor.html')
add('AMD_CSI2_Driver','https://github.com/Xilinx/linux-xlnx/blob/master/drivers/media/platform/xilinx/xilinx-csi2rxss.c')
add('AMD_Video_DMA_Driver','https://github.com/Xilinx/linux-xlnx/blob/master/drivers/media/platform/xilinx/xilinx-dma.c')
add('AMD_IMX547_Repo','https://github.com/Xilinx/mv-camera-sensor-module');add('AMD_ISP_Repo','https://github.com/Xilinx/xilinx-isp-module')
add('AMD_Wiki_Linux','https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841996/Linux')
add('Linux_DMABUF_Sync','https://docs.kernel.org/driver-api/dma-buf.html');add('Linux_Network_Timestamps','https://docs.kernel.org/networking/timestamping.html');add('Linux_SocketCAN','https://docs.kernel.org/networking/can.html')
nr=json.loads((P.parent/'01_NVIDIA/reference_metrial/_registry/materials.json').read_text(encoding='utf8'));i=D/'imports';i.mkdir(exist_ok=True)
for name,s in [('Compare_03_HSB','NVIDIA_02_HSB_ARCH'),('Compare_03_CoE','NVIDIA_02_SIPL_COE')]:
 r=nr[s];o=pathlib.Path(r['original_file']);assert hashlib.sha256(o.read_bytes()).hexdigest()==r['original_sha256']
 (i/(name+'.meta.json')).write_text(json.dumps(dict(url=r['url'],status=200,file=str(o),sha256=r['original_sha256'],headers={'Content-Type':r['content_type']},final_url=r['final_url'],retrieved_at_utc=r['retrieved_at_utc'])),encoding='utf8');add(name,r['url'])
(R/'toolkit/manifests/AMD_03_stage3.json').write_text(json.dumps(items,indent=2),encoding='utf8');print(len(items))
