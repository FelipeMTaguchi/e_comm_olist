SELECT 
    
    strftime('%Y-%m', r.review_creation_date) AS date,
    
    
    ROUND(
        AVG((julianday(r.review_answer_timestamp) - julianday(r.review_creation_date)) * 24.0), 
        1
    ) AS response_time_hours

FROM order_reviews r
WHERE r.review_score <= 2
  AND r.review_creation_date IS NOT NULL
  AND r.review_answer_timestamp IS NOT NULL

GROUP BY strftime('%Y-%m', r.review_creation_date)
ORDER BY date ASC;