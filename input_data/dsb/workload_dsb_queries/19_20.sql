SELECT COUNT(*)
FROM date_dim AS d,
   store_sales AS ss,
   item AS i,
   customer AS c,
   customer_address AS ca,
   store AS s
WHERE i.i_category = 'Books'
   AND d.d_year = 2000 and d.d_moy = 10
   AND ca.ca_state = 'NY'
   AND c.c_birth_month = 4
   AND ss.ss_wholesale_cost between 59 and 79

   AND d.d_date_sk = ss.ss_sold_date_sk
   AND ss.ss_item_sk = i.i_item_sk
   AND ss.ss_customer_sk = c.c_customer_sk
   AND c.c_current_addr_sk = ca.ca_address_sk
   AND ss.ss_store_sk = s.s_store_sk;
