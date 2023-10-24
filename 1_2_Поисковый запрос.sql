SELECT customer_id,rental_id,staff_id,amount
FROM public.payment
WHERE amount < 2.0 AND staff_id = 1
ORDER BY rental_id ASC