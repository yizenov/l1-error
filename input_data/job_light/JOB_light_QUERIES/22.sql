SELECT COUNT(*)
FROM title AS t,
	movie_keyword AS mk,
	cast_info AS ci
WHERE t.production_year > 1950 and t.kind_id = 1

	AND t.id = mk.movie_id
	AND t.id = ci.movie_id;
