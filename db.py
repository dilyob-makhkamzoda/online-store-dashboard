# db.py
"""
Модуль для подключения к базе данных DuckDB и получения датафреймов
"""

import duckdb
import pandas as pd

DB_PATH = "db/my.db"


def get_connection():
    """Создаёт и возвращает подключение к DuckDB"""
    return duckdb.connect(DB_PATH)


def fetch_table(table_name: str) -> pd.DataFrame:
    """Возвращает датафрейм из таблицы по её имени"""
    con = get_connection()
    return con.execute(f"SELECT * FROM course_project.{table_name}").df()


def fetch_joined_data() -> pd.DataFrame:
    """
    Возвращает объединённый датафрейм из таблиц sales, clients, products и product_category
    """
    con = get_connection()
    query = """
        SELECT s.*, 
               c.Name AS client_name, c.gender, c.age, c.MaritalStatus, c.DateFirstPurchase,
               p.productname, p.price,
               cat.categoryname
        FROM course_project.sales s
        LEFT JOIN course_project.clients c ON s.clientid = c.Clientid
        LEFT JOIN course_project.products p ON s.productid = p.productid
        LEFT JOIN course_project.product_category cat ON p.categoryid = cat.categoryid
    """
    return con.execute(query).df()


def fetch_monthly_revenue() -> pd.DataFrame:
    """Группировка выручки по месяцам"""
    con = get_connection()
    query = """
        SELECT DATE_TRUNC('month', orderdate) AS month,
               SUM(p.price * s.amount) AS revenue
        FROM course_project.sales s
        JOIN course_project.products p ON s.productid = p.productid
        GROUP BY month
        ORDER BY month
    """
    return con.execute(query).df()
