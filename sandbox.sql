SELECT 
    r.review_score AS nota,
    COUNT(o.order_id) AS total_pedidos,
    ROUND(AVG(julianday(o.order_estimated_delivery_date) - julianday(o.order_delivered_customer_date)), 2) AS media_dias_antecedencia
FROM orders o
LEFT JOIN order_reviews r 
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND r.review_score IS NOT NULL
GROUP BY r.review_score
ORDER BY r.review_score DESC;

SELECT 
    r.review_score AS nota,
    COUNT(o.order_id) AS total_pedidos_atrasados,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date)), 1) AS media_dias_de_atraso
FROM orders o
LEFT JOIN order_reviews r 
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date > o.order_estimated_delivery_date
  AND r.review_score IS NOT NULL
GROUP BY r.review_score
ORDER BY r.review_score DESC;

SELECT 
    r.review_score AS nota,
    COUNT(o.order_id) AS total_geral_pedidos,
    SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS total_pedidos_atrasados,
    ROUND(
        AVG(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1.0 ELSE 0.0 END) * 100, 
        2
    ) || '%' AS proporcao_de_atraso
FROM orders o
LEFT JOIN order_reviews r 
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND r.review_score IS NOT NULL
GROUP BY r.review_score
ORDER BY r.review_score DESC;
