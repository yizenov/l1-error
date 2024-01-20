SELECT COUNT(*)
FROM customer AS c,
	orders AS o,
	lineitem AS l,
	supplier AS s,
	nation AS n,
	region AS r
WHERE r.r_name = 'EUROPE'
	AND o.o_orderdate >= date '1994-01-01' and o.o_orderdate < date '1994-01-01' + interval '1' year
	AND l.l_returnflag = 'R'
	AND c.c_mktsegment = 'HOUSEHOLD'

	AND c.c_custkey = o.o_custkey
	AND l.l_orderkey = o.o_orderkey
	AND l.l_suppkey = s.s_suppkey
	AND c.c_nationkey = s.s_nationkey
	AND s.s_nationkey = n.n_nationkey
	AND n.n_regionkey = r.r_regionkey;
