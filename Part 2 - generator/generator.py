import pandas as pd
import numpy as np
from random import randint, getrandbits
import time


class ThingGenerator:
    def __init__(self, col_names):
        self._list = pd.DataFrame(columns=col_names)

    def get_list(self):
        return self._list

    def write_to_csv(self, file_name):
        print('Data saved to "' + file_name + '".')
        self._list.to_csv(file_name)

    def reset(self):
        if not self._list.empty:
            self._list = pd.DataFrame(columns=self._list.columns.values.tolist())


class PersonGenerator(ThingGenerator):
    """
        Generates a pandas DataFrame with n random names, surnames, and birthdays.
        Choice of names depends on selected birth year or age range.

        Attributes:
            __name_list (DataFrame): Contains entire names data set
            __surname_list (DataFrame): Contains entire surname data set
    """
    def __init__(self):
        super(PersonGenerator, self).__init__(
            col_names=['id', 'name', 'surname', 'dob']
        )
        self.__name_list = pd.read_csv("NationalNames.csv")
        print('Loaded ' + str(self.__name_list.shape[0]) + ' names.')
        self.__surname_list = pd.read_csv("Names_2010Census.csv")
        print('Loaded ' + str(self.__surname_list.shape[0]) + ' surnames.')

    def generate(self, n=1, year_of_birth=None, age_range=None):
        print('Generating ' + str(n) + ' people...')
        time_start = time.time()

        if year_of_birth is not None:
            valid_names = self.__name_list[self.__name_list.Year == year_of_birth]
            picked_names = valid_names.sample(n=n, replace=True)
        elif age_range is not None:
            valid_names = self.__name_list[(self.__name_list.Year >= 2019 - age_range[1]) &
                                           (self.__name_list.Year <= 2019 - age_range[0])]
            picked_names = valid_names.sample(n=n, replace=True)
        else:
            picked_names = self.__name_list.sample(n=n, replace=True)

        picked_surnames = self.__surname_list.sample(n=n, replace=True)

        picked_names = picked_names.reset_index(drop=True)
        picked_surnames = picked_surnames.reset_index(drop=True)

        print(self._list.shape)
        self._list['id'] = range(n)
        self._list['name'] = picked_names['Name']
        self._list['surname'] = picked_surnames['name']
        self._list['dob'] = ['{}-{:0>2d}-{:0>2d}'.format(year, randint(1, 12), randint(1, 28))
                             for year in picked_names['Year']]

        time_end = time.time()
        print('Done! Time taken: ' + str(time_end - time_start))
        return self._list


class AddressGenerator(ThingGenerator):
    """ Generates a pandas DataFrame with n randomly picked addresses from the OpenAddresses database

        Attributes:
            __address_list (DataFrame): Contains entire OpenAddresses Massachusetts database
    """
    def __init__(self):
        super(AddressGenerator, self).__init__(
            col_names=['id', 'number', 'street', 'unit', 'city', 'district', 'region', 'postcode']
        )
        self.__address_list = pd.read_csv("openaddr-collected-us-northeast/ma/statewide.csv",
                                          dtype={'NUMBER':np.str,'STREET':np.str,'CITY':np.str,'DISTRICT':np.str,'REGION':np.str,'POSTCODE':np.str})
        print('Loaded ' + str(self.__address_list.shape[0]) + ' addresses.')

    def generate(self, n=1):
        print('Generating ' + str(n) + ' addresses...')
        time_start = time.time()

        if n > self.__address_list.shape[0]:
            print('WARNING: Picking addresses with replacement!')
            replace = True
        else:
            replace = False

        picked_addresses = self.__address_list.sample(n=n, replace=replace)
        picked_addresses = picked_addresses.reset_index(drop=True)

        self._list['id'] = range(n)
        self._list['number'] = picked_addresses['NUMBER']
        self._list['street'] = picked_addresses['STREET']
        self._list['unit'] = picked_addresses['UNIT']
        self._list['city'] = picked_addresses['CITY']
        self._list['district'] = picked_addresses['DISTRICT']
        self._list['region'] = picked_addresses['REGION']
        self._list['postcode'] = picked_addresses['POSTCODE']

        time_end = time.time()
        print('Done! Time taken: ' + str(time_end - time_start))
        return self._list


