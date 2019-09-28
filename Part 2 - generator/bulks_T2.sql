use real;

DELETE FROM under_contract;
DELETE FROM contract_invoice;
DELETE FROM contract;
DELETE FROM payment_frequency;
DELETE FROM in_charge;
DELETE FROM estate;
DELETE FROM estate_type;
DELETE FROM estate_status;
DELETE FROM employee;
DELETE FROM contract_type;
DELETE FROM client;
DELETE FROM city;
DELETE FROM country;

BULK INSERT dbo.country FROM 'D:\DATA_T2_\country.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.city FROM 'D:\DATA_T2_\city.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.client FROM 'D:\DATA_T2_\client.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.contract_type FROM 'D:\DATA_T2_\contract_type.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.employee FROM 'D:\DATA_T2_\employee.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.estate_status FROM 'D:\DATA_T2_\estate_status.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.estate_type FROM 'D:\DATA_T2_\estate_type.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.estate FROM 'D:\DATA_T2_\estate.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.in_charge FROM 'D:\DATA_T2_\in_charge.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.payment_frequency FROM 'D:\DATA_T2_\payment_frequency.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.contract FROM 'D:\DATA_T2_\contract.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.contract_invoice FROM 'D:\DATA_T2_\contract_invoice.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.under_contract FROM 'D:\DATA_T2_\under_contract.bulk' WITH (FIELDTERMINATOR=',');