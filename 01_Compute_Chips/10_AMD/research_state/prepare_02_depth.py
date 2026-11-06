"""Begin user-authorized 02 topic deepening; no downloads or report rewrites."""
import json,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
S=P/'research_state';D=S/'depth_02';D.mkdir(exist_ok=True)
baseline={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in P.glob('*.md')}
b=S/'baselines/02_depth_before.json'
if not b.exists():b.write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
topics=[
 ('02A_GPU_Execution_and_Deployment','GPU执行、图编译与模型部署'),
 ('02B_RyzenAI_Compilation_and_Quantization','Ryzen AI NPU编译、量化与异构推理'),
 ('02C_Versal_Compiler_and_Runtime','Versal编译器、张量布局与VART runtime'),
 ('02D_EDF_BSP_and_Execution_Domains','EDF/BSP、SHEL与多执行域'),
 ('02E_ROS_Acceleration_and_System_Integration','ROS加速、追踪与端到端系统集成')]
(D/'topics.json').write_text(json.dumps(topics,ensure_ascii=False,indent=2),encoding='utf-8')
f=S/'progress.json';p=json.loads(f.read_text(encoding='utf-8'))
p.update(authorization='用户明确02深度不足，授权参考08研究方法独立专题深度调研、分文件保存；当前仅补深02，不启动03。',
 review_status='02_topics_in_progress',current_dimension='02_Software_Stack',next_step='按02A—02E完成机制、官方资料/图/API核验和独立文件自检，再交付专题索引。')
p['software_depth_topics']=dict(planned=[x[0] for x in topics],completed=[],method='痛点→原理/数据流→API/实现→优势条件→官方测量→机制对标→版本/许可/失效→可复建验证')
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
targets={
 'AMD_HIP_Model':'https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html',
 'AMD_HIP_Graphs':'https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/hipgraph.html',
 'AMD_HIP_Coherence':'https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/memory_management/coherence_control.html',
 'AMD_HIP_Allocator':'https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/memory_management/stream_ordered_allocator.html',
 'AMD_HIP_Tuning':'https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html',
 'AMD_ROCm_GraphSafe':'https://rocm.docs.amd.com/en/latest/reference/graph-safe-support.html',
 'AMD_vLLM_Optimization':'https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/optimization/vllm-v1-optimization.html',
 'AMD_Acceleration_Libs':'https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/optimization/model-acceleration-libs.html',
 'AMD_ROCm_Isolation':'https://rocm.docs.amd.com/en/latest/reference/system-optimization/gpu-isolation.html'}
known={u.split('#')[0] for r in R.values() for u in r.get('links',[])}
assert set(targets.values()) <= known,set(targets.values())-known
manifest=[dict(name=n,url=u,expected='html',used_by=[topics[0][0]]) for n,u in targets.items()]
(P.parents[1]/'toolkit/manifests/AMD_02A_deep.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(baseline=str(b),topics=topics,initial_sources=len(manifest)),ensure_ascii=False))
