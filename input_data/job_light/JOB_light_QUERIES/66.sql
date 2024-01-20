SELECT COUNT(*)
FROM title AS t,
	movie_info AS mi,
	movie_keyword AS mk,
	movie_companies AS mc,
	cast_info AS ci
WHERE ci.role_id = 2
	AND mi.info_type_id = 16
	AND t.production_year > 2010

	AND t.id = mi.movie_id
	AND t.id = mc.movie_id
	AND t.id = ci.movie_id
	AND t.id = mk.movie_id;
