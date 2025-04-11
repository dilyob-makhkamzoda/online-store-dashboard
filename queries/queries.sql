-- queries.sql

-- 1. Топ категорий по выручке
SELECT categoryname, SUM(revenue) AS total_revenue
FROM course_project.sales_extended
GROUP BY categoryname
ORDER BY total_revenue DESC;

-- 2. Средняя оценка по категориям
SELECT categoryname, ROUND(AVG(reviewscore), 2) AS avg_score
FROM course_project.sales_extended
GROUP BY categoryname
ORDER BY avg_score DESC;

-- 3. Средний чек по полу
SELECT gender, ROUND(AVG(revenue), 2) AS avg_revenue
FROM course_project.sales_extended
GROUP BY gender;

-- 4. Доля повторных клиентов
WITH purchase_counts AS (
    SELECT clientid, COUNT(*) AS total_orders
    FROM course_project.sales_extended
    GROUP BY clientid
),
repeat_stats AS (
    SELECT
        SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) AS repeat_count,
        COUNT(*) AS total_clients
    FROM purchase_counts
)
SELECT 
    repeat_count,
    total_clients,
    ROUND(100.0 * repeat_count / total_clients, 1) AS repeat_rate_pct
FROM repeat_stats;

-- 5. Оконная функция: ранг клиента по общей выручке
SELECT DISTINCT clientid, client_name, gender,
       SUM(revenue) OVER (PARTITION BY clientid) AS total_client_revenue,
       RANK() OVER (ORDER BY SUM(revenue) OVER (PARTITION BY clientid) DESC) AS revenue_rank
FROM course_project.sales_extended;
