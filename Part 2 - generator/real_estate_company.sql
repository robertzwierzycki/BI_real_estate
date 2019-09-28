
USE real;

DROP TABLE IF EXISTS under_contract;
DROP TABLE IF EXISTS contract_invoice;
DROP TABLE IF EXISTS contract;
DROP TABLE IF EXISTS payment_frequency;
DROP TABLE IF EXISTS in_charge;
DROP TABLE IF EXISTS estate;
DROP TABLE IF EXISTS estate_type;
DROP TABLE IF EXISTS estate_status;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS contract_type;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS country;

CREATE TABLE country (
    id int PRIMARY KEY,
    country_name varchar(128)  NOT NULL,
);

CREATE TABLE city (
    id int PRIMARY KEY,
    city_name varchar(128)  NOT NULL,
    country_id int FOREIGN KEY REFERENCES country
);

CREATE TABLE client (
    id int PRIMARY KEY,
    client_name varchar(255)  NOT NULL,
    client_address varchar(255)  NOT NULL,
    contact_person varchar(255)  NULL,
    phone varchar(64)  NULL,
    mobile varchar(64)  NULL,
    mail varchar(64)  NULL,
    client_details text  NULL,
);

CREATE TABLE contract_type (
    id int PRIMARY KEY,
    contract_type_name varchar(64)  NOT NULL,
);

CREATE TABLE employee (
    id int  PRIMARY KEY,
    first_name varchar(64)  NOT NULL,
    last_name varchar(64)  NOT NULL,
);



CREATE TABLE estate_status (
    id int  PRIMARY KEY,
    estate_status_name varchar(64)  NOT NULL,
);

CREATE TABLE estate_type (
    id int  PRIMARY KEY,
    type_name varchar(128)  NOT NULL,
);

CREATE TABLE estate (
    id int  PRIMARY KEY,
    estate_name varchar(255)  NOT NULL,
    city_id int  FOREIGN KEY REFERENCES city,
    estate_type_id int  FOREIGN KEY REFERENCES estate_type,
    floor_space decimal(8,2)  NULL,
    number_of_balconies int  NULL,
    balconies_space decimal(8,2)  NULL,
    number_of_bedrooms int  NULL,
    number_of_bathrooms int  NULL,
    number_of_garages int  NULL,
    number_of_parking_spaces int  NULL,
    pets_allowed bit  NULL,
    estate_description text  NOT NULL,
    estate_status_id int FOREIGN KEY REFERENCES estate_status,
);

CREATE TABLE in_charge (
    id int PRIMARY KEY,
    estate_id int FOREIGN KEY REFERENCES estate,
    employee_id int  FOREIGN KEY REFERENCES employee,
    date_from date  NOT NULL,
    date_to date  NULL,
);

CREATE TABLE payment_frequency (
    id int PRIMARY KEY,
    payment_frequency_name varchar(64)  NOT NULL
);

CREATE TABLE contract (
    id int PRIMARY KEY,
    client_id int  FOREIGN KEY REFERENCES client,
    employee_id int FOREIGN KEY REFERENCES employee,
    contract_type_id int FOREIGN KEY REFERENCES contract_type,
    contract_details text  NOT NULL,
    payment_frequency_id int FOREIGN KEY REFERENCES payment_frequency,
    number_of_invoices int  NULL,
    payment_amount decimal(10,2)  NULL,
    fee_precentage decimal(5,2)  NOT NULL,
    fee_amount decimal(10,2)  NULL,
    date_signed date  NOT NULL,
    start_date date  NOT NULL,
    end_date date  NULL
);

CREATE TABLE contract_invoice (
    id int  PRIMARY KEY,
    contract_id int FOREIGN KEY REFERENCES contract,
    invoice_number varchar(64)  NOT NULL,
    invoice_details text  NOT NULL,
    invoice_amount decimal(10,2)  NOT NULL,
    date_created date  NOT NULL,
    date_paid date  NULL
);

CREATE TABLE under_contract (
    id int  NOT NULL,
    estate_id int FOREIGN KEY REFERENCES estate,
    contract_id int FOREIGN KEY REFERENCES contract
);
