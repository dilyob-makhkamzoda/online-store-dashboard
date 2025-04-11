# ddl.py
"""
Модуль инициализации базы данных DuckDB из Excel-файла.
Создаёт таблицы, представления и загружает данные.
"""

import duckdb
import pandas as pd

DB_PATH = "db/my.db"
EXCEL_PATH = "data/online_store_sales.xlsx"


def run_ddl():
    print(" Подключение к DuckDB...")
    con = duckdb.connect(DB_PATH)

    print(" Выполнение create_tables.sql...")
    with open("queries/create_tables.sql", "r", encoding="utf-8") as f:
        con.execute(f.read())

    print(" Загрузка Excel...")
    xls = pd.ExcelFile(EXCEL_PATH)

    df_clients = xls.parse("Clients").dropna(subset=["Clientid"]).copy()
    df_clients["Clientid"] = df_clients["Clientid"].astype(int)
    df_clients = df_clients.drop_duplicates(subset=["Clientid"])

    df_categories = xls.parse("Product_category").drop_duplicates().copy()
    df_products = xls.parse("Products").drop_duplicates(subset=["productid"]).copy()

    if "Sales" in xls.sheet_names:
        df_sales = xls.parse("Sales").dropna(subset=["clientid", "productid"]).copy()
    else:
        print(" Лист Sales не найден в Excel. Проверь название листа.")
        return

    print("Чистка данных...")
    df_clients["BirthDate"] = pd.to_datetime(df_clients["BirthDate"], errors="coerce")
    df_clients["DateFirstPurchase"] = pd.to_datetime(df_clients["DateFirstPurchase"], errors="coerce")

    df_sales["clientid"] = df_sales["clientid"].astype(int)
    df_sales["productid"] = df_sales["productid"].astype(int)
    df_sales["orderdate"] = pd.to_datetime(df_sales["orderdate"], errors="coerce")
    df_sales["reviewscore"] = pd.to_numeric(df_sales["reviewscore"], errors="coerce")

    df_sales = df_sales[df_sales["clientid"].isin(df_clients["Clientid"])]
    df_sales = df_sales[df_sales["productid"].isin(df_products["productid"])]

    print("Загрузка данных в БД...")
    con.execute("DELETE FROM course_project.sales;")
    con.execute("DELETE FROM course_project.products;")
    con.execute("DELETE FROM course_project.product_category;")
    con.execute("DELETE FROM course_project.clients;")

    con.register("clients_temp", df_clients)
    con.register("categories_temp", df_categories)
    con.register("products_temp", df_products)
    con.register("sales_temp", df_sales)

    con.execute("INSERT INTO course_project.clients SELECT * FROM clients_temp")
    con.execute("INSERT INTO course_project.product_category SELECT * FROM categories_temp")
    con.execute("INSERT INTO course_project.products SELECT * FROM products_temp")
    con.execute("INSERT INTO course_project.sales SELECT * FROM sales_temp")

    print("Создание представлений...")
    with open("queries/view.sql", "r", encoding="utf-8") as f:
        con.execute(f.read())

    print("DDL завершён. База и данные готовы.")


if __name__ == "__main__":
    run_ddl()