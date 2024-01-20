SELECT COUNT(*)
FROM title AS t,
	movie_info AS mi,
	movie_info_idx AS mi_idx,
	movie_keyword AS mk,
	cast_info AS ci
WHERE mi.info_type_id = 3
	AND mi_idx.info_type_id = 100

	AND t.id = mi.movie_id
	AND t.id = mi_idx.movie_id
	AND t.id = ci.movie_id
	AND t.id = mk.movie_id;
