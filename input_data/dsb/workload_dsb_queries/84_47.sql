SELECT COUNT(*)
FROM customer AS c,
   customer_address AS ca,
   customer_demographics AS cd,
   household_demographics AS hd,
   income_band AS ib,
   store_returns AS sr
WHERE ca.ca_city = 'Friendship'
   AND ib.ib_lower_bound >= 5 * 10000 and ib.ib_upper_bound <= 5 * 10000 + 50000

   AND c.c_current_addr_sk = ca.ca_address_sk
   AND ib.ib_income_band_sk = hd.hd_income_band_sk
   AND cd.cd_demo_sk = c.c_current_cdemo_sk
   AND hd.hd_demo_sk = c.c_current_hdemo_sk
   AND sr.sr_cdemo_sk = cd.cd_demo_sk;
