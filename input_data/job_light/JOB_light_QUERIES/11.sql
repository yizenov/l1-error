SELECT COUNT(*)
FROM title AS t,
	movie_info AS mi,
	movie_keyword AS mk
WHERE t.production_year > 2005

	AND t.id = mi.movie_id
	AND t.id = mk.movie_id;
