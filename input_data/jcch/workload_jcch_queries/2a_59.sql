SELECT COUNT(*)
FROM part AS p,
   supplier AS s,
   partsupp AS ps,
   nation AS n,
   region AS r
WHERE p.p_size = 36 and p.p_type like '%ED GOLD'
   AND r.r_name = 'EUROPE'

   AND p.p_partkey = ps.ps_partkey
   AND s.s_suppkey = ps.ps_suppkey
   AND s.s_nationkey = n.n_nationkey
   AND n.n_regionkey = r.r_regionkey;
