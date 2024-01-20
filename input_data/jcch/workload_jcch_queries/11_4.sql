SELECT COUNT(*)
FROM partsupp AS ps,
	supplier AS s,
	nation AS n
WHERE n.n_name = 'EGYPT'

	AND ps.ps_suppkey = s.s_suppkey
	AND s.s_nationkey = n.n_nationkey;
