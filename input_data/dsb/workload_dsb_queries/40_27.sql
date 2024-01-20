SELECT COUNT(*)
FROM warehouse AS w,
   item AS i,
   date_dim AS d,
   catalog_sales AS cs,
   catalog_returns AS cr
WHERE d.d_date between (cast('1999-06-24' as date) - interval '30 day') and (cast('1999-06-24' as date) + interval '30 day') 
   AND i.i_category = 'Children' and i.i_manager_id between 33 and 72
   AND cs.cs_wholesale_cost between 35 and 54

   AND i.i_item_sk = cs.cs_item_sk
   AND cs.cs_warehouse_sk = w.w_warehouse_sk
   AND cs.cs_sold_date_sk = d.d_date_sk
   AND cs.cs_order_number = cr.cr_order_number
   AND cs.cs_item_sk = cr.cr_item_sk;
