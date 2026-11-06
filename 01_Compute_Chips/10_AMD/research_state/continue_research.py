import pathlib,json,hashlib,sys,re
P=pathlib.Path(__file__).resolve().parent.parent;R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf8'))
if sys.argv[1]=='start':
 stem=sys.argv[2];d=P/'research_state'/('depth_'+stem[:2]);d.mkdir(exist_ok=True)
 b=P/'research_state/baselines'/(stem+'_before.json')
 if not b.exists():b.write_text(json.dumps({x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in P.glob('*.md')},indent=2),encoding='utf8')
 f=P/'research_state/progress.json';p=json.loads(f.read_text(encoding='utf8'))
 p['scope']='AMD具身智能01—09；01—03完成，03已获用户认可，04—09连续授权按序深入并归档'
 p['authorization']='用户：好的，按照这个质量继续04到09的调研。每章完成检查后继续，无逐章批准门槛。'
 p['review_status']='04_to_09_continuously_authorized';p['current_dimension']=stem;p['next_dimension']=stem;p['next_step']='完成当前章证据/正文/图/归档/检查后按序继续，直至09。'
 if '03_Sensor_Integration' not in p['approved_dimensions']:p['approved_dimensions'].append('03_Sensor_Integration')
 p['sensor_integration_review']['status']='approved_by_user'
 p['continuous_authorization']={'chapters':['04_AI_Capabilities','05_Simulation_Environment','06_Robot_Integration','07_Ecosystem','08_Core_Technology_Moat','09_SWOT_Analysis'],'user_instruction':'好的，按照这个质量继续04到09的调研','status':'active'}
 f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8');print(stem)
elif sys.argv[1]=='list':
 for s,r in R.items():
  if re.search(sys.argv[2],s,re.I):print(s,r.get('archive_status'),r['url'])
elif sys.argv[1]=='read':
 s=sys.argv[2];f=pathlib.Path(R[s]['file']);t=re.sub(r'\s+',' ',((f.parent/'text.txt') if (f.parent/'text.txt').exists() else f).read_text(encoding='utf8'))
 if len(sys.argv)==3:print(t)
 for pat in sys.argv[3:]:
  print('\n',s,pat)
  for m in list(re.finditer(pat,t,re.I))[:3]:print(t[max(0,m.start()-100):m.end()+850])
elif sys.argv[1]=='links':
 for s in sys.argv[2:-1]:
  print(s)
  for l in R[s].get('links',[]):
   u=l.get('url',l.get('href','')) if isinstance(l,dict) else l
   if re.search(sys.argv[-1],u,re.I):print(u)
elif sys.argv[1]=='assets':
 for s in sys.argv[2:]:
  for a in R[s].get('assets',[]):
   if re.search(r'\.(png|jpg|jpeg|svg|gif)($|\?)',a['url'],re.I) and not re.search('logo|fontawesome|favicon|icon|avatar',a['url'],re.I):print(s,a['url'],(P/'reference_metrial'/a.get('local_file',a['file'])).as_posix())
