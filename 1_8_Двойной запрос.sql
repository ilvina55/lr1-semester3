SELECT actor_id, first_name, last_name
FROM public.actor
WHERE actor_id IN (
	SELECT actor_id
	FROM public.film_actor
	WHERE film_id=4
)