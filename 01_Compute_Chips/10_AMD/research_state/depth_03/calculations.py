import json,pathlib
D=pathlib.Path(__file__).resolve().parent;rows=[]
for fps in [120,122]:
 for bits in [8,10,12,16]:
  r=2472*2128*fps*bits;rows.append(dict(width=2472,height=2128,fps=fps,storage_bits_per_pixel=bits,payload_Gbps=r/1e9,payload_MBps=r/8/1e6,formula='width*height*fps*storage_bits_per_pixel',status='分析，非实测；packed位深和16bit slot假设独立，不含协议/blanking'))
traverse=1920*1080*3*60
o=dict(raw_payload=rows,active_pixel_capacity_Mpixel_s=4*237.6,DDR=dict(single_traverse_MB_s=traverse/1e6,three_memory_to_memory_stages_GB_s=traverse*6/1e9,four_stream_payload_GB_s=traverse*4/1e9,extra_copy_read_write_four_stream_GB_s=traverse*4*2/1e9,conditions='1080pRGB8@60；3阶段各完整读写一次或4stream假设；不含capture/display/CCA额外pass，不证明目标并发支持'),age=dict(queued_frames=3,fps=60,conditional_wait_ms=3/60*1000,status='条件估算，非实测，不含曝光处理'))
(D/'calculations.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf8');print('calculation inputs/results saved')
