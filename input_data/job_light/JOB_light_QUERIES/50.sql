SELECT COUNT(*)
FROM title AS t,
	movie_info AS mi,
	movie_keyword AS mk,
	movie_companies AS mc
WHERE mk.keyword_id = 398
	AND mc.company_type_id = 2
	AND t.production_year > 2000 and t.production_year < 2010

	AND t.id = mk.movie_id
	AND t.id = mc.movie_id
	AND t.id = mi.movie_id;
