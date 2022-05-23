import requests
import pandas as pd
from lxml import html


def send_request(url):
    response = requests.get(
        url='api',
        params={
            'api_key': '',
            'url': url,
        },

    )
    return response.content


old_data = pd.read_csv("old_data.csv")
search_list = old_data['part_number'].tolist()
manufact = old_data['manufacturer'].tolist()
data = {
    'part_number': [],
    'manufacturer': [],
    'Scraped Part': [],
    'Also known as': [],
    'Median Price': [],
    'Match': []
}
j = 0
for i in search_list[200000::]:
    tree = html.fromstring(send_request(f'https://octopart.com/search?q={i}'))
    button = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/span')
    if not button:
        scraped_part = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/'
                                  'div[1]/div[1]/div/a/div[2]/span/span')
        if scraped_part:
            scraped_part = scraped_part[0].text
        else:
            scraped_part = ' '
        amount = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/'
                            'div[1]/div[1]/div/div/span[2]')
        if amount:
            amount = amount[0].text
            currency = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/'
                                  'div[2]/div[1]/div[1]/div/div/span[1]')[0].text
            price = f'{currency} {amount}'
        else:
            price = ' '

        aka = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[1]/span[2]/mark')
        if not aka:
            aka = ' '
        else:
            aka = aka[0].text
        data['part_number'].append(i)
        data['manufacturer'].append(manufact[search_list.index(i)])
        data['Scraped Part'].append(scraped_part)
        data['Also known as'].append(aka)
        data['Median Price'].append(price)
        data['Match'].append(' ')
        df = pd.DataFrame(data)

        writer = pd.ExcelWriter('new_data2.xlsx', engine='xlsxwriter')

        df.to_excel(writer, sheet_name='Sheet1', index=False)

        writer.save()
        j += 1
        print(j)
    else:
        scraped_part = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/'
                                  'div/div[1]/div[1]/div/a/div[2]/span/span')
        if scraped_part:
            scraped_part = scraped_part[0].text
        else:
            scraped_part = ' '
        amount = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/div/div[1]/div[2]/'
                            'div[1]/div[1]/div/div/span[2]')
        if amount:
            amount = amount[0].text
            currency = tree.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/div/div[1]/'
                                  'div[2]/div[1]/div[1]/div/div/span[1]')[0].text
            price = f'{currency} {amount}'
        else:
            price = ' '

        aka = tree.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[1]/span[2]/mark')
        if not aka:
            aka = ' '
        else:
            aka = aka[0].text
        data['part_number'].append(i)
        data['manufacturer'].append(manufact[search_list.index(i)])
        data['Scraped Part'].append(scraped_part)
        data['Also known as'].append(aka)
        data['Median Price'].append(price)
        data['Match'].append('Not Found')
        df = pd.DataFrame(data)

        writer = pd.ExcelWriter('new_data2.xlsx', engine='xlsxwriter')

        df.to_excel(writer, sheet_name='Sheet1', index=False)

        writer.save()
        print('not found')
