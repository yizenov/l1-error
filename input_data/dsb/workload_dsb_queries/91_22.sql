SELECT COUNT(*)
FROM call_center AS cc,
   catalog_returns AS cr,
   date_dim AS d,
   customer AS c,
   customer_address AS ca,
   customer_demographics AS cd,
   household_demographics AS hd
WHERE d.d_year = 2002 and d.d_moy = 7
   AND ((cd.cd_marital_status = 'M' and cd.cd_education_status = 'Unknown') or (cd.cd_marital_status = 'W' and cd.cd_education_status = 'Advanced Degree'))
   AND hd.hd_buy_potential like '5001-10000%'
   AND ca.ca_gmt_offset = -7

   AND cr.cr_call_center_sk = cc.cc_call_center_sk
   AND cr.cr_returned_date_sk = d.d_date_sk
   AND cr.cr_returning_customer_sk = c.c_customer_sk
   AND cd.cd_demo_sk = c.c_current_cdemo_sk
   AND hd.hd_demo_sk = c.c_current_hdemo_sk
   AND ca.ca_address_sk = c.c_current_addr_sk;
