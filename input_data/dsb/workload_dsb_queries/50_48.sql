SELECT COUNT(*)
FROM store_sales AS ss,
   store_returns AS sr,
   store AS s,
   date_dim AS d1,
   date_dim AS d2
WHERE d2.d_moy = 4
   AND d1.d_dow = 3
   AND s.s_state in ('GA', 'IN', 'TN')

   AND ss.ss_ticket_number = sr.sr_ticket_number
   AND ss.ss_item_sk = sr.sr_item_sk
   AND ss.ss_sold_date_sk = d1.d_date_sk
   AND sr.sr_returned_date_sk = d2.d_date_sk
   AND ss.ss_customer_sk = sr.sr_customer_sk
   AND ss.ss_store_sk = s.s_store_sk
   AND sr.sr_store_sk = s.s_store_sk;
