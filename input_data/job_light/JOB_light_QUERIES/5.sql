SELECT COUNT(*)
FROM title AS t,
	movie_info_idx AS mi_idx,
	movie_companies AS mc
WHERE mi_idx.info_type_id = 113
	AND mc.company_type_id = 2
	AND t.production_year > 2005 and t.production_year < 2010

	AND t.id = mc.movie_id
	AND t.id = mi_idx.movie_id;
