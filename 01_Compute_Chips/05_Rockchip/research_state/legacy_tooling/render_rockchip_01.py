import pathlib,json,subprocess,hashlib
from PIL import Image
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
out=p/'derived/figures';out.mkdir(parents=True,exist_ok=True)
sha=lambda f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
fig=[]
c=json.loads((out/'candidates.json').read_text(encoding='utf-8'))
for i,name in [(2,'RK3588S_Chip_Block_Radxa'),(3,'CM5_System_Block_Radxa'),(9,'ROCK4D_v112_Interface_Radxa')]:
 a=c[i];f=out/(name+'.png');im=Image.open(a['file']).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);bg.convert('RGB').save(f)
 fig.append(dict(file=f.as_posix(),sha256=sha(f),source_id=a['source_id'],source_url=a['source_url'],original_file=a['file'],original_sha256=sha(a['file']),operation='原始WebP完整转为PNG，透明区域合成白底，未裁剪'))
pop=pathlib.Path('C:/Users/kundaxu/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
for n,page,name in [('Firefly_RK182X_Kit_PDF',3,'Firefly_RK182X_DualM2_Overview'),('Firefly_RK182X_Kit_PDF',4,'Firefly_RK182X_DualM2_Spec'),('Firefly_RK182X_Kit_PDF',24,'Firefly_RK182X_Model_Benchmark'),('Radxa_ROCK5BPlus_Schematic_v121',3,'ROCK5BPlus_v121_Block')]:
 v=r[n];prefix=out/name
 subprocess.run([str(pop),'-f',str(page),'-l',str(page),'-r','110','-singlefile','-png',v['file'],str(prefix)],check=True)
 f=prefix.with_suffix('.png');fig.append(dict(file=f.as_posix(),sha256=sha(f),source_id=n,source_url=v['url'],original_file=v['file'],original_sha256=v['sha256'],operation=f'Poppler pdftoppm渲染PDF第{page}页，110dpi完整页，未裁剪'))
(out/'selected_trace.json').write_text(json.dumps(fig,ensure_ascii=False,indent=2),encoding='utf-8')
print([f['file'] for f in fig])
