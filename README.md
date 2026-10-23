# Cart Scope

Аналитика покупательских сессий интернет-магазина. Сейчас проект сравнивает
модели логистической регрессии и оценивает вероятность покупки на данных
Online Shoppers Purchasing Intention.
Отдельный пример на Mushrooms демонстрирует обработку категориальных данных.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Откройте `notebooks/session_conversion.ipynb` и выполните ячейки по порядку.
В Windows окружение активируется командой `.venv\Scripts\Activate.ps1`.

## Данные

Поместите CSV из [UCI](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)
в `data/raw/online_shoppers_intention.csv`, затем создайте копии с пропусками:

```bash
python -m src.data.create_missing_sessions
```

Если производные файлы уже есть, этот шаг пропустите. При настроенном хранилище
данные можно получить через `dvc pull`. Текущее хранилище DVC локальное;
для настройки: `dvc remote add --local -d local ../cart-scope-dvc-storage`.

## Результаты

- Обработка, подбор параметров и выводы – в ноутбуке.
- Метрики и график – в `reports/conversion/`.
- Полный конвейер – `models/session_conversion.pkl`, загрузка через `cloudpickle.load`.
- Данные и модель отслеживаются DVC. После переобучения:
  `dvc add models/session_conversion.pkl`.

Оценка относится к завершённым сессиям; качество прогноза до покупки не проверено.
Перед коммитом выводы ноутбука очищаются, результаты сохраняются в отчётах.

## Классификация грибов

[Ноутбук](notebooks/mushroom_classification.ipynb) использует
[Mushrooms из OpenML](https://www.openml.org/d/24): файл `data/raw/mushroom.arff`.
Разделение 80/20, признак редкости `odor`, заполнение пропусков, кодирование
и логистическая регрессия объединены в Pipeline.

Accuracy: **0,9988**, ROC-AUC: **1,0000** (округлено); 2 ошибки на 1 625 тестовых
объектах. Пример сохраняет задачу определения съедобности и не моделирует покупки.
Все этапы и выводы находятся в ноутбуке.

Модель `models/mushroom.pkl` сохраняется через стандартный `pickle`.
Перед её загрузкой выполните ячейку с определением `RareOdorCounter`.
Данные и модель отслеживаются DVC:

```bash
dvc add data/raw/mushroom.arff models/mushroom.pkl
```
