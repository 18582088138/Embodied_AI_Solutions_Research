"""Recheck the three existing first-round reports and record their actual status."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAT = ROOT / '06_Open_Source'
sys.path.insert(0, str(ROOT / 'toolkit'))
from archive_paths import portable


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(portable(value), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def validate():
    for name in ['21_LeRobot_SO101', '22_OpenArm', '23_ALOHA_Mobile_ALOHA']:
        project = CAT / name
        qa = project / 'research_state/archive_qa/01_Product_Research_quality.json'
        if not qa.exists():
            dump(qa, dict(outcome='pending', scope='Initial link target; replaced by the actual report check below.'))
        registry = json.loads((project / 'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
        trace = json.loads((project / 'research_state/evidence/01_Product_Research.json').read_text(encoding='utf-8'))
        manifest = project / 'research_state/manifests/final_reuse.json'
        dump(manifest, [dict(name=sid, url=registry[sid]['url'], expected='any', used_by=['01_Product_Research']) for sid in trace['source_ids']])
        result = subprocess.run([sys.executable, str(ROOT / 'toolkit/download_materials.py'), '--project', str(project),
                                 '--manifest', str(manifest), '--dimension', '01_Product_Research'], capture_output=True, text=True, encoding='utf-8')
        reuse = json.loads((project / 'reference_metrial/_registry/last_run.json').read_text(encoding='utf-8'))
        dump(project / 'research_state/archive_qa/final_reuse.json', reuse)
        print(name, 'reuse_returncode', result.returncode, flush=True)
        if result.returncode:
            print(result.stdout, result.stderr)
            return 1
        result = subprocess.run([sys.executable, str(ROOT / 'toolkit/check_report.py'), '--project', str(project),
                                 '--report', '01_Product_Research.md', '--baseline', str(project / 'research_state/baselines/01_Product_Research_before.json')],
                                capture_output=True, text=True, encoding='utf-8')
        actual = project / 'reference_metrial/derived/qa/01_Product_Research_quality.json'
        if actual.exists():
            shutil.copy2(actual, qa)
        quality = json.loads(qa.read_text(encoding='utf-8'))
        print(name, quality['outcome'], 'han', quality.get('body_han_chars'), 'sources', quality.get('sources'),
              'errors', quality.get('errors'), flush=True)
        if result.returncode:
            print(result.stdout, result.stderr)
            return 1
        state_path = project / 'research_state/progress.json'
        state = json.loads(state_path.read_text(encoding='utf-8'))
        state.update(authorization='用户要求在研究库增加开源具身智能方案子项目；当前续接已有产品级首轮报告并完成核验。',
                     completed_dimensions=['01_Product_Research'], current_dimension=None,
                     review_status='首轮报告已完成来源、图片与结构/归档复核；尚未取得用户审阅或实机验收',
                     report_depth='first_round_product_research', validation_on='2026-11-08 Asia/Shanghai',
                     next_step='按正文证据缺口补深；采购询价、完整许可审计和实机验证另记。')
        dump(state_path, state)
    return 0


if __name__ == '__main__':
    raise SystemExit(validate())
