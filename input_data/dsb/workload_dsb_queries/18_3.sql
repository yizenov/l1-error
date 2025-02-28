SELECT COUNT(*)
FROM catalog_sales AS cs,
   customer_demographics AS cd,
   customer AS c,
   customer_address AS ca,
   date_dim AS d,
   item AS i
WHERE cd.cd_gender = 'F' and cd.cd_education_status = '4 yr Degree' 
   AND ca.ca_state in ('MO', 'NE', 'SD')
   AND cs.cs_wholesale_cost between 25 and 30
   AND i.i_category = 'Children'

   AND cs.cs_sold_date_sk = d.d_date_sk
   AND cs.cs_item_sk = i.i_item_sk
   AND cs.cs_bill_cdemo_sk = cd.cd_demo_sk
   AND cs.cs_bill_customer_sk = c.c_customer_sk
   AND c.c_current_addr_sk = ca.ca_address_sk;
