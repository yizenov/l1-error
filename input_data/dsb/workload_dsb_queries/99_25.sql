SELECT COUNT(*)
FROM catalog_sales AS cs,
   warehouse AS w,
   ship_mode AS sm,
   call_center AS cc,
   date_dim AS d
WHERE d.d_month_seq between 1200 and 1200 + 23
   AND cs.cs_list_price between 261 and 290
   AND sm.sm_type = 'NEXT DAY'
   AND cc.cc_class = 'medium'
   AND w.w_gmt_offset = -5

   AND cs.cs_ship_date_sk = d.d_date_sk
   AND cs.cs_warehouse_sk = w.w_warehouse_sk
   AND cs.cs_ship_mode_sk = sm.sm_ship_mode_sk
   AND cs.cs_call_center_sk = cc.cc_call_center_sk;
