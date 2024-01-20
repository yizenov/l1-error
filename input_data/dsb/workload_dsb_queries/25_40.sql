SELECT COUNT(*)
FROM store_sales AS ss,
   store_returns AS sr,
   catalog_sales AS cs,
   date_dim AS d1,
   date_dim AS d2,
   date_dim AS d3,
   store AS s,
   item AS i
WHERE d1.d_moy = 2 and d1.d_year = 1999
   AND d2.d_year = 1999 and d2.d_moy between 2 and 2 + 2
   AND d3.d_year = 1999 and d3.d_moy between 2 and 2 + 2

   AND d1.d_date_sk = ss.ss_sold_date_sk
   AND i.i_item_sk = ss.ss_item_sk
   AND s.s_store_sk = ss.ss_store_sk
   AND ss.ss_customer_sk = sr.sr_customer_sk
   AND ss.ss_item_sk = sr.sr_item_sk
   AND ss.ss_ticket_number = sr.sr_ticket_number
   AND sr.sr_returned_date_sk = d2.d_date_sk
   AND sr.sr_customer_sk = cs.cs_bill_customer_sk
   AND sr.sr_item_sk = cs.cs_item_sk
   AND cs.cs_sold_date_sk = d3.d_date_sk;
