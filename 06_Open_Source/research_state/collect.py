"""Use the repository downloader; keep all source bytes in each product archive."""
from pathlib import Path
import json, subprocess, sys, hashlib, os

ROOT = Path(__file__).resolve().parents[2]
CATEGORY = ROOT / '06_Open_Source'
SEEDS = {
 '21_LeRobot_SO101': {
  'LeRobot_README':'https://raw.githubusercontent.com/huggingface/lerobot/main/README.md',
  'LeRobot_LICENSE':'https://raw.githubusercontent.com/huggingface/lerobot/main/LICENSE',
  'SO101_Hardware':'https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/README.md',
  'SO101_Docs':'https://huggingface.co/docs/lerobot/so101',
 },
 '22_OpenArm': {
  'OpenArm_Web':'https://openarm.dev/',
  'OpenArm_Hardware':'https://raw.githubusercontent.com/enactic/openarm/main/README.md',
  'OpenArm_LICENSE':'https://raw.githubusercontent.com/enactic/openarm/main/LICENSE',
 },
 '23_ALOHA_Mobile_ALOHA': {
  'ALOHA_Web':'https://tonyzhaozh.github.io/aloha/',
  'ALOHA_README':'https://raw.githubusercontent.com/tonyzhaozh/aloha/main/README.md',
  'Mobile_ALOHA_Web':'https://mobile-aloha.github.io/',
  'Mobile_ALOHA_README':'https://raw.githubusercontent.com/MarkFzp/mobile-aloha/main/README.md',
  'ALOHA_LICENSE':'https://raw.githubusercontent.com/tonyzhaozh/aloha/main/LICENSE',
 },
 '24_Reachy2': {
  'Reachy_Web':'https://www.pollen-robotics.com/reachy/',
  'Reachy2_SDK':'https://raw.githubusercontent.com/pollen-robotics/reachy2-sdk/main/README.md',
  'Reachy2_SDK_LICENSE':'https://raw.githubusercontent.com/pollen-robotics/reachy2-sdk/main/LICENSE',
  'Reachy2_Docs':'https://docs.pollen-robotics.com/',
 },
 '25_Reachy_Mini': {
  'ReachyMini_README':'https://raw.githubusercontent.com/pollen-robotics/reachy_mini/main/README.md',
  'ReachyMini_LICENSE':'https://raw.githubusercontent.com/pollen-robotics/reachy_mini/main/LICENSE',
  'ReachyMini_Hardware':'https://raw.githubusercontent.com/pollen-robotics/reachy_mini_hardware/main/README.md',
  'ReachyMini_Web':'https://huggingface.co/spaces/pollen-robotics/Reachy_Mini',
 },
 '26_Berkeley_Humanoid_Lite': {
  'BHL_Web':'https://lite.berkeley-humanoid.org/',
  'BHL_README':'https://raw.githubusercontent.com/HybridRobotics/Berkeley-Humanoid-Lite/main/README.md',
  'BHL_LICENSE':'https://raw.githubusercontent.com/HybridRobotics/Berkeley-Humanoid-Lite/main/LICENSE',
 },
 '27_ToddlerBot': {
  'ToddlerBot_Web':'https://toddlerbot.github.io/',
  'ToddlerBot_README':'https://raw.githubusercontent.com/stanfordtoddlerbot/toddlerbot/main/README.md',
  'ToddlerBot_LICENSE':'https://raw.githubusercontent.com/stanfordtoddlerbot/toddlerbot/main/LICENSE',
 },
 '28_AgiBot_X1': {
  'X1_Hardware':'https://raw.githubusercontent.com/agibot-tech/agibot_x1_hardware/main/README.md',
  'X1_Infer':'https://raw.githubusercontent.com/agibot-tech/agibot_x1_infer/main/README.md',
  'X1_Train':'https://raw.githubusercontent.com/agibot-tech/agibot_x1_train/main/README.md',
 },
 '29_OpenLoong': {
  'OpenLoong_Web':'https://www.openloong.org.cn/',
  'OpenLoong_Hardware':'https://raw.githubusercontent.com/loongOpen/OpenLoong-Hardware/main/README.md',
  'OpenLoong_Control':'https://raw.githubusercontent.com/loongOpen/OpenLoong-Dyn-Control/main/README.md',
  'OpenLoong_LICENSE':'https://raw.githubusercontent.com/loongOpen/OpenLoong-Dyn-Control/main/LICENSE',
 },
}

def dump(p, data):
 p.parent.mkdir(parents=True, exist_ok=True)
 p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def collect(product, sources, stage):
 project = CATEGORY / product
 manifest = project / 'research_state/manifests' / (stage+'.json')
 entries=[dict(name=k,url=v,expected='any',used_by=['01_Product_Research']) for k,v in sources.items()]
 dump(manifest, entries)
 print('PRODUCT', product, flush=True)
 return subprocess.run([sys.executable,str(ROOT/'toolkit/download_materials.py'),'--project',str(project),
   '--manifest',str(manifest),'--timeout','18','--max-assets','45','--max-mb','30','--jobs','6','--delay','0.12']).returncode

if __name__ == '__main__':
 if len(sys.argv)==1:
  baseline=CATEGORY/'research_state/existing_reports_before.json'
  if not baseline.exists():
   before={}
   for base,dirs,files in os.walk(ROOT):
    dirs[:]=[d for d in dirs if d not in ('reference_metrial','.git','__pycache__')]
    for name in files:
     if name.endswith('.md'):
      p=Path(base)/name
      before[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
   dump(baseline, before)
  for product,sources in SEEDS.items(): collect(product,sources,'01_initial')
 else:
  payload=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
  for product,sources in payload.items():collect(product,sources,Path(sys.argv[1]).stem)
