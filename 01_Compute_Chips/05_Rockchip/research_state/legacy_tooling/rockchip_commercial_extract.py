import pathlib,json,re
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
for n in ['Firefly_ROC_RK3588S','Firefly_RK182X_Kit','Radxa_ROCK5T_Power','Radxa_ROCK5T_Product']:
 f=pathlib.Path(r[n]['file']);t=f.with_name('text.txt').read_text(encoding='utf-8')
 print(n)
 if n.startswith('Firefly'):
  i=t.find('View all ROC-RK3588S-PC');print(t[i:i+1900])
  for m in re.finditer(r'Spec:|RAM:|Parameter:|Configuration:|Regular price Add to cart',t): print(t[max(0,m.start()-160):m.start()+500])
 else:
  i=t.find(' Parameter Configuration');print(t[i:i+4300]) if i>=0 else print(t[-4000:])
