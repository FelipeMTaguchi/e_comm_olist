SELECT 
    c.customer_state AS state,
    ROUND(AVG(r.review_score), 2) AS satisfaction,
    ROUND(AVG(julianday(o.order_estimated_delivery_date) - julianday(o.order_delivered_customer_date)), 1) AS delivery_time,
    COUNT(o.order_id) AS total_orders
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items i ON o.order_id = i.order_id
INNER JOIN products p ON i.product_id = p.product_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND p.product_category_name = ? 
GROUP BY c.customer_state
ORDER BY total_orders DESC;
