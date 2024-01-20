SELECT COUNT(*)
FROM customer AS c,
	orders AS o,
	lineitem AS l
WHERE l.l_quantity <= 696

	AND c.c_custkey = o.o_custkey
	AND o.o_orderkey = l.l_orderkey;