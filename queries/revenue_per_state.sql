-- TODO: This query will return a table with two columns; customer_state, and 
-- Revenue. The first one will have the letters that identify the top 10 states 
-- with most revenue and the second one the total revenue of each.
-- HINT: All orders should have a delivered status and the actual delivery date 
-- should be not null. 

WITH delivered_orders AS (
    SELECT 
        order_id,
        customer_id
    FROM olist_orders
    WHERE 
        order_status = 'delivered'
        AND order_delivered_customer_date IS NOT NULL
),
payments AS (
    SELECT 
        order_id,
        SUM(payment_value) AS revenue
    FROM olist_order_payments
    GROUP BY order_id
),
joined AS (
    SELECT
        c.customer_state,
        p.revenue
    FROM delivered_orders o
    JOIN olist_customers c ON o.customer_id = c.customer_id
    JOIN payments p ON o.order_id = p.order_id
)
SELECT
    customer_state,
    SUM(revenue) AS Revenue
FROM joined
GROUP BY customer_state
ORDER BY Revenue DESC
LIMIT 10;