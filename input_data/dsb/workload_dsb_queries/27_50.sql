SELECT COUNT(*)
FROM store_sales AS ss,
   customer_demographics AS cd,
   date_dim AS d,
   store AS s,
   item AS i
WHERE d.d_year = 2001
   AND cd.cd_gender = 'F' and cd.cd_marital_status = 'M' and cd.cd_education_status = '4 yr Degree'
   AND s.s_state = 'GA'
   AND i.i_category = 'Books'

   AND ss.ss_sold_date_sk = d.d_date_sk
   AND ss.ss_item_sk = i.i_item_sk
   AND ss.ss_store_sk = s.s_store_sk
   AND ss.ss_cdemo_sk = cd.cd_demo_sk;
