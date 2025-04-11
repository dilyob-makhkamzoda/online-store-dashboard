-- view.sql

CREATE OR REPLACE VIEW course_project.sales_extended AS
SELECT
    s.sale_id,
    s.clientid,
    s.orderdate,
    s.productid,
    s.amount,
    s.payment_method,
    s.city,
    s.reviewscore,
    s.saledate,
    c.Name AS client_name,
    c.gender,
    c.age,
    c.MaritalStatus,
    c.DateFirstPurchase,
    p.productname,
    p.price,
    pc.categoryname,
    (p.price * s.amount) AS revenue
FROM course_project.sales s
LEFT JOIN course_project.clients c ON s.clientid = c.Clientid
LEFT JOIN course_project.products p ON s.productid = p.productid
LEFT JOIN course_project.product_category pc ON p.categoryid = pc.categoryid;
