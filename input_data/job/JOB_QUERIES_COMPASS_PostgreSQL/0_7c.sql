SELECT COUNT(*)
FROM aka_name AS an,
    cast_info AS ci,
    info_type AS it,
    link_type AS lt,
    movie_link AS ml,
    name AS n,
    person_info AS pi,
    title AS t
WHERE an.name is not null and (an.name like '%a%' or an.name like '%A%')
    AND it.info = 'mini biography'
    AND lt.link in ('references', 'referenced in', 'features', 'featured in')
    AND n.name_pcode_cf between 'A' and 'F' and (n.gender = 'm' or (n.gender = 'f' and n.name like '%A%'))
    AND pi.note is not null
    AND t.production_year between 1980 and 2010

    AND n.id = an.person_id
    AND n.id = pi.person_id
    AND ci.person_id = n.id
    AND t.id = ci.movie_id
    AND ml.linked_movie_id = t.id
    AND lt.id = ml.link_type_id
    AND it.id = pi.info_type_id
    AND pi.person_id = an.person_id
    AND pi.person_id = ci.person_id
    AND an.person_id = ci.person_id
    AND ci.movie_id = ml.linked_movie_id;
