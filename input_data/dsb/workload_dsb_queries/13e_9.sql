SELECT COUNT(*)
FROM store_sales AS ss,
   store AS s,
   customer_demographics AS cd,
   household_demographics AS hd,
   customer_address AS ca,
   date_dim AS d
WHERE d.d_year = 2001
   AND ca.ca_country = 'United States' and ca.ca_state in ('MN', 'NE', 'WI')
   AND cd.cd_marital_status = 'S' and cd.cd_education_status = '4 yr Degree'
   AND ss.ss_sales_price between 50.00 and 100.00 and ss.ss_net_profit between 150 and 300
   AND hd.hd_dep_count = 1

   AND s.s_store_sk = ss.ss_store_sk
   AND ss.ss_sold_date_sk = d.d_date_sk 
   AND ss.ss_hdemo_sk = hd.hd_demo_sk
   AND cd.cd_demo_sk = ss.ss_cdemo_sk
   AND ss.ss_addr_sk = ca.ca_address_sk;
