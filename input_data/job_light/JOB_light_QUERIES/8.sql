SELECT COUNT(*)
FROM title AS t,
	movie_info_idx AS mi_idx,
	movie_keyword AS mk
WHERE t.production_year > 2005
	AND mi_idx.info_type_id = 101

	AND t.id = mi_idx.movie_id
	AND t.id = mk.movie_id;
