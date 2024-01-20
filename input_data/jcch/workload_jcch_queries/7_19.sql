SELECT COUNT(*)
FROM supplier AS s,
	lineitem AS l,
	orders AS o,
	customer AS c,
	nation AS n1,
	nation AS n2
WHERE l.l_shipdate between date '1993-01-01' and date '1998-01-01'
	AND n1.n_name = 'GERMANY'

	AND s.s_suppkey = l.l_suppkey
	AND o.o_orderkey = l.l_orderkey
	AND c.c_custkey = o.o_custkey
	AND s.s_nationkey = n1.n_nationkey
	AND c.c_nationkey = n2.n_nationkey;
