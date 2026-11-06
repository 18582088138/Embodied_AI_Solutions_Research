import pathlib,json
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3];items=[]
base='https://xilinx.github.io/kria-apps-docs/kr260/build/html/docs/'
for name,path in [
 ('AMD_MV_Overview','10gige_vision_camera/src/overview.html'),('AMD_MV_Intro','10gige_vision_camera/src/introduction.html'),
 ('AMD_MV_Deploy','10gige_vision_camera/src/app_deployment.html'),('AMD_MV_HW','10gige_vision_camera/src/10gige.html'),
 ('AMD_MV_ISP','10gige_vision_camera/src/hw_arch_accel_dd.html'),('AMD_MV_SW','10gige_vision_camera/src/sw_arch_platform_dd.html'),
 ('AMD_MV_App','10gige_vision_camera/src/sw_arch_accel_dd.html'),('AMD_MV_Debug','10gige_vision_camera/src/debug.html'),('AMD_MV_Issues','10gige_vision_camera/src/known_issues.html'),
 ('AMD_PTP_Deploy','gps_1588_ptp/src/app_deployment.html'),('AMD_PTP_HW','gps_1588_ptp/src/hw_arch_platform.html'),('AMD_PTP_SW','gps_1588_ptp/src/sw_arch_platform.html')]:
 items.append(dict(name=name,url=base+path,expected='html',used_by=['03_Sensor_Integration']))
items.append(dict(name='AMD_TSN_Landing',url='https://xilinx.github.io/kria-apps-docs/kr260/ros2_multinode_communication_via_tsn/0_3/build/html/ros2_multinode_communication_via_tsn_landing.html',expected='html',used_by=['03_Sensor_Integration']))
(R/'toolkit/manifests/AMD_03_stage2.json').write_text(json.dumps(items,indent=2),encoding='utf8')
print(len(items))
