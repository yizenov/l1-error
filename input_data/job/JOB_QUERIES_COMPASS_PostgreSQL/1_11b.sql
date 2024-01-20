SELECT COUNT(*)
FROM company_name AS cn,
    company_type AS ct,
    keyword AS k,
    link_type AS lt,
    movie_companies AS mc,
    movie_keyword AS mk,
    movie_link AS ml,
    title AS t
WHERE cn.country_code not in ('[pl]') and (cn.name like '%Film%' or cn.name like '%Warner%')
    AND ct.kind = 'production companies'
    AND k.keyword = 'sequel'
    AND lt.link like '%follows%'
    AND mc.note is null
    AND t.production_year = 1998 and t.title like '%Money%'

    AND lt.id = ml.link_type_id
    AND ml.movie_id = t.id
    AND t.id = mk.movie_id
    AND mk.keyword_id = k.id
    AND t.id = mc.movie_id
    AND mc.company_type_id = ct.id
    AND mc.company_id = cn.id
    AND ml.movie_id = mk.movie_id
    AND ml.movie_id = mc.movie_id
    AND mk.movie_id = mc.movie_id;