class ClientGenerator(ThingGenerator):
    """ Generates a pandas DataFrame with n randomly generated clients.
        Uses instances of PersonGenerator and AddressGenerator.

        Attributes:
            __person_generator (PersonGenerator): used to generate client_name
            __address_generator (DataFrame): used to generate client_address

        Args:
            person_generator (PersonGenerator)
            address_generator (AddressGenerator)
    """
    def __init__(self, person_generator, address_generator):
        super(ClientGenerator, self).__init__(
            col_names=['id', 'client_name', 'client_address', 'contact_person', 'phone',
                       'mobile', 'mail', 'client_details']
        )
        self.__person_generator = person_generator
        self.__address_generator = address_generator

    def generate(self, n=1):
        print('Generating ' + str(n) + ' clients...')
        time_start = time.time()

        generated_people = self.__person_generator.generate(n=n)
        generated_addresses = self.__address_generator.generate(n=n)

        self._list['id'] = range(0, n)
        self._list['client_name'] = generated_people['surname'].map(str) + ' ' + generated_people['name'].map(str)
        self._list['client_address'] = generated_addresses['number'] + ' ' + \
            generated_addresses['street'].str.title() + ' ' + generated_addresses['city'].str.title() + ', ' + \
            generated_addresses['region'] + ' ' + generated_addresses['postcode']
        # TODO: self._list['contact_person']
        self._list['phone'] = ['{:0>3d} {:0>3d} {:0>3d}'.format(randint(0, 999), randint(0, 999), randint(0, 999))
                               for i in range(n)]
        self._list['mobile'] = ['{:0>3d} {:0>3d} {:0>3d}'.format(randint(0, 999), randint(0, 999), randint(0, 999))
                                for i in range(n)]
        self._list['mail'] = generated_people['surname'].str.lower() + '.' + generated_people['name'].str.lower() + \
            '@gmail.com'
        # TODO: self._list['client_details']

        time_end = time.time()
        print('Done! Time taken: ' + str(time_end - time_start))
        return self._list

    def write_to_csv(self):
        print('Data saved to "generated_data/client.csv".')
        self._list.to_csv('generated_data/client.csv', columns=['client_name', 'client_address', 'contact_person', 'phone',
                       'mobile', 'mail', 'client_details'])


class EmployeeGenerator(ThingGenerator):
    """ Generates a pandas DataFrame with n randomly generated clients.
        Uses instances of PersonGenerator and AddressGenerator.

        Attributes:
            __person_generator (PersonGenerator): used to generate client_name
            __higher_position (list): positions occupied by employees with higher education
            __medium_position (list): positions occupied by employees with medium education
        Args:
            person_generator (PersonGenerator)
    """
    def __init__(self, person_generator):
        super(EmployeeGenerator, self).__init__(
            col_names=['id', 'pin', 'name', 'surname', 'dob',
                       'education', 'position', 'date_of_acceptance', 'date_of_end']
        )
        self.__person_generator = person_generator
        self.__higher_position = ['financial director', 'operations director', 'marketing director', 'data scientist']
        self.__medium_position = ['real estate agent', 'technician', 'IT specialist', 'data scientist']

    def generate(self, n=1):
        print('Generating ' + str(n) + ' employees...')
        time_start = time.time()

        self.__person_generator.reset()
        generated_people = self.__person_generator.generate(n=n, age_range=(20, 45))

        self._list['id'] = range(0, n)
        self._list['pin'] = ['{:0>4d}'.format(randint(0, 9999)) for i in range(n)]
        self._list['name'] = generated_people['name']
        self._list['surname'] = generated_people['surname']
        self._list['dob'] = generated_people['dob']
        self._list['education'] = ['medium' if chance < 30 else 'higher' for chance in np.random.randint(0, 100, n)]
        self._list['position'] = [self.__medium_position[randint(0, len(self.__medium_position)-1)]
                                  if education == 'medium' else self.__higher_position[randint(0, len(self.__higher_position)-1)]
                                  for education in self._list['education']]
        self._list['date_of_acceptance'] = ['{}-{:0>2d}-{:0>2d}'.format(year + randint(18, 19), randint(1, 12), randint(1, 28))
                                            for year in generated_people['dob'].str.slice(0, 4).map(int)]
        self._list['date_of_end'] = [(None if year >= 2019 else
                                     '{}-{:0>2d}-{:0>2d}'.format(year, randint(1, 12), randint(1, 28)))
                                     for year in self._list['date_of_acceptance'].str.slice(0, 4).map(int) + np.random.randint(1, 10, n)]

        time_end = time.time()
        print('Done! Time taken: ' + str(time_end - time_start))
        return self._list

    def write_to_excel(self):
        print('Data saved to "generated_data/employee.xlsx".')
        self._list.to_excel('generated_data/employee.xlsx', columns=['pin', 'name', 'surname', 'dob',
                       'education', 'position', 'date_of_acceptance', 'date_of_end'])

    def write_to_csv(self):
        print('Data saved to "generated_data/employee.csv".')
        self._list.to_csv('generated_data/employee.csv', columns=['name', 'surname'])


