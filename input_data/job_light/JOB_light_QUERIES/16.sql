SELECT COUNT(*)
FROM title AS t,
	movie_info AS mi,
	movie_companies AS mc
WHERE t.production_year > 1990
	AND mc.company_type_id = 2

	AND t.id = mi.movie_id
	AND t.id = mc.movie_id;
