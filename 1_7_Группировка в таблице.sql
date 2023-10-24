SELECT 
	   customer.customer_id,
	   customer.first_name,
       customer.last_name,
	   COUNT(rental.rental_id) AS inventory_taken
FROM public.customer AS customer
INNER JOIN public.rental AS rental
	ON customer.customer_id = rental.customer_id
WHERE customer.store_id = 2
GROUP BY customer.customer_id
HAVING COUNT (rental.rental_id) <=20

ORDER BY COUNT(rental.rental_id)  DESC