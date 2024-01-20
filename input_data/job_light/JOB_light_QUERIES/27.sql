SELECT COUNT(*)
FROM title AS t,
	movie_keyword AS mk,
	movie_companies AS mc
WHERE t.production_year > 1950

	AND t.id = mk.movie_id
	AND t.id = mc.movie_id;
