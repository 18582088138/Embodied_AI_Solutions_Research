import pathlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
for n in sys.argv[1:]:
 v=r[n];print(n,v.get('error',''))
 if not v.get('file'):continue
 t=pathlib.Path(v['file']).read_text(encoding='utf-8')
 print(t[:1200]);print('MARKDOWN LINKS',re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',t));print('IMAGES',re.findall(r'<img[^>]+src=["\']([^"\']+)',t));print('LINKS',v.get('links',[]))
