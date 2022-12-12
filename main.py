import time
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from tqdm import tqdm

headers = Headers(os='win', browser='chrome')

def get_url():
    for page in tqdm(range(1,40)):
        url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}&hhtmFrom=vacancy_search_list'
        re = requests.get(url, headers=headers.generate())
        soup = BeautifulSoup(re.text, features= 'html.parser')
        all_vacancy = soup.find_all('div', class_='serp-item')

        for vacancy in all_vacancy:
            vacancy_url = vacancy.find('a', class_='serp-item__title')['href']
            yield vacancy_url


def get_vacancy(data,card):
        try:
            description = data.find('div', attrs={'data-qa': 'vacancy-description'}).text
        except:
            description = ''
        if 'Django' in description and 'Flask' in description:

            title = data.find('h1', attrs={'data-qa':'vacancy-title'}).text
            try:
                salary = data.find('span', attrs={'data-qa':'vacancy-salary-compensation-type-net'}).text.replace('\xa0','')
            except:
                salary = ''
            
            company_name = data.find('a', attrs={'data-qa':'vacancy-company-name'}).text.replace('\xa0',' ')
            city = data.find('div', attrs={'data-qa':'vacancy-serp__vacancy-address'}).text.replace('\xa02', '').replace('\xa0','')
            if salary != '' and description != '':
                vacancies = {
                                    'title' : title,
                                    'url' : card,
                                    'salary' : salary,
                                    'company': company_name,
                                    'city' : city
                                    
                                }

                return vacancies


          

def main():
    vacancies_list =[]
    for card in get_url():
        re = requests.get(card, headers=headers.generate())
        time.sleep(0.3)
        soup = BeautifulSoup(re.text, features= 'html.parser')
        data = soup.find('div', class_='main-content')
        if get_vacancy(data,card) != None:
            vacancies_list.append(get_vacancy(data,card))
            with open ('result.json', 'w', encoding='utf-8') as f:
                json.dump(vacancies_list, f, indent=4, ensure_ascii=False)
            
        
    
if __name__ == '__main__':
    main()

    
