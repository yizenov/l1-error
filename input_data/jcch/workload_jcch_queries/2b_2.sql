SELECT COUNT(*)
FROM part AS p,
   supplier AS s,
   partsupp AS ps,
   nation AS n,
   region AS r
WHERE r.r_name = 'AMERICA'

   AND p.p_partkey = ps.ps_partkey
   AND s.s_suppkey = ps.ps_suppkey
   AND s.s_nationkey = n.n_nationkey
   AND n.n_regionkey = r.r_regionkey;
