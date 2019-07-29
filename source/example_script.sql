--
-- File generated with SQLiteStudio v3.2.1 on mié. jul. 24 12:36:29 2019
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

	-- ***  DROP y CREATE  ****
	-- Table: address
	DROP TABLE IF EXISTS address;
	CREATE TABLE address (id INTEGER PRIMARY KEY ASC, street_name varchar(250), street_number varchar(250), post_code varchar(250) NOT NULL, person_id INTEGER NOT NULL, FOREIGN KEY(person_id) REFERENCES person(id));

	-- Table: person
	DROP TABLE IF EXISTS person;
	CREATE TABLE person (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL);
  ---------------------------------------------------------------------------------------
	-- ***  INSERT  ****
	-- Table: address
	INSERT INTO address (id, street_name, street_number, post_code, person_id) VALUES (1, 'python road', '1', '00000', 1);
	INSERT INTO address (id, street_name, street_number, post_code, person_id) VALUES (2, 'blblblbl', '1', '2222', 2);
	INSERT INTO address (id, street_name, street_number, post_code, person_id) VALUES (6, 'pythoncentrallllll', '11', '1221', 14);
	INSERT INTO address (id, street_name, street_number, post_code, person_id) VALUES (12, 'blblblbl', '1', '2222', 2);
	INSERT INTO address (id, street_name, street_number, post_code, person_id) VALUES (22, 'blblblbl', '1', '2222', 2);

	-- Table: person
	INSERT INTO person (id, name) VALUES (1, 'pythoncentral');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
