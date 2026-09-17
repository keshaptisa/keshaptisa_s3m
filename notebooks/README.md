# Notebook Map

Основная последовательность сохранена под едиными именами `sber_v1`–`sber_v8`. Папка `archive/` содержит уникальные контрольные и альтернативные сборки из рабочего архива.

## Основная линия

| Файл | Исходная роль | Outputs |
|---|---|---:|
| [`sber_v1.ipynb`](sber_v1.ipynb) | ранний v5, чистый код multi-view + geometry | нет |
| [`sber_v2.ipynb`](sber_v2.ipynb) | v5 с фактическими outputs; источник результата 14.987 | да |
| [`sber_v3.ipynb`](sber_v3.ipynb) | v7, два бэкбона в одном проходе | да |
| [`sber_v4.ipynb`](sber_v4.ipynb) | v7 fixed, исправленная рабочая копия | да |
| [`sber_v5.ipynb`](sber_v5.ipynb) | v8, 336/448 + ML-Decoder + weighted ensemble | нет |
| [`sber_v6.ipynb`](sber_v6.ipynb) | v9 lean, ViT-B/14 + EVA-02-B/14 @336 | нет |
| [`sber_v7.ipynb`](sber_v7.ipynb) | финальная сборка трёх конфигураций | нет |
| [`sber_v8.ipynb`](sber_v8.ipynb) | обучение трёх веток с нуля отдельными процессами | нет |

## Архив доказательств

| Файл | Зачем сохранён |
|---|---|
| [`dino448_s2_source.ipynb`](archive/dino448_s2_source.ipynb) | фактический исходник сильнейшей ветки DINOv2 ViT-S/14 @448 |
| [`postprocessing_addon.ipynb`](archive/postprocessing_addon.ipynb) | бэггинг правила, глобальные веса и пороги по доле |
| [`v6_dinov3.ipynb`](archive/v6_dinov3.ipynb) | эксперимент с DINOv3, cross-view и soft-F1 |
| [`v7_two_backbones_clean.ipynb`](archive/v7_two_backbones_clean.ipynb) | чистая контрольная версия v7 |
| [`v8_resolution_mldecoder.ipynb`](archive/v8_resolution_mldecoder.ipynb) | контрольная версия v8 из архива |
| [`final_solution_15541.ipynb`](archive/final_solution_15541.ipynb) | сборочный ноутбук, описывающий импорт трёх источников и результат 15.541 |
| [`final_solution_three_trainable.ipynb`](archive/final_solution_three_trainable.ipynb) | вариант с тремя обучаемыми источниками |
| [`final_solution_two_models.ipynb`](archive/final_solution_two_models.ipynb) | упрощённый вариант на двух моделях |
| [`train_only.ipynb`](archive/train_only.ipynb) | облегчённый pipeline без EDA и второго уровня |

Ноутбук напарницы намеренно не опубликован: репозиторий хранит наши эксперименты. Использованная оттуда идея согласования меток описана в журнале без распространения чужого кода.
