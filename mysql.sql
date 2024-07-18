-- mysql.sql
CREATE DATABASE khootdb CHARACTER SET utf8;
CREATE USER 'khootdbuser'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON khootdb.* TO 'khootdbuser'@'localhost';
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
-- SET GLOBAL time_zone = 'UTC';
FLUSH PRIVILEGES;