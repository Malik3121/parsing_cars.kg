import requests
from bs4 import BeautifulSoup
import csv

def write_to_csv(data: dict):
    with open('data.csv', 'a') as file:
        write = csv.writer(file)
        write.writerow((data['title'], data['price'], data['img'], data['desk']))

def get_html(url):
    response = requests.get(url)
    # print(response.status_code)
    # print(response.text)
    return response.text

def get_page(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('div',class_ = 'pages fl').find_all('a')
    # print(page_list)
    last_page = page_list[-2].text
    return last_page


def get_data(html):
    soup = BeautifulSoup(html,'lxml')
    # print(soup)
    cars = soup.find('div', class_ = 'catalog-list').find_all('a')
    # print(cars)
    for car in cars:
        try:
            title = car.find('span', class_ ='catalog-item-caption').text.strip()
        except:
            title = ''
        # print(title)
        try:
            price = car.find('span', class_ = 'catalog-item-price').text
        except:
            price = ''
        # print(title + price)
        try:
            comment = car.find('span', class_ = 'catalog-item-descr').text.split()
            desk = ' '.join(comment)
        except:
            desk = ''
        # print(title + price + desk)
        try:
            img = car.find('img').get('src')
        except:
            img =''
        
        data = {
            'title': title,
            'price': price,
            'desk': desk,
            'img': img
        }
        write_to_csv(data)


def main():
    url = 'https://cars.kg/offers'
    html = get_html(url)
    num = int(get_page(html))
    i = 1
    while i <= num:
        # print(i)
        url = f'https://cars.kg/offers/{i}'
        html = get_html(url)
        get_data(html)
        if i == num:
            num = int(get_page(html))
        i += 1



with open('data.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['title', 'price','image','descriptions'])


main()