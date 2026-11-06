import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).resolve().parents[1]/'01_Compute_Chips/06_Huawei_HiSilicon'
r=json.loads((p/'reference_metrial/_registry/materials.json').read_text('utf-8'))
mode=sys.argv[1]
if mode=='pdf':
    from pypdf import PdfReader
    for i,x in enumerate(PdfReader(r['HiSilicon_AcademyPDF']['file']).pages):
        print('PAGE',i+1,(x.extract_text() or '')[:2300])
elif mode=='images':
    for n in sys.argv[2:]:
        print('IMAGES',n,json.dumps(r[n]['images'],ensure_ascii=False)[:18000])
elif mode=='assets':
    from PIL import Image
    for n in sys.argv[2:]:
        print('ASSETS',n)
        for a in r[n].get('assets',[]):
            if '/dam/asset/view/' in a['url']:
                f=p/'reference_metrial'/a.get('local_file',a['file'])
                try:
                    im=Image.open(f)
                    if min(im.size)>100: print(im.size,a['url'],f)
                except Exception: pass
elif mode=='links':
    for n in sys.argv[2:]:
        print('LINKS',n)
        for a in r[n]['links']:
            if any(k in str(a).lower() for k in ['3559','white','pdf','hardware','200i','dk','datasheet']): print(a)
elif mode=='text':
    for n in sys.argv[2:]:
        t=(pathlib.Path(r[n]['file']).parent/'text.txt').read_text('utf-8')
        a=t.find('关键特性');b=t.find('感兴趣的产品');print(n,t[max(a,0):b if b>=0 else None])
