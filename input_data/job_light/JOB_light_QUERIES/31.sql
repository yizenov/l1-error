SELECT COUNT(*)
FROM title AS t,
	cast_info AS ci,
	movie_companies AS mc
WHERE t.production_year > 2005 and t.production_year < 2015
	AND ci.role_id = 2

	AND t.id = ci.movie_id
	AND t.id = mc.movie_id;
