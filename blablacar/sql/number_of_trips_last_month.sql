    SELECT SUM(trips_cnt) as trips_cnt
      FROM datamart_trips_supply
     WHERE is_full_trip IS TRUE --This clause ensures we only count the full route
       AND _PARTITIONTIME BETWEEN DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 MONTH) AND DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 1 DAY) 
           -- This clause checks that the partition is between the first day and the last day of the last month.