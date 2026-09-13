SELECT 
    julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) AS delay_days,
    r.review_score AS satisfaction
FROM orders o
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND r.review_score IS NOT NULL;
