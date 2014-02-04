CREATE DATABASE osb;
CREATE USER 'dimas'@'localhost' IDENTIFIED BY 'dimas';
GRANT ALL ON osb.* TO 'dimas'@'localhost';
ALTER DATABASE osb CHARACTER SET utf8 COLLATE utf8_general_ci