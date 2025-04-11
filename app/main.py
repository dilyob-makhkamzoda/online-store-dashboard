# main.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# 🛠️ Автоинициализация базы, если она не существует
if not os.path.exists("db/my.db"):
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import ddl
    ddl.run_ddl()


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import fetch_joined_data


st.set_page_config(page_title="Онлайн-продажи", layout="wide")

st.title("📊 Аналитика онлайн-продаж")
st.markdown("Аналитическая панель по данным интернет-магазина")

# 📥 Загрузка данных из БД
@st.cache_data
def load_data():
    df = fetch_joined_data()
    df["revenue"] = df["price"] * df["amount"]
    df["orderdate"] = pd.to_datetime(df["orderdate"])
    return df

df = load_data()

# 📍 Боковая панель фильтров
with st.sidebar:
    st.header("Фильтры")
    cities = st.multiselect("Города", df["city"].dropna().unique())
    categories = st.multiselect("Категории", df["categoryname"].dropna().unique())

# 🔍 Фильтрация
df_filtered = df.copy()
if cities:
    df_filtered = df_filtered[df_filtered["city"].isin(cities)]
if categories:
    df_filtered = df_filtered[df_filtered["categoryname"].isin(categories)]

# 📈 KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔁 Продаж", f"{df_filtered['amount'].sum():,.0f}")
col2.metric("👥 Клиентов", df_filtered['clientid'].nunique())
col3.metric("💰 Средняя цена", f"{df_filtered['price'].mean():.2f} $")
col4.metric("📦 Выручка", f"{df_filtered['revenue'].sum():,.0f} $")

# 📊 Графики
st.subheader("📦 Продажи по категориям")
fig1 = px.bar(
    df_filtered.groupby("categoryname")["amount"].sum().sort_values().reset_index(),
    x="amount", y="categoryname", orientation="h",
    title="Объём продаж по категориям"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🏙️ Топ городов")
fig2 = px.bar(
    df_filtered.groupby("city")["amount"].sum().sort_values(ascending=False).head(10).reset_index(),
    x="city", y="amount",
    title="Города с наибольшим количеством заказов"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📆 Выручка по месяцам")
df_filtered["month"] = df_filtered["orderdate"].dt.to_period("M").astype(str)
fig3 = px.line(
    df_filtered.groupby("month")["revenue"].sum().reset_index(),
    x="month", y="revenue",
    title="Динамика выручки по месяцам"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🧍 Распределение по полу")
gender_data = df_filtered["gender"].value_counts().reset_index()
gender_data.columns = ["gender", "count"]
fig4 = px.pie(gender_data, values="count", names="gender", title="Гендерное распределение клиентов")
st.plotly_chart(fig4, use_container_width=True)

