SELECT COUNT(*)
FROM supplier AS s,
	lineitem AS l,
	orders AS o,
	nation AS n
WHERE o.o_orderstatus = 'F'
	AND l.l_receiptdate > l.l_commitdate
	AND n.n_name = 'CHINA'

	AND s.s_suppkey = l.l_suppkey
	AND o.o_orderkey = l.l_orderkey
	AND s.s_nationkey = n.n_nationkey;
