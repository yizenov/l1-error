SELECT COUNT(*)
FROM part AS p,
   supplier AS s,
   partsupp AS ps,
   nation AS n,
   region AS r
WHERE p.p_size = 49 and p.p_type like '%INED GOLD'
   AND r.r_name = 'MIDDLE EAST'

   AND p.p_partkey = ps.ps_partkey
   AND s.s_suppkey = ps.ps_suppkey
   AND s.s_nationkey = n.n_nationkey
   AND n.n_regionkey = r.r_regionkey;
