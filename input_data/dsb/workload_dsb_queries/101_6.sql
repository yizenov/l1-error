SELECT COUNT(*)
FROM store_sales AS ss,
   store_returns AS sr,
   web_sales AS ws,
   date_dim AS d1,
   date_dim AS d2,
   item AS i,
   customer AS c,
   customer_address AS ca,
   household_demographics AS hd
WHERE i.i_category in ('Books', 'Children', 'Jewelry')
   AND ca.ca_state in ('FL', 'IA', 'SC', 'VA', 'WI')
   AND hd.hd_buy_potential = '5001-10000' and hd.hd_income_band_sk between 11 and 17

   AND ss.ss_ticket_number = sr.sr_ticket_number
   AND ss.ss_customer_sk = ws.ws_bill_customer_sk
   AND ss.ss_customer_sk = c.c_customer_sk
   AND c.c_current_addr_sk = ca.ca_address_sk
   AND c.c_current_hdemo_sk = hd.hd_demo_sk
   AND ss.ss_item_sk = sr.sr_item_sk
   AND sr.sr_item_sk = ws.ws_item_sk
   AND i.i_item_sk = ss.ss_item_sk
   AND sr.sr_returned_date_sk = d1.d_date_sk
   AND ws.ws_sold_date_sk = d2.d_date_sk;
