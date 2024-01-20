SELECT COUNT(*)
FROM customer AS c,
	orders AS o,
	lineitem AS l
WHERE c.c_mktsegment = 'AUTOMOBILE'
	AND o.o_orderdate < date '1995-03-26'
	AND l.l_shipdate > date '1995-03-26'

	AND c.c_custkey = o.o_custkey
	AND l.l_orderkey = o.o_orderkey;
