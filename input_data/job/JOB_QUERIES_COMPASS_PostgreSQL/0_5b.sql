SELECT COUNT(*)
FROM company_type AS ct,
    info_type AS it,
    movie_companies AS mc,
    movie_info AS mi,
    title AS t
WHERE ct.kind = 'production companies'
    AND mc.note not like '%(VHS)%' and mc.note like '%(USA)%' and mc.note not like '%(1994)%'
    AND mi.info in ('USA', 'America')
    AND t.production_year > 2010

    AND t.id = mi.movie_id
    AND t.id = mc.movie_id
    AND mc.movie_id = mi.movie_id
    AND ct.id = mc.company_type_id
    AND it.id = mi.info_type_id;
