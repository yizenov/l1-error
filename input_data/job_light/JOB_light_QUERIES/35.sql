SELECT COUNT(*)
FROM title AS t,
	cast_info AS ci,
	movie_companies AS mc
WHERE t.production_year > 1990

	AND t.id = mc.movie_id
	AND t.id = ci.movie_id;
