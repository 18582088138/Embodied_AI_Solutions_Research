"""One-time migration of old CLI entry points to the unified downloader."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
WRAPPER='''"""Compatibility entry point; delegates all downloads to the project toolkit."""
import pathlib, runpy, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
args = sys.argv[1:]
if args and not args[0].startswith('--'):
    args = ['--manifest', args[0], *args[1:]]
DEFAULT_PROJECT
sys.argv = [str(ROOT / 'Embodied_AI_Solutions_Research/toolkit/download_materials.py'), *args]
runpy.run_path(sys.argv[0], run_name='__main__')
'''
for name in ('collect_sources.py','collect_panorama_sources.py','research_nvidia_hardware.py'):
    default="if '--project' not in args:\n    args += ['--project', '01_Compute_Chips/01_NVIDIA']" if name=='research_nvidia_hardware.py' else ''
    (ROOT/'scripts'/name).write_text(WRAPPER.replace('DEFAULT_PROJECT',default),encoding='utf-8')
    print('Updated',name)
