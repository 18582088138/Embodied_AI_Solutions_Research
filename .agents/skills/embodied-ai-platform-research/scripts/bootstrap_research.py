"""Deploy the bundled archive and report tools without downloads or overwrites."""
import argparse, hashlib, json, pathlib, shutil
from datetime import datetime, timezone

FILES=('download_materials.py','test_download_materials.py','check_report.py','archive_paths.py','prepare_git_sources.py','organize_repository.py','verify_repository.py')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True,type=pathlib.Path)
    parser.add_argument('--project',required=True,help='Project path relative to the research root')
    args=parser.parse_args();root=args.root.resolve();relative=pathlib.Path(args.project)
    if relative.is_absolute():parser.error('--project must be relative to --root')
    project=(root/relative).resolve()
    if project==root or not project.is_relative_to(root):parser.error('project escapes research root')
    if any(x in ('toolkit','reference_metrial','_Evidence') for x in project.relative_to(root).parts):
        parser.error('project cannot be an evidence or toolkit directory')
    source=pathlib.Path(__file__).resolve().parent;toolkit=root/'toolkit'
    if not toolkit.resolve().is_relative_to(root):parser.error('toolkit resolves outside research root')
    # Validate every destination before writing any file. Never overwrite a different version.
    for name in FILES:
        src=source/name;dest=toolkit/name
        if not src.is_file():parser.error('missing bundled tool: '+name)
        if dest.exists() and (not dest.is_file() or dest.read_bytes()!=src.read_bytes()):
            parser.error('existing tool differs; inspect compatibility before updating: '+str(dest))
    project.mkdir(parents=True,exist_ok=True);toolkit.mkdir(parents=True,exist_ok=True)
    for name in FILES:
        dest=toolkit/name
        if not dest.exists():shutil.copy2(source/name,dest)
    (toolkit/'manifests').mkdir(exist_ok=True)
    for folder in ('evidence','baselines'):(project/'research_state'/folder).mkdir(parents=True,exist_ok=True)
    deployment=dict(skill='embodied-ai-platform-research',deployed_at_utc=datetime.now(timezone.utc).isoformat(),
        root=root.as_posix(),project=project.as_posix(),
        tools={name:hashlib.sha256((toolkit/name).read_bytes()).hexdigest() for name in FILES})
    (project/'research_state/toolkit_deployment.json').write_text(json.dumps(deployment,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(deployment,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
