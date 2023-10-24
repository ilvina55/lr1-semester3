SELECT film.title, film.length,film.rental_rate 
FROM public.film AS film
INNER JOIN  public.film_category  AS film_category
	ON film.film_id = film_category.film_id
INNER JOIN public.category AS category
	ON film_category.category_id = category.category_id
WHERE  category.name = 'Horror'
ORDER BY film.release_year ASC