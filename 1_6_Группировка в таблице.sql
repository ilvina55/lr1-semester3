SELECT 
	   customer.customer_id,
	   customer.first_name,
       customer.last_name,
	   COUNT(rental.rental_id) AS inventory_taken
FROM public.customer 
INNER JOIN public.rental AS rental
	ON customer.customer_id = rental.customer_id
GROUP BY customer.customer_id
ORDER BY COUNT(rental.rental_id)  DESC