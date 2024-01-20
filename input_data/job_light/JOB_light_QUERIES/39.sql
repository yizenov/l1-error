SELECT COUNT(*)
FROM title AS t,
	movie_info AS mi,
	movie_info_idx AS mi_idx,
	movie_companies AS mc
WHERE t.kind_id = 1
	AND mc.company_type_id = 2
	AND mi_idx.info_type_id = 101
	AND mi.info_type_id = 16

	AND t.id = mi.movie_id
	AND t.id = mi_idx.movie_id
	AND t.id = mc.movie_id;
