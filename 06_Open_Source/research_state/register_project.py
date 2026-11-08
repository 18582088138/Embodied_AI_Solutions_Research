"""Register the existing open-source research materials without altering originals."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAT = ROOT / '06_Open_Source'
sys.path.insert(0, str(ROOT / 'toolkit'))
from prepare_git_sources import prepare

PRODUCTS = {
    '21_LeRobot_SO101': ('LeRobot / SO-101', '桌面操作与学习闭环'),
    '22_OpenArm': ('OpenArm', '双臂接触操作与开放硬件'),
    '23_ALOHA_Mobile_ALOHA': ('ALOHA / Mobile ALOHA', '双臂模仿学习与移动示教'),
    '24_Reachy2': ('Reachy 2', '成套双臂移动平台与SDK'),
    '25_Reachy_Mini': ('Reachy Mini', '桌面交互、应用开发与开放边界'),
    '26_Berkeley_Humanoid_Lite': ('Berkeley Humanoid Lite', '低成本人形硬件与运动控制'),
    '27_ToddlerBot': ('ToddlerBot', '小型人形运动与操作学习'),
    '28_AgiBot_X1': ('AgiBot X1 / 智元灵犀X1', '国内人形、BOM与训练/推理链路'),
    '29_OpenLoong': ('OpenLoong / 青龙', '全尺寸人形硬件、动力学控制与仿真'),
    '30_XLeRobot': ('XLeRobot', '低成本移动双臂与社区集成'),
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def register():
    baseline = CAT / 'research_state/registration_before.json'
    if not baseline.exists():
        dump(baseline, {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in CAT.glob('[0-9][0-9]_*/*.md')})
    rows = []
    for name, (title, focus) in PRODUCTS.items():
        project = CAT / name
        registry = json.loads((project / 'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
        valid = {key: record for key, record in registry.items() if record['archive_status'] != 'failed'}
        state_path = project / 'research_state/progress.json'
        if not state_path.exists():
            dump(state_path, dict(platform=title, scope=focus, research_type='product_multidimensional',
                                 authorization='用户要求增加开源具身智能方案子项目；当前登记候选资料与后续研究范围。',
                                 completed_dimensions=[], current_dimension='source_review_and_scope',
                                 review_status='候选资料已归档；尚无产品报告、用户审阅或实机验收',
                                 data_cutoff='2026-11-08 Asia/Shanghai',
                                 pending_evidence='候选来源的事实、分层许可、价格/配置与复现条件待逐项深入核验。',
                                 next_step='按RESEARCH_PLAN.md顺序核验来源并撰写01_Product_Research.md。'))
        prepare(project)
        if not (project / 'README.md').exists():
            links = []
            for sid, record in valid.items():
                if 'LICENSE' in sid or not record.get('file'):
                    continue
                if Path(record['file']).suffix not in ('.html', '.md', '.txt'):
                    continue
                links.append(f'- [{sid}]({record["url"]})')
                if len(links) == 3:
                    break
            text = f'# {title}\n\n[返回开源方案总览](../README.md) · [研究计划](../RESEARCH_PLAN.md) · [研究首页](../../README.md)\n\n'
            text += f'研究重点：{focus}。当前已登记{len(valid)}条成功归档来源和{len(registry)-len(valid)}条失败候选；尚未交付产品报告。网页的静态依赖完整度、失败原因与实际采集日期见来源清单。\n\n'
            text += '## 候选官方/作者入口\n\n' + '\n'.join(links) + '\n\n'
            text += '## 后续调研\n\n按统一九项问题核查硬件与版本、控制/学习链路、模型与数据、分层许可、价格包含项、国内外获取和复现条件，再形成产品级报告。仓库公开不等于全部硬件、固件、权重和数据已开放；候选资料不能替代事实审阅与实机测试。\n\n'
            text += '- [来源与本地原件目录](REFERENCES.md)\n- [URL、路径与SHA256](sources.json)\n- [研究状态](research_state/progress.json)\n'
            (project / 'README.md').write_text(text, encoding='utf-8')
        state = json.loads(state_path.read_text(encoding='utf-8'))
        done = '01_Product_Research' in state.get('completed_dimensions', [])
        rows.append((name, title, focus, done))
    readme = '# 开源具身智能方案\n\n新增日期：2026-11-08（Asia/Shanghai）。研究库第六类，覆盖本体、控制、遥操作、数据和学习相连的开源方案。\n\n[研究首页](../README.md) · [调研计划与统一问题](RESEARCH_PLAN.md) · [研究进度](research_state/progress.json) · [导航校验](research_state/navigation_quality.json)\n\n'
    readme += '候选名单包含不同开放程度的方案，开放范围须分别核验硬件、代码、固件、权重、数据与依赖。产品级首轮报告、用户审阅和实机验收分别记录。\n\n## 首批研究对象\n\n'
    for name, title, focus, done in rows:
        status = '首轮产品报告已核验，待用户审阅' if done else '候选资料已归档，产品报告待编写'
        readme += f'- [{title}]({name}/README.md) — {focus}；{status}。\n'
    readme += '\n## 资料与使用\n\n'
    summary = 'presentations/output/开源具身智能方案_3页正文_2026-11-08.pptx'
    if (CAT / summary).exists():
        readme += f'[三页正文汇总PPT]({summary})：方案全景、代表项目的能力与成本、按任务选型及验证重点。[来源与交付记录](presentations/summary_manifest.json)。\n\n'
    readme += '每个产品独立保存报告、来源清单与研究状态；HTML/PDF原件和依赖留在其本地reference_metrial/，不上传Git。清单保留真实采集时间、URL、SHA256、失败候选和依赖缺失。首轮报告可用于研究导航与PoC候选筛选；报价、完整许可和实机性能按报告中的缺口继续核验。\n'
    (CAT / 'README.md').write_text(readme, encoding='utf-8')
    completed = [name for name, _, _, done in rows if done]
    dump(CAT / 'research_state/progress.json', dict(project='开源具身智能方案', category='06_Open_Source',
        initiated_on='2026-11-08 Asia/Shanghai', authorization='在Embodied_AI_Solutions_Research中增加一个“开源具身智能方案”的子项目的调研工作',
        project_registered=True, phase='first_round_reports_and_candidate_registration',
        planned_products=list(PRODUCTS), completed_first_round_products=completed,
        pending_products=[name for name in PRODUCTS if name not in completed],
        user_review_status='未取得用户审阅', hardware_validation_status='未开展实机测试',
        next_step='Reachy 2为下一份产品报告，按研究计划逐项继续；已交付三篇按各自缺口补深。'))


if __name__ == '__main__':
    register()
