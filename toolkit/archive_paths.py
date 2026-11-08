"""Portable repository paths for archive metadata (Python standard library)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = ('01_Compute_Chips/', '02_Core_Components/', '03_Robot_Manufacturers/',
            '04_AI_Models/', '05_Software_and_OS/', '06_Open_Source/',
            'toolkit/', '_Evidence/', '.agents/')


def map_values(value, transform):
    if isinstance(value, dict):
        return {k: map_values(v, transform) for k, v in value.items()}
    if isinstance(value, list):
        return [map_values(v, transform) for v in value]
    return transform(value) if isinstance(value, str) else value


def portable(value, root=ROOT):
    prefix = root.as_posix().rstrip('/') + '/'
    def convert(text):
        normalized = text.replace('\\', '/')
        if normalized.casefold().startswith(prefix.casefold()):
            return normalized[len(prefix):]
        if normalized.casefold() == root.as_posix().casefold():
            return '.'
        return text
    return map_values(value, convert)


def restore(value, root=ROOT):
    def convert(text):
        if text.startswith(PREFIXES):
            return (root / text).as_posix()
        return text
    return map_values(value, convert)


def load_json(path):
    return restore(json.loads(Path(path).read_text(encoding='utf-8-sig')))
