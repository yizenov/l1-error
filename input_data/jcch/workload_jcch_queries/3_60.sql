SELECT COUNT(*)
FROM customer AS c,
	orders AS o,
	lineitem AS l
WHERE c.c_mktsegment = 'HOUSEHOLD'
	AND o.o_orderdate < date '1995-03-13'
	AND l.l_shipdate > date '1995-03-13'

	AND c.c_custkey = o.o_custkey
	AND l.l_orderkey = o.o_orderkey;
