SELECT COUNT(*)
FROM complete_cast AS cc,
    comp_cast_type AS cct,
    company_name AS cn,
    company_type AS ct,
    info_type AS it,
    keyword AS k,
    kind_type AS kt,
    movie_companies AS mc,
    movie_info AS mi,
    movie_keyword AS mk,
    title AS t
WHERE cct.kind = 'complete+verified'
    AND cn.country_code = '[us]'
    AND it.info = 'release dates'
    AND k.keyword in ('nerd', 'loner', 'alienation', 'dignity')
    AND kt.kind in ('movie')
    AND mi.note like '%internet%' and mi.info like 'USA:% 200%'
    AND t.production_year > 2000

    AND kt.id = t.kind_id
    AND t.id = mi.movie_id
    AND t.id = mk.movie_id
    AND t.id = mc.movie_id
    AND t.id = cc.movie_id
    AND mk.movie_id = mi.movie_id
    AND mk.movie_id = mc.movie_id
    AND mk.movie_id = cc.movie_id
    AND mi.movie_id = mc.movie_id
    AND mi.movie_id = cc.movie_id
    AND mc.movie_id = cc.movie_id
    AND k.id = mk.keyword_id
    AND it.id = mi.info_type_id
    AND cn.id = mc.company_id
    AND ct.id = mc.company_type_id
    AND cct.id = cc.status_id;
