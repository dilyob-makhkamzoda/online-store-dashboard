# 🧠 Проект: Анализ продаж онлайн-магазина

## 📌 Описание
Курсовой проект по дисциплине "Анализ данных". Цель — провести анализ данных интернет-магазина, визуализировать ключевые метрики через дашборд и задеплоить его с помощью Streamlit.

Автор: **Makhkamzoda Dilyob & Bomulloev Fazliddin**

**Makhkamzoda Dilyob:https://github.com/dilyob-makhkamzoda/**  
**Bomulloev Fazliddin:https://github.com/FazlBomulloev/**


## 📂 Структура репозитория
```
online_store_dashboard/
├── app/                 # streamlit-дашборд
│   └── main.py
├── db/                  # база данных
│   └── my.db
├── data/                # рабочая копия исходных файлов
│   └── online_store_sales.xlsx
├── eda/                 # EDA-анализ
│   ├── eda.ipynb
│   └── summary.md
├── queries/             # SQL-скрипты
│   ├── create_tables.sql
│   ├── view.sql
│   └── queries.sql
├── ddl.py               # создание и наполнение БД
├── db.py                # функции доступа к БД
├── requirements.txt     # зависимости проекта
└── README.md
```

## 📊 Используемый датасет
- **Источник:** собственный датасет, собранный из симулированных данных
- **Структура:** 4 таблицы (sales, clients, products, product_category)
- **Связи:** по внешним ключам (clientid, productid, categoryid)

## ⚙️ Используемые технологии
- `DuckDB` — база данных в памяти
- `pandas` — анализ данных
- `plotly`, `matplotlib`, `seaborn` — визуализация
- `streamlit` — интерактивный дашборд
- `scipy.stats` — проверка статистических гипотез

## 🔍 Что реализовано:
- EDA-анализ и гипотезы в `eda.ipynb`
- SQL-запросы с оконными функциями, агрегацией, датами
- Дашборд с KPI, фильтрами и графиками

## 🚀 Деплой дашборда
**Streamlit Cloud:** [ссылка появится после загрузки](https://streamlit.io/cloud)

## 📝 Как запустить локально
```bash
# Установка окружения
python -m venv venv
source venv/bin/activate    # или venv\Scripts\activate на Windows
pip install -r requirements.txt

# Запуск ETL
python ddl.py

# Запуск дашборда
streamlit run app/main.py
```

