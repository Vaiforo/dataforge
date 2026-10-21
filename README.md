# Cart Scope

Аналитика покупательских сессий интернет-магазина. Сейчас проект сравнивает
модели логистической регрессии и оценивает вероятность покупки на данных
Online Shoppers Purchasing Intention.

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
