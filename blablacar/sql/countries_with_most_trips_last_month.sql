       WITH 

            trips_per_country AS (
            -- Returns the number of trips published per departure country during the last completed month.
     SELECT cities.country_id AS departure_country,
            SUM(trips.trips_cnt) AS trips_cnt
       FROM datamart_trips_supply AS trips
      WHERE is_full_trip IS TRUE --This clause ensures we only count the same trip once
        AND _PARTITIONTIME BETWEEN DATE_SUB(DATE_TRUNC(current_date(), MONTH), INTERVAL 1 MONTH) AND DATE_SUB(DATE_TRUNC(current_date(), MONTH), INTERVAL 1 DAY) 
  LEFT JOIN dim_cities AS cities
         ON trips.departure_city_id = cities.city_id
   GROUP BY cities.country_id
            ),

            ranked_countries AS (
            -- Returns a rank of the country based on their number of trips descending.
     SELECT departure_country,
            trips_cnt,
            RANK() OVER (ORDER BY trips_cnt DESC) AS country_rank
            -- The main advantage of using a RANK function rather than a limit statement is to account for the situation in which two countries would have the same number of trips.
            -- The limit statement would only return one, but the rank will return all of them.
       FROM trips_per_country
            )

            -- Returns the country/countries with the most trips published
     SELECT departure_country,
            trips_cnt
       FROM ranked_countries
      WHERE country_rank = 1
