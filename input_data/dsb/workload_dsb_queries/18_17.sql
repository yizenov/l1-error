SELECT COUNT(*)
FROM catalog_sales AS cs,
   customer_demographics AS cd,
   customer AS c,
   customer_address AS ca,
   date_dim AS d,
   item AS i
WHERE cd.cd_gender = 'F' and cd.cd_education_status = 'Unknown' 
   AND ca.ca_state in ('CA', 'KY', 'ME')
   AND cs.cs_wholesale_cost between 45 and 50
   AND i.i_category = 'Shoes'

   AND cs.cs_sold_date_sk = d.d_date_sk
   AND cs.cs_item_sk = i.i_item_sk
   AND cs.cs_bill_cdemo_sk = cd.cd_demo_sk
   AND cs.cs_bill_customer_sk = c.c_customer_sk
   AND c.c_current_addr_sk = ca.ca_address_sk;
