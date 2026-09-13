SELECT 
    strftime('%Y-%m', o.order_delivered_customer_date) AS date,
    
    ROUND(AVG(r.review_score), 2) AS satisfaction,
    
    ROUND(
        AVG(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1.0 ELSE 0.0 END) * 100, 
        1
    ) AS delivery_time

FROM orders o
LEFT JOIN order_reviews r 
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND r.review_score IS NOT NULL

GROUP BY strftime('%Y-%m', o.order_delivered_customer_date)
ORDER BY date ASC;
