CREATE TABLE IF NOT EXISTS accounts (
  id VARCHAR PRIMARY KEY,
  account_limit INT NULL,
  products JSON NULL
);

CREATE TABLE IF NOT EXISTS  customer (
  id VARCHAR PRIMARY KEY,
  username VARCHAR NULL,
  name VARCHAR NULL,
  address TEXT NULL,
  birthdate TIMESTAMP NULL,
  email VARCHAR NULL,
  active BOOLEAN NULL,
  tier_and_details JSON NULL
);


CREATE TABLE IF NOT EXISTS customersXaccount (
  id SERIAL PRIMARY KEY,
  customer_id VARCHAR NULL,
  account_id VARCHAR NULL,
  FOREIGN KEY (customer_id) REFERENCES customer(id),
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);


CREATE TABLE IF NOT EXISTS transactionsMetadata (
  id VARCHAR PRIMARY KEY,
  account_id VARCHAR NULL,
  transaction_count INT NULL,
  bucket_start_date TIMESTAMP NULL,
  bucket_end_date TIMESTAMP NULL,
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);


CREATE TABLE IF NOT EXISTS transactions (
  id SERIAL PRIMARY KEY,
  account_id VARCHAR NULL,
  date TIMESTAMP NULL,
  amount INT NULL,
  transaction_code VARCHAR NULL,
  symbol VARCHAR NULL,
  price FLOAT NULL,
  total FLOAT NULL,
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);
