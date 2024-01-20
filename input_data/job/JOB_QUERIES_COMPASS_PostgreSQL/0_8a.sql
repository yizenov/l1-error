SELECT COUNT(*)
FROM aka_name AS an,
    cast_info AS ci,
    company_name AS cn,
    movie_companies AS mc,
    name AS n,
    role_type AS rt,
    title AS t
WHERE ci.note = '(voice: English version)'
    AND cn.country_code = '[jp]'
    AND mc.note like '%(Japan)%' and mc.note not like '%(USA)%'
    AND n.name like '%Yo%' and n.name not like '%Yu%'
    AND rt.role_t = 'actress'

    AND an.person_id = n.id
    AND n.id = ci.person_id
    AND ci.movie_id = t.id
    AND t.id = mc.movie_id
    AND mc.company_id = cn.id
    AND ci.role_id = rt.id
    AND an.person_id = ci.person_id
    AND ci.movie_id = mc.movie_id;
