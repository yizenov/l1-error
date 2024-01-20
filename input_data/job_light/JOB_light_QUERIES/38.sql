SELECT COUNT(*)
FROM title AS t,
	movie_info AS mi,
	movie_info_idx AS mi_idx,
	movie_companies AS mc
WHERE mi_idx.info_type_id = 101
	AND mi.info_type_id = 3
	AND t.production_year > 2000 and t.production_year < 2010
	AND mc.company_type_id = 2

	AND t.id = mi.movie_id
	AND t.id = mi_idx.movie_id
	AND t.id = mc.movie_id;
