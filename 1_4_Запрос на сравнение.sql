SELECT title,release_year,rating,length 
FROM public.film
WHERE description NOT LIKE '%Dentist%'
ORDER BY rating DESC