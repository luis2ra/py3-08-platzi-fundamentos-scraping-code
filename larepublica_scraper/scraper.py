import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

# XPATH_LINK_TO_ARTICLE = '//h2[@class="headline"]/a/@href'
XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
# XPATH_TITLE = '//h1[@class="headline"]/a/text()'
XPATH_TITLE = '//h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
# XPATH_BODY = '//div[@class="articleWrapper  "]/p[not(@class)]/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                print(title)
                title = title.strip()
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'files/{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)

            if not os.path.isdir('files'):
                os.mkdir('files')

            today = datetime.date.today().strftime('%Y-%m-%d')
            if not os.path.isdir(f'files/{today}'):
                os.mkdir(f'files/{today}')

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
