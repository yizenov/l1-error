SELECT COUNT(*)
FROM title AS t,
	movie_keyword AS mk,
	movie_companies AS mc,
	cast_info AS ci
WHERE mk.keyword_id = 117

	AND t.id = ci.movie_id
	AND t.id = mk.movie_id
	AND t.id = mc.movie_id;
