SELECT COUNT(*)
FROM catalog_sales AS cs,
   warehouse AS w,
   ship_mode AS sm,
   call_center AS cc,
   date_dim AS d
WHERE d.d_month_seq between 1180 and 1180 + 23
   AND cs.cs_list_price between 128 and 157
   AND sm.sm_type = 'REGULAR'
   AND cc.cc_class = 'large'
   AND w.w_gmt_offset = -5

   AND cs.cs_ship_date_sk = d.d_date_sk
   AND cs.cs_warehouse_sk = w.w_warehouse_sk
   AND cs.cs_ship_mode_sk = sm.sm_ship_mode_sk
   AND cs.cs_call_center_sk = cc.cc_call_center_sk;
