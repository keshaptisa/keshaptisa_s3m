"""Определяет архитектуру модели по её весам.

Нужен, потому что конфигурация прогона `dino448_s2` не зафиксирована в ноутбуке
напарника: там текущий run_tag `eva448`, комментарий указывает на eva02 для
`dino448_v2`, а rebuild_specs для `dino448` — на vit_small_patch14_dinov2.
Формы параметров снимают неоднозначность однозначно.

Запуск:  python scripts/identify_backbone.py путь/к/архиву.zip
"""
import sys, zipfile, tempfile
from pathlib import Path

import torch


def identify(state_dict):
    sd = state_dict.get('state_dict', state_dict) if isinstance(state_dict, dict) else state_dict
    keys = list(sd.keys())
    emb = next((tuple(v.shape) for k, v in sd.items()
                if k.endswith('patch_embed.proj.weight')), None)
    n_blocks = len({k.split('blocks.')[1].split('.')[0] for k in keys if 'blocks.' in k})
    has_reg = any('reg_token' in k for k in keys)
    # EVA-02 использует rotary position embedding — у DINOv2 таких параметров нет
    has_rope = any(('rope' in k.lower()) or ('freqs' in k.lower()) for k in keys)

    print(f'ключей: {len(keys)}')
    print(f'patch_embed.proj.weight: {emb}')
    print(f'блоков: {n_blocks} | reg_token: {has_reg} | rope/freqs: {has_rope}')

    if emb is None:
        return 'не опознано: нет patch_embed'
    dim = emb[0]
    if has_rope:
        return 'eva02_base_patch14_448.mim_in22k_ft_in22k_in1k'
    if dim == 384:
        return 'vit_small_patch14_reg4_dinov2.lvd142m' if has_reg else 'vit_small_patch14_dinov2.lvd142m'
    if dim == 768:
        return 'vit_base_patch14_reg4_dinov2.lvd142m' if has_reg else 'vit_base_patch14_dinov2.lvd142m'
    if dim == 1024:
        return 'vit_large_patch14_reg4_dinov2.lvd142m'
    return f'не опознано: ширина {dim}'


def main(path):
    path = Path(path)
    if path.suffix == '.zip':
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            print(f'файлов в архиве: {len(names)}')
            for m in sorted(names):
                print(f'  {m:<52s} {z.getinfo(m).file_size / 1e6:8.1f} МБ')
            weights = [m for m in names if m.endswith(('.pth', '.pt'))]
            if not weights:
                print('\nвесов в архиве нет'); return
            with tempfile.TemporaryDirectory() as tmp:
                z.extract(weights[0], tmp)
                sd = torch.load(Path(tmp) / weights[0], map_location='cpu', weights_only=False)
    else:
        sd = torch.load(path, map_location='cpu', weights_only=False)

    arch = identify(sd)
    print(f'\nархитектура: {arch}')
    print(f"\nCONFIG = dict(run_tag='dino448_s2', backbone='{arch}',\n"
          f"              tile=448, backbone_lr=4e-5, batch_size=6,\n"
          f"              accum=4, layer_decay=0.75)")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'sber_meshqc_dino448_s2.zip')
