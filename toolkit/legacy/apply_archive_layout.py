"""Rebase archive metadata after relayout_current_archive.ps1; no downloads."""
import json,pathlib
from download_materials import save_json
root=pathlib.Path(__file__).resolve().parents[1]/'01_Compute_Chips/01_NVIDIA/reference_metrial'
root=root.resolve()
moves=json.loads((root/'_registry/layout_moves.json').read_text(encoding='utf-8-sig'))
if isinstance(moves,dict):moves=[moves]
def rebase(value):
    for move in moves:
        if value==move['from'] or value.startswith(move['from']+'\\'):return move['to']+value[len(move['from']):]
    return value
records=json.loads((root/'_registry/materials.json').read_text(encoding='utf-8'))
for record in records.values():
    for key in ('file','original_file'):
        if record.get(key):record[key]=rebase(record[key])
    for asset in record.get('assets',[]):
        if asset.get('local_file'):
            absolute=str(root/asset['local_file'])
            asset['local_file']=pathlib.Path(rebase(absolute)).relative_to(root).as_posix()
    location=record.get('file',record.get('original_file'))
    if location:save_json(pathlib.Path(location).parent/'metadata.json',record)
save_json(root/'_registry/materials.json',records)
print('Rebased',len(records),'metadata records')
