SELECT COUNT(*)
FROM title AS t,
	movie_keyword AS mk,
	movie_companies AS mc
WHERE mk.keyword_id = 117

	AND t.id = mc.movie_id
	AND t.id = mk.movie_id;
