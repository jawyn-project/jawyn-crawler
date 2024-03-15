import requests
from bs4 import BeautifulSoup
import re
import time
import json


def take(link, result,key):
    url = link
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Couldn't access {url}. Error: {e}")
        return [], [], []

    html_2 = r.text.encode("utf8")

    # Extraindo texto da página
    soup = BeautifulSoup(html_2, 'html.parser')
    paragraphs = soup.find_all('p')
    all_text = ' '.join(p.get_text() for p in paragraphs)

    headline = soup.title.string

    result.append(f'{{"key": "{key}", "link": "{link}", "headline": "{headline}", "content": "{all_text}"}}')

    # Extraindo todos os links da página
    wiki_links = []
    other_links = []

    for link in soup.find_all('a', href=True):
        full_link = link['href']
        if full_link.startswith('/'):
            full_link = 'https://pt.wikipedia.org' + full_link
            wiki_links.append(full_link)
        elif full_link.startswith('http'):
            other_links.append(full_link)

    # Separando links da Wikipédia
    title_links = []
    other_wiki_links = []

    for link in wiki_links:
        if re.match(r'https://pt\.wikipedia\.org/wiki/[^/:(]*$', link) and not link.endswith('.png'):
            if link not in title_links:
                title_links.append(link)
        else:
            other_wiki_links.append(link)

    return title_links, other_wiki_links, other_links


def traverse(title_links, result, link_acess,key):
    print()

    for i in range(5):
        if title_links:
            link = title_links.pop(0)

            if link not in link_acess:
                print("calling link:" + link)
                time.sleep(1)
                new_title_links, other_wiki_links, other_links = take(link, result,key)
                title_links.extend(new_title_links)
                link_acess.append(link)


result = []
link_acess = []
keys = ["Brsil", "Bolo", "Gato"]


for i in range(len(keys)):
    link = ('https://pt.wikipedia.org/wiki/' + keys[i])
    title_links, other_wiki_links, other_links = take(link, result, keys[i])
    traverse(title_links, result, link_acess, keys[i])


file_name = "data.json"

try:
    with open(file_name, "w", encoding='utf-8') as file:
        for item in result:
            file.write(json.dumps(item, ensure_ascii=False))
            file.write('\n')
    print(f"JSON saved successfully at: {file_name}")
except Exception as e:
    print(f"Error saving JSON: {e}")


#ler o .json

# try:
#     with open(file_name, "r", encoding='utf-8') as file:
#         json_content = [json.loads(line) for line in file]
#     print(json_content)
# except Exception as e:
#     print(f"Error reading JSON: {e}")
