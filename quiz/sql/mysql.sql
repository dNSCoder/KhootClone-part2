CREATE DATABASE quizdb CHARACTER SET utf8;
CREATE USER 'quizdbuser'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON quizdb.* TO 'quizdbuser'@'localhost';
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
SET GLOBAL time zone 'Asia/Bangkok';
FLUSH PRIVILEGES;
