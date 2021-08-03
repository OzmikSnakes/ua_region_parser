import csv

from companies_parser import CompaniesParser, Company

parser = CompaniesParser()
for i in range(1, 6):
    parser.parse(f'https://www.ua-region.com.ua/ru/kved/01.11?start_page={i}')
print(len(parser.companies))
parser.close_driver()

with open('res/companies.csv', mode='w', encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=',', lineterminator='\r')
    file_writer.writerow(['Название', 'Адрес', 'Юридический адрес', 'Фактический адрес',
                          'Почтовый адрес', 'Телефоны', 'Факс', 'E-mail', 'Сайт'])
    for company in parser.companies:
        file_writer.writerow([company.name, company.locations['Адрес'], company.locations['Юридический адрес'],
                              company.locations['Фактический адрес'], company.locations['Почтовый адрес'],
                              ', '.join(company.phone_numbers), company.fax, ', '.join(company.emails),
                              company.website])
