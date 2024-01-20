SELECT COUNT(*)
FROM item AS item1,
   item AS item2,
   store_sales AS s1,
   store_sales AS s2,
   date_dim AS d,
   customer AS c,
   customer_address AS ca,
   customer_demographics AS cd
WHERE d.d_year between 2000 and 2000 + 1
   AND item1.i_category in ('Books', 'Home')
   AND item2.i_manager_id between 16 and 35
   AND cd.cd_marital_status = 'W' and cd.cd_education_status = 'Secondary'
   AND s1.ss_list_price between 184 and 198
   AND s2.ss_list_price between 184 and 198

   AND s1.ss_ticket_number = s2.ss_ticket_number
   AND s1.ss_item_sk = item1.i_item_sk
   AND s2.ss_item_sk = item2.i_item_sk
   AND s1.ss_customer_sk = c.c_customer_sk
   AND c.c_current_addr_sk = ca.ca_address_sk
   AND c.c_current_cdemo_sk = cd.cd_demo_sk
   AND d.d_date_sk = s1.ss_sold_date_sk;
