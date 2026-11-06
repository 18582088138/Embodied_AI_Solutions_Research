"""Read archived sources only; no network or registry mutation."""
import argparse, json, pathlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from html.parser import HTMLParser

PROJECT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('names', nargs='*')
parser.add_argument('--links', action='store_true')
parser.add_argument('--pattern')
parser.add_argument('--extract-pdfs', action='store_true')
parser.add_argument('--embedded-specs', action='store_true')
args = parser.parse_args()
records = json.loads((PROJECT/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
for name in args.names or records:
    r = records.get(name, {})
    print('\nSOURCE',name,r.get('archive_status'),r.get('error',''))
    if not r.get('file'): continue
    p = pathlib.Path(r['file'])
    if args.embedded_specs:
        class Embedded(HTMLParser):
            def handle_starttag(self, tag, attributes):
                for key, value in attributes:
                    if value and len(value)>3000 and 'formatValue' in value:
                        try: obj=json.loads(value)
                        except ValueError: continue
                        out=PROJECT/'reference_metrial/derived/extracted'/f'{name}_{key}.json'
                        out.parent.mkdir(parents=True,exist_ok=True)
                        out.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
                        print('ATTRIBUTE',key,'JSON',out)
                        def visit(x):
                            if isinstance(x,list):
                                for item in x:visit(item)
                            elif isinstance(x,dict):
                                if 'elements' in x:
                                    print(json.dumps({'title':x.get('title'), 'elements':{k:{'label':v.get('title'), 'value':v.get('formatValue',v.get('value'))} for k,v in x['elements'].items()}},ensure_ascii=False))
                                else:
                                    for item in x.values():visit(item)
                        visit(obj)
        Embedded().feed(p.read_text(encoding='utf-8'))
        continue
    if p.suffix == '.pdf' and args.extract_pdfs:
        from pypdf import PdfReader
        reader = PdfReader(p)
        out = PROJECT/'reference_metrial/derived/extracted'/f'{name}.txt'
        out.parent.mkdir(parents=True, exist_ok=True)
        texts = [f'\n=== PAGE {i+1} ===\n'+page.extract_text() for i,page in enumerate(reader.pages)]
        out.write_text(''.join(texts), encoding='utf-8')
        print('PAGES',len(reader.pages),'METADATA',reader.metadata)
        content=''.join(texts)
    elif p.suffix == '.html':
        content = (p.parent/'text.txt').read_text(encoding='utf-8')
        if 'Español' in content: content=content.rsplit('Español',1)[-1]
        content=content.split('Subscribe to the latest')[0]
    else: continue
    if args.links:
        for link in r.get('links',[]):
            text=json.dumps(link,ensure_ascii=False)
            if '#' in text: continue
            if not args.pattern or re.search(args.pattern,text,re.I): print(text)
    elif args.pattern:
        intervals=[]
        for m in re.finditer(args.pattern, content, re.I):
            left,right=max(0,m.start()-170),m.end()+550
            if intervals and left <= intervals[-1][1]: intervals[-1]=(intervals[-1][0],max(right,intervals[-1][1]))
            else: intervals.append((left,right))
        for left,right in intervals: print(content[left:right])
    else: print(content)
