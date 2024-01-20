SELECT COUNT(*)
FROM part AS p,
	supplier AS s,
	lineitem AS l,
	orders AS o,
	customer AS c,
	nation AS n1,
	nation AS n2,
	region AS r
WHERE o.o_orderdate between date '1994-01-01' and date '1998-01-01'
	AND r.r_name = 'MIDDLE EAST'

	AND p.p_partkey = l.l_partkey
	AND s.s_suppkey = l.l_suppkey
	AND l.l_orderkey = o.o_orderkey
	AND o.o_custkey = c.c_custkey
	AND c.c_nationkey = n1.n_nationkey
	AND n1.n_regionkey = r.r_regionkey
	AND s.s_nationkey = n2.n_nationkey;
