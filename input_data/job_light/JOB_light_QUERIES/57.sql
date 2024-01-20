SELECT COUNT(*)
FROM title AS t,
	movie_info_idx AS mi_idx,
	movie_keyword AS mk,
	cast_info AS ci
WHERE t.production_year > 2000 and t.kind_id = 1
	AND mi_idx.info_type_id = 101

	AND t.id = mk.movie_id
	AND t.id = ci.movie_id
	AND t.id = mi_idx.movie_id;
