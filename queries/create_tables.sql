CREATE SCHEMA IF NOT EXISTS course_project;

CREATE TABLE IF NOT EXISTS course_project.clients (
    Clientid INTEGER PRIMARY KEY,
    Name TEXT,
    BirthDate DATE,
    MaritalStatus TEXT,
    Address TEXT,
    Phone TEXT,
    DateFirstPurchase DATE,
    gender TEXT,
    age INTEGER
);

CREATE TABLE IF NOT EXISTS course_project.product_category (
    categoryid INTEGER PRIMARY KEY,
    categoryname TEXT
);

CREATE TABLE IF NOT EXISTS course_project.products (
    productid INTEGER PRIMARY KEY,
    productname TEXT,
    price DOUBLE,
    categoryid INTEGER,
    FOREIGN KEY (categoryid) REFERENCES course_project.product_category(categoryid)
);

CREATE TABLE IF NOT EXISTS course_project.sales (
    sale_id INTEGER PRIMARY KEY,
    clientid INTEGER,
    orderdate DATE,
    productid INTEGER,
    amount INTEGER,
    payment_method TEXT,
    city TEXT,
    reviewscore DOUBLE,
    saledate TEXT,
    FOREIGN KEY (clientid) REFERENCES course_project.clients(Clientid),
    FOREIGN KEY (productid) REFERENCES course_project.products(productid)
);
