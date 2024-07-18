-- postgres.sql
CREATE DATABASE khootdb;
CREATE USER khootdbuser WITH PASSWORD '1234';
ALTER ROLE khootdbuser SET client_encoding TO 'utf8';
ALTER ROLE khootdbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE khootdbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE khootdb TO khootdbuser;
GRANT usage ON schema public TO khootdbuser;
GRANT create ON schema public TO khootdbuser;