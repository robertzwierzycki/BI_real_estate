USE real;

BULK INSERT dbo.country FROM 'D:\DATA_T1_\country.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.city FROM 'D:\DATA_T1_\city.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.client FROM 'D:\DATA_T1_\client.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.contract_type FROM 'D:\DATA_T1_\contract_type.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.employee FROM 'D:\DATA_T1_\employee.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.estate_status FROM 'D:\DATA_T1_\estate_status.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.estate_type FROM 'D:\DATA_T1_\estate_type.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.estate FROM 'D:\DATA_T1_\estate.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.in_charge FROM 'D:\DATA_T1_\in_charge.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.payment_frequency FROM 'D:\DATA_T1_\payment_frequency.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.contract FROM 'D:\DATA_T1_\contract.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.contract_invoice FROM 'D:\DATA_T1_\contract_invoice.bulk' WITH (FIELDTERMINATOR=',');
BULK INSERT dbo.under_contract FROM 'D:\DATA_T1_\under_contract.bulk' WITH (FIELDTERMINATOR=',');
