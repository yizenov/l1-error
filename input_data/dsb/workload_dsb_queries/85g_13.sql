SELECT COUNT(*)
FROM web_sales AS ws,
   web_returns AS wr,
   web_page AS wp,
   customer_demographics AS cd1,
   customer_demographics AS cd2,
   customer_address AS ca,
   date_dim AS d,
   reason AS r
WHERE d.d_year = 1999
   AND ca.ca_country = 'United States' and ca.ca_state in ('AR', 'CA', 'NC')
   AND cd1.cd_marital_status = 'M' and cd1.cd_education_status = '2 yr Degree'
   AND ws.ws_sales_price between 100.00 and 150.00 and ws.ws_net_profit between 50 and 250

   AND ws.ws_web_page_sk = wp.wp_web_page_sk
   AND ws.ws_item_sk = wr.wr_item_sk
   AND ws.ws_order_number = wr.wr_order_number
   AND ws.ws_sold_date_sk = d.d_date_sk
   AND cd1.cd_demo_sk = wr.wr_refunded_cdemo_sk
   AND cd2.cd_demo_sk = wr.wr_returning_cdemo_sk
   AND ca.ca_address_sk = wr.wr_refunded_addr_sk
   AND r.r_reason_sk = wr.wr_reason_sk
   AND cd1.cd_marital_status = cd2.cd_marital_status
   AND cd1.cd_education_status = cd2.cd_education_status;
