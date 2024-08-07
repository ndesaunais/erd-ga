CREATE TABLE IF NOT EXISTS addresses (
  id SERIAL PRIMARY KEY,
  street TEXT,
  suburb TEXT,
  government_area TEXT,
  market TEXT,
  country TEXT,
  country_code TEXT,
  location JSON
);

CREATE TABLE IF NOT EXISTS hosts (
  id INT PRIMARY KEY,
  url TEXT,
  name TEXT,
  location TEXT,
  about TEXT,
  response_time TEXT NULL,
  thumbnail_url TEXT,
  picture_url TEXT,
  neighbourhood TEXT,
  response_rate INT NULL,
  is_superhost BOOLEAN,
  has_profile_pic BOOLEAN,
  identity_verified BOOLEAN,
  listings_count INT,
  total_listings_count INT,
  verifications JSON
);

CREATE TABLE IF NOT EXISTS listings (
  id VARCHAR PRIMARY KEY,
  listing_url TEXT,
  name TEXT,
  summary TEXT,
  space TEXT,
  description TEXT,
  neighborhood_overview TEXT NULL,
  notes TEXT NULL,
  transit TEXT NULL,
  access TEXT NULL,
  interaction TEXT NULL,
  house_rules TEXT NULL,
  property_type TEXT NULL,
  room_type TEXT NULL,
  bed_type TEXT NULL,
  minimum_nights TEXT NULL,
  maximum_nights TEXT NULL,
  cancellation_policy TEXT NULL,
  last_scraped TIMESTAMP NULL,
  calendar_last_scraped TIMESTAMP NULL,
  first_review TIMESTAMP NULL,
  last_review TIMESTAMP NULL,
  accommodates INT NULL,
  bedrooms INT NULL,
  beds INT NULL,
  number_of_reviews INT NULL,
  bathrooms FLOAT NULL,
  amenities JSON NULL,
  price FLOAT NULL,
  security_deposit FLOAT NULL,
  cleaning_fee FLOAT NULL,
  extra_people FLOAT NULL,
  guests_included FLOAT NULL,
  images JSON NULL,
  availability JSON NULL,
  review_scores JSON NULL,
  reviews_per_month INT NULL,
  address_id INT,
  host_id INT,
  weekly_price FLOAT NULL,
  monthly_price FLOAT NULL,
  FOREIGN KEY (address_id) REFERENCES addresses(id),
  FOREIGN KEY (host_id) REFERENCES hosts(id)
);


CREATE TABLE IF NOT EXISTS reviews (
  id VARCHAR PRIMARY KEY,
  date TIMESTAMP,
  listing_id VARCHAR,
  reviewer_id INT,
  reviewer_name TEXT,
  comments TEXT,
  FOREIGN KEY (listing_id) REFERENCES listings(id)
);
