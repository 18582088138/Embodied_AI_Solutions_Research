import pathlib,json,hashlib,sys
root=pathlib.Path(__file__).resolve().parent.parent;p=root/'01_Compute_Chips/05_Rockchip';s=p/'research_state'
def baseline(stem):
 f=s/'baselines'/f'{stem}_before.json'
 if not f.exists():f.write_text(json.dumps({x.relative_to(p).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in p.rglob('*.md')},indent=2),encoding='utf-8')
if __name__=='__main__':
 baseline('02_Software_Stack');baseline('02A_BSP_Multimedia')
 v=json.loads((s/'progress.json').read_text(encoding='utf-8'));v.update(authorization='用户继续02，视为01通过并授权第2章总览及必要专题；03尚未启动',review_status='01 approved; 02 in_progress',current_dimension='02',next_step='按02A→02B→02C→02D→02E逐篇调研、归档和检查，汇总02；本轮交付02')
 v['software_depth_topics']=dict(planned=['02A_BSP_Multimedia','02B_RKNN2_Compiler_Runtime','02C_RKLLM','02D_RKNN3_RK182X','02E_ROS_Control_Operations'],completed=[],current_topic='02A_BSP_Multimedia',checks={},review_status='user authorized chapter 02')
 (s/'progress.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
