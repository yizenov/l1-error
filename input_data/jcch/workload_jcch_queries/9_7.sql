SELECT COUNT(*)
FROM part AS p,
	supplier AS s,
	lineitem AS l,
	partsupp AS ps,
	orders AS o,
	nation AS n
WHERE p.p_name like '%hiny mined gold%'

	AND s.s_suppkey = l.l_suppkey
	AND ps.ps_suppkey = l.l_suppkey
	AND ps.ps_partkey = l.l_partkey
	AND p.p_partkey = l.l_partkey
	AND o.o_orderkey = l.l_orderkey
	AND s.s_nationkey = n.n_nationkey;