class EstateInfoGenerator(ThingGenerator):
    def __init__(self, address_generator):
        super(EstateInfoGenerator, self).__init__(
            col_names=['id', 'estate_name', 'city_id', 'estate_type_id', 'floor_space',
                       'number_of_balconies', 'balconies_space', 'number_of_bedrooms',
                       'number_of_bathrooms', 'number_of_garages', 'number_of_parking_spaces',
                       'pets_allowed', 'estate_description', 'estate_status_id']
        )

        self.__estate_types = pd.DataFrame({'id': range(6),
                                            'type_name': ['fee simple absolute', 'life', 'tenancy for years',
                                                          'tenancy at will', 'joint tenancy', 'tenancy in common'],
                                            'ownership': ['freehold', 'freehold', 'non-freehold', 'non-freehold',
                                                          'concurrent', 'concurrent']})

        # https://www.redfin.com/resources/what-does-active-status-mean-in-real-estate-listings
        self.__estate_status = pd.DataFrame({'id': range(8),
                                             'estate_status_name': ['active', 'active contingent',
                                                                    'active – first right', 'active kick-out',
                                                                    'active – no-show', 'active option contract',
                                                                    'active with contingencies', 'inactive']})
        self.__address_generator = address_generator

    def generate(self, n=1):
        print('Generating information for ' + str(n) + ' estates...')
        time_start = time.time()

        generated_addresses = self.__address_generator.generate(n)
        unique_cities = generated_addresses['city'].unique()
        self.__cities = pd.DataFrame({'id': range(len(unique_cities)), 'city_name': unique_cities,
                                      'country_id': [0] * len(unique_cities)})

        self._list['id'] = range(0, n)
        self._list['number_of_bedrooms'] = np.random.randint(0, 4, n)
        self._list['number_of_bathrooms'] = [randint(1, bedrooms) if bedrooms > 0 else 1
                                             for bedrooms in self._list['number_of_bedrooms']]
        self._list['number_of_balconies'] = np.random.randint(0, 2, n)
        self._list['floor_space'] = (self._list['number_of_bedrooms'] + self._list['number_of_bathrooms'] + 2) * \
                                    np.random.randint(20, 26, n)
        self._list['balconies_space'] = self._list['number_of_balconies'] * np.random.randint(10, 15, n)

        self._list['estate_name'][self._list['number_of_bedrooms'] == 0] = 'Studio Apartment'
        self._list['estate_name'][self._list['number_of_bedrooms'] > 2] = 'House'
        self._list['estate_name'][(self._list['number_of_bedrooms'] == 1) & (self._list['floor_space'] > 92)] = 'House'
        self._list['estate_name'][(self._list['number_of_bedrooms'] == 1) &
                                  (self._list['floor_space'] <= 92)] = '1 Bed Apartment'
        self._list['estate_name'][(self._list['number_of_bedrooms'] == 2) & (self._list['floor_space'] > 115)] = 'House'
        self._list['estate_name'][(self._list['number_of_bedrooms'] == 2) &
                                  (self._list['floor_space'] <= 115)] = '2 Bed Apartment'

        self._list['pets_allowed'][self._list['estate_name'] != 'House'] = np.random.randint(0, 2, (self._list['estate_name'] != 'House').sum())
        self._list['pets_allowed'][self._list['estate_name'] == 'House'] = 1

        self._list['estate_type_id'] = self.__estate_types['type_name'].sample(n, replace=True).reset_index()
        self._list['estate_status_id'] = self.__estate_status['estate_status_name'].sample(n, replace=True).reset_index()

        self._list['number_of_garages'] = np.random.randint(0, 3, n)
        self._list['number_of_parking_spaces'] = np.random.randint(0, 3, n)

        self._list['city_id'] = [self.__cities[self.__cities['city_name'] == city].iloc[0]['id']
                                 for city in generated_addresses['city']]

        # TODO: self._list['estate_description']

        time_end = time.time()
        print('Done! Time taken: ' + str(time_end - time_start))
        return self._list

    def write_to_csv(self):
        print('Data saved to "generated_data/estate.csv".')
        self._list.to_csv('generated_data/estate.csv', columns=['estate_name', 'city_id', 'estate_type_id', 'floor_space',
                       'number_of_balconies', 'balconies_space', 'number_of_bedrooms',
                       'number_of_bathrooms', 'number_of_garages', 'number_of_parking_spaces',
                       'pets_allowed', 'estate_description', 'estate_status_id'])
        print('Data saved to "generated_data/estate_type.csv".')
        self.__estate_types.to_csv('generated_data/estate_type.csv', columns=['type_name'])
        print('Data saved to "generated_data/estate_status.csv".')
        self.__estate_status.to_csv('generated_data/estate_status.csv', columns=['estate_status_name'])
        print('Data saved to "generated_data/city.csv".')
        self.__cities.to_csv('generated_data/city.csv', columns=['city_name', 'country_id'])


