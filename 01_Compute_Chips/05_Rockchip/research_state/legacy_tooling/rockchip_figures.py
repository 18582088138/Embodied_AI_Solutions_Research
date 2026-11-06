import pathlib,json,sys
from PIL import Image,ImageDraw
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
selected=[]
for n in ['Radxa_CM5','Radxa_ROCK4D','Rockchip_Multicard_2026','Firefly_RK182X_Kit']:
 v=r[n]
 for a in v.get('assets',[]):
  f=p/a.get('local_file',a['file'])
  try:
   im=Image.open(f)
   if im.width<500 or im.height<200:continue
   selected.append(dict(source_id=n,file=f.as_posix(),source_url=a['url'],sha256=a['sha256'],size=im.size))
  except Exception:continue
out=p/'derived/figures';out.mkdir(parents=True,exist_ok=True)
(out/'candidates.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
for start in range(0,len(selected),20):
 subset=selected[start:start+20];sheet=Image.new('RGB',(1200,280*((len(subset)+3)//4)),'white');d=ImageDraw.Draw(sheet)
 for j,a in enumerate(subset):
  im=Image.open(a['file']).convert('RGB');im.thumbnail((290,235));x=(j%4)*300;y=(j//4)*280
  sheet.paste(im,(x,y));d.text((x,y+238),str(start+j)+' '+a['source_id'],fill='black')
 sheet.save(out/('contact_'+str(start)+'.png'))
print('Candidates',len(selected));print([(i,a['source_id'],a['size'],a['source_url']) for i,a in enumerate(selected)])
