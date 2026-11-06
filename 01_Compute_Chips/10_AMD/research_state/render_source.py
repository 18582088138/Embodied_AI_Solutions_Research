import pathlib,json,sys,subprocess
P=pathlib.Path(__file__).resolve().parent.parent;R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf8'))
s=sys.argv[1];page=sys.argv[2];out=P/'reference_metrial/derived/figures'/('source_'+s+'_p'+page)
subprocess.run([r'C:\Users\kundaxu\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe','-f',page,'-singlefile','-scale-to','1800','-png',R[s]['file'],str(out)],check=True);print(str(out)+'.png')