class ContractGenerator(ThingGenerator):
    def __init__(self, client_generator, estate_generator, employee_generator):
        super(ContractGenerator, self).__init__(
            col_names=['id', 'client_id', 'employee_id', 'contract_type_id', 'contract_details', 'payment_frequency_id',
                       'number_of_invoice', 'payment_amount', 'fee_percentage', 'fee_amount', 'date_signed',
                       'start_date', 'end_date']
        )

        self.__client_generator = client_generator
        self.__estate_generator = estate_generator
        self.__employee_generator = employee_generator

        self.__contract_type = pd.DataFrame({'id': range(3), 'contract_type_name': ['sale brokerage service',
                                                                                    'purchase brokerage service',
                                                                                    'advertisement service']})
        self.__payment_frequency = pd.DataFrame({'id': range(4),
                                                 'payment_frequency_name': ['weekly', 'monthly', 'quarterly',
                                                                            'annually']})

        self.__under_contract = pd.DataFrame(columns=['id', 'estate_id', 'contract_id'])
        self.__contract_invoice = pd.DataFrame(columns=['id', 'contract_id', 'invoice_number', 'invoice_details',
                                                        'invoice_amount', 'date_created', 'date_paid'])

    def generate(self, n=1):
        print('Generating ' + str(n) + ' contracts...')
        time_start = time.time()

        self.__generated_estates = self.__estate_generator.generate(n=n)
        self.__generated_clients = self.__client_generator.generate(n=n)
        self.__generated_employees = self.__employee_generator.generate(n=1000)

        num_contracts = np.sum(self.__generated_estates['estate_status_id'] == 7)

        self._list['id'] = range(0, n)
        self._list['client_id'] = np.random.randint(0, n, n)
        self._list['employee_id'] = np.random.randint(0, 1000, n)
        self._list['contract_type_id'] = np.random.randint(0, 3, n)
        # TODO: self._list['contract_details']
        self._list['payment_frequency_id'] = np.random.randint(0, 4, n)
        # TODO: self._list['number_of_invoice']
        self._list['payment_amount'] = np.random.randint(200000, 700000, n)
        self._list['fee_percentage'] = np.random.randint(15, 50) / 10
        self._list['fee_amount'] = self._list['payment_amount'] * self._list['fee_percentage'] / 100
        self._list['fee_amount'] = self._list['fee_amount'].round(2)
        self._list['date_signed'] = ['{}-{:0>2d}-{:0>2d}'.format(randint(1990, 2019), randint(1, 11), randint(1, 28))
                             for i in range(n)]
        self._list['start_date'] = self._list['date_signed']
        self._list['end_date'] = ['{}-{:0>2d}-{:0>2d}'.format(year, randint(1, 12), randint(1, 28))
                                  for year in self._list['start_date'].str.slice(0, 4).map(int) +
                                  np.random.randint(1, 20, n)]

        self.__under_contract['id'] = range(n)
        self.__under_contract['estate_id'] = range(n)
        self.__under_contract['contract_id'] = range(n)

        self.__contract_invoice['id'] = range(n)
        self.__contract_invoice['contract_id'] = range(n)
        self.__contract_invoice['invoice_number'] = range(1039, 1039 + n)
        # TODO: self.__contract_invoice['invoice_details']
        self.__contract_invoice['invoice_amount'] = self._list['fee_amount']
        self.__contract_invoice['date_created'] = self._list['end_date']
        self.__contract_invoice['date_paid'] = self._list['end_date']

        time_end = time.time()
        print('Done! Time taken: ' + str(time_end - time_start))
        return self._list

    def write_to_csv(self):
        print('Data saved to "generated_data/contract.csv".')
        self._list.to_csv('generated_data/contract.csv', columns=['client_id', 'employee_id', 'contract_type_id', 'contract_details', 'payment_frequency_id',
                       'number_of_invoice', 'payment_amount', 'fee_percentage', 'fee_amount', 'date_signed',
                       'start_date', 'end_date'])

        print('Data saved to "generated_data/contract_type.csv".')
        self.__contract_type.to_csv('generated_data/contract_type.csv', columns=['contract_type_name'])
        print('Data saved to "generated_data/under_contract.csv".')
        self.__under_contract.to_csv('generated_data/under_contract.csv', columns=['estate_id', 'contract_id'])
        print('Data saved to "generated_data/payment_frequency.csv".')
        self.__payment_frequency.to_csv('generated_data/payment_frequency.csv', columns=['payment_frequency_name'])
        print('Data saved to "generated_data/contract_invoice.csv".')
        self.__contract_invoice.to_csv('generated_data/contract_invoice.csv', columns=['contract_id', 'invoice_number', 'invoice_details',
                                                        'invoice_amount', 'date_created', 'date_paid'])

        self.__employee_generator.write_to_csv()
        self.__employee_generator.write_to_excel()
        self.__client_generator.write_to_csv()
        self.__estate_generator.write_to_csv()

"""
in_charge = pd.DataFrame(columns=['estate_id', 'employee_id', 'date_from', 'date_to'])
in_charge['estate_id'] = range(0, 1000000)
in_charge['employee_id'] = np.random.randint(0, 1000, 1000000)
in_charge['date_from'] = ['{}-{:0>2d}-{:0>2d}'.format(randint(1990, 2019), randint(1, 6), randint(1, 28))
                             for i in range(1000000)]
in_charge['date_to'] = ['{}-{:0>2d}-{:0>2d}'.format(year, randint(6, 12), randint(1, 28))
                                  for year in in_charge['date_from'].str.slice(0, 4).map(int) +
                                  np.random.randint(1, 3, 1000000)]
in_charge.to_csv('generated_data/in_charge.csv')
"""
if __name__ == '__main__':
    person_generator = PersonGenerator()
    address_generator = AddressGenerator()

    employee_generator = EmployeeGenerator(person_generator)
    client_generator = ClientGenerator(person_generator, address_generator)
    estate_generator = EstateInfoGenerator(address_generator)

    contract_generator = ContractGenerator(client_generator, estate_generator, employee_generator)

    contract_generator.generate(1000000)
    contract_generator.write_to_csv()
