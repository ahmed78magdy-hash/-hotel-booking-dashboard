CREATE DATABASE hotel_booking;
USE hotel_booking;
SHOW TABLES;
SHOW TABLES;
DESCRIBE hotel_booking;
SELECT COUNT(*) FROM hotel_booking;
TRUNCATE TABLE hotel_booking;
LOAD DATA LOCAL INFILE 'D:/Final Project data/Hotel Booking/hotel_booking.csv'
INTO TABLE hotel_booking
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
SELECT COUNT(*) FROM hotel_booking;
SELECT * FROM hotel_booking 
WHERE children IS NULL 
LIMIT 10;
SELECT children, COUNT(*) 
FROM hotel_booking 
GROUP BY children 
ORDER BY children;
SELECT
  SUM(hotel IS NULL) AS hotel_nulls,
  SUM(is_canceled IS NULL) AS is_canceled_nulls,
  SUM(lead_time IS NULL) AS lead_time_nulls,
  SUM(arrival_date_year IS NULL) AS arrival_year_nulls,
  SUM(arrival_date_month IS NULL) AS arrival_month_nulls,
  SUM(country IS NULL) AS country_nulls,
  SUM(market_segment IS NULL) AS market_segment_nulls,
  SUM(distribution_channel IS NULL) AS distribution_channel_nulls,
  SUM(reserved_room_type IS NULL) AS reserved_room_nulls,
  SUM(assigned_room_type IS NULL) AS assigned_room_nulls,
  SUM(deposit_type IS NULL) AS deposit_type_nulls,
  SUM(agent IS NULL) AS agent_nulls,
  SUM(company IS NULL) AS company_nulls,
  SUM(customer_type IS NULL) AS customer_type_nulls,
  SUM(adr IS NULL) AS adr_nulls,
  SUM(reservation_status IS NULL) AS reservation_status_nulls,
  SUM(reservation_status_date IS NULL) AS reservation_status_date_nulls,
  SUM(name IS NULL) AS name_nulls,
  SUM(email IS NULL) AS email_nulls,
  SUM(`phone-number` IS NULL) AS phone_nulls,
  SUM(credit_card IS NULL) AS credit_card_nulls
FROM hotel_booking;
SELECT
  SUM(agent = '') AS agent_blanks,
  SUM(company = '') AS company_blanks,
  SUM(country = '') AS country_blanks,
  SUM(email = '') AS email_blanks,
  SUM(`phone-number` = '') AS phone_blanks,
  SUM(credit_card = '') AS credit_card_blanks
FROM hotel_booking;
SELECT hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_day_of_month, adults, children, babies, email, COUNT(*) AS cnt
FROM hotel_booking
GROUP BY hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_day_of_month, adults, children, babies, email
HAVING COUNT(*) > 1
ORDER BY cnt DESC
LIMIT 20;
SELECT * FROM hotel_booking
WHERE email = 'Lisa_M@gmail.com' AND lead_time = 283 AND arrival_date_year = 2015 AND arrival_date_month = 'July';
SELECT COUNT(*) AS total_duplicate_rows
FROM (
  SELECT hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_day_of_month, adults, children, babies, email
  FROM hotel_booking
  GROUP BY hotel, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_day_of_month, adults, children, babies, email
  HAVING COUNT(*) > 1
) AS dupes;
ALTER TABLE hotel_booking ADD COLUMN row_id INT AUTO_INCREMENT PRIMARY KEY;
SELECT row_id, hotel, is_canceled, lead_time, email
FROM hotel_booking
WHERE email = 'Lisa_M@gmail.com' AND lead_time = 283 AND arrival_date_year = 2015 AND arrival_date_month = 'July';
DELETE FROM hotel_booking WHERE row_id = 36645;
SELECT COUNT(*) FROM hotel_booking;
SELECT
  SUM(adults = 0 AND children = 0 AND babies = 0) AS zero_guest_bookings,
  SUM(adr < 0) AS negative_price_bookings,
  SUM(adr = 0) AS zero_price_bookings,
  SUM(stays_in_weekend_nights = 0 AND stays_in_week_nights = 0) AS zero_night_stays,
  MAX(adr) AS max_price,
  MAX(lead_time) AS max_lead_time
