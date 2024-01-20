SELECT COUNT(*)
FROM customer AS c,
	orders AS o,
	lineitem AS l,
	nation AS n
WHERE o.o_orderdate >= date '1992-05-17' and o.o_orderdate < date '1992-05-29'
	AND l.l_returnflag = 'R'

	AND c.c_custkey = o.o_custkey
	AND l.l_orderkey = o.o_orderkey
	AND c.c_nationkey = n.n_nationkey;
