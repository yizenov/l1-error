SELECT COUNT(*)
FROM title AS t,
	movie_keyword AS mk,
	movie_companies AS mc
WHERE mk.keyword_id = 398
	AND mc.company_type_id = 2

	AND t.id = mk.movie_id
	AND t.id = mc.movie_id;