FROM hotel_booking;
SELECT row_id, hotel, adr, reservation_status, email FROM hotel_booking WHERE adr < 0;
DELETE FROM hotel_booking WHERE row_id = 55512;
SELECT COUNT(*) FROM hotel_booking;
SELECT row_id, hotel, is_canceled, adults, children, babies, adr, reservation_status
FROM hotel_booking
WHERE adults = 0 AND children = 0 AND babies = 0
LIMIT 15;
DELETE FROM hotel_booking WHERE adults = 0 AND children = 0 AND babies = 0;
DELETE FROM hotel_booking WHERE adults = 0 AND children = 0 AND babies = 0;
DELETE FROM hotel_booking 
WHERE row_id IN (
  SELECT row_id FROM (
    SELECT row_id FROM hotel_booking WHERE adults = 0 AND children = 0 AND babies = 0
  ) AS temp
);
SELECT COUNT(*) FROM hotel_booking;
SELECT is_canceled, COUNT(*) 
FROM hotel_booking 
WHERE adr = 0 
GROUP BY is_canceled;
SELECT is_canceled, reservation_status, COUNT(*) 
FROM hotel_booking 
WHERE stays_in_weekend_nights = 0 AND stays_in_week_nights = 0
GROUP BY is_canceled, reservation_status;
DELETE FROM hotel_booking 
WHERE stays_in_weekend_nights = 0 
AND stays_in_week_nights = 0 
AND reservation_status = 'Check-Out';
SELECT COUNT(*) FROM hotel_booking;
SELECT row_id, hotel, adr, lead_time, reservation_status
FROM hotel_booking
WHERE adr > 1000 OR lead_time > 500
ORDER BY adr DESC
LIMIT 20;
DELETE FROM hotel_booking WHERE row_id = 82199;
SELECT COUNT(*) FROM hotel_booking;
SELECT country, COUNT(*) 
FROM hotel_booking 
WHERE country != TRIM(country) 
GROUP BY country;
SELECT 
  SUM(hotel != TRIM(hotel)) AS hotel_spaces,
  SUM(meal != TRIM(meal)) AS meal_spaces,
  SUM(market_segment != TRIM(market_segment)) AS market_segment_spaces,
  SUM(distribution_channel != TRIM(distribution_channel)) AS distribution_channel_spaces,
  SUM(reserved_room_type != TRIM(reserved_room_type)) AS reserved_room_spaces,
  SUM(deposit_type != TRIM(deposit_type)) AS deposit_type_spaces,
  SUM(customer_type != TRIM(customer_type)) AS customer_type_spaces,
  SUM(reservation_status != TRIM(reservation_status)) AS reservation_status_spaces
FROM hotel_booking;
SELECT COUNT(DISTINCT country) AS distinct_raw, COUNT(DISTINCT UPPER(country)) AS distinct_upper
FROM hotel_booking;
SELECT 
  COUNT(DISTINCT hotel) AS hotel_raw, COUNT(DISTINCT UPPER(hotel)) AS hotel_upper,
  COUNT(DISTINCT meal) AS meal_raw, COUNT(DISTINCT UPPER(meal)) AS meal_upper,
  COUNT(DISTINCT market_segment) AS market_raw, COUNT(DISTINCT UPPER(market_segment)) AS market_upper,
  COUNT(DISTINCT distribution_channel) AS dist_raw, COUNT(DISTINCT UPPER(distribution_channel)) AS dist_upper,
  COUNT(DISTINCT deposit_type) AS deposit_raw, COUNT(DISTINCT UPPER(deposit_type)) AS deposit_upper,
  COUNT(DISTINCT customer_type) AS customer_raw, COUNT(DISTINCT UPPER(customer_type)) AS customer_upper
FROM hotel_booking;
SELECT 
  SUM(agent = 'NULL') AS agent_literal_null,
  SUM(company = 'NULL') AS company_literal_null,
  SUM(country = 'NULL') AS country_literal_null
FROM hotel_booking;