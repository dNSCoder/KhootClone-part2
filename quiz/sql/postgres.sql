CREATE DATABASE quizdb;
CREATE USER quizdbuser WITH PASSWORD '1234';
ALTER ROLE quizdbuser SET client_encoding TO 'utf8';
ALTER ROLE quizdbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE quizdbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE quizdb TO quizdbuser;
GRANT usage ON schema public TO quizdbuser;
GRANT create ON schema public TO quizdbuser;
