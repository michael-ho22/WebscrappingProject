from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import plotly.express as px
import pandas as pd

authors_list = []
author_count = {}
authors_list.clear()
author_count.clear()

quotes_list = []
num_of_words = 0
num_of_quotes = 0
most_words = 0
longest_quote = ''
least_words = 300
shortest_quote = ''

tags_list = []
tags_dict = {}

for page in range(1,11):
    url = 'https://quotes.toscrape.com/page/' + str(page) + '/'
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url, headers=headers)

    website = urlopen(req).read()
    soup = BeautifulSoup(website, 'html.parser')
    


    ## START OF AUTHOR STATISTICS ##
    authors = soup.findAll('small',class_='author')
    

    for x in range(0,10):
        author = authors[x].text
        if author not in authors_list:
            authors_list.append(author)
            author_count[author] = 1
        else:
            author_count[author] += 1
            # if author_count[author] > most_quotes:
            #     most_quotes = author_count[author]
            #     author_most_quotes = author
    
    most_quotes = max(author_count.values())
    author_most_quotes = max(author_count, key=author_count.get)
    least_quotes = min(author_count.values())
    author_least_quotes = min(author_count, key=author_count.get)
    
    min_authors = [k for k, v in author_count.items() if v == least_quotes] #helps removes the list brackets when printing
    minimum = str(min_authors)
    minimum = minimum.replace("'", "").replace('"', '')
    ## END OF AUTHOR STATISTICS ##



    ## START OF QUOTE ANALYSIS ##
    quotes = soup.findAll('span',class_='text')
    

    for x in range(0,10):
        author = authors[x].text
        quote = quotes[x].text
        words = len((quote).split())
        num_of_words += words
        num_of_quotes += 1
        if words > most_words:
            most_words = words
            longest_quote = quote
            long_author = author
        else:
            continue
        if words < least_words:
            least_words = words
            shortest_quote = quote
            short_author = author
        # quotes_list.append(quote)
    ## END OF QUOTE ANALYSIS ##
    


    ## START OF TAG ANALYSIS ##
    tags = soup.findAll('a',class_='tag')
    length = len(tags) - 10

    for x in range(length):
        tag = tags[x].text
        if tag not in tags_list:
            tags_list.append(tag)
            tags_dict[tag] = 1
        else:
            tags_dict[tag] += 1
    ## END OF TAG ANALYSIS ##


## RESULTS FOR AUTHOR STATS ##
# print(authors_list)
# print(author_count)
# sorted_authors = sorted(author_count.items(), key = lambda x:x[1], reverse=True)
# print(sorted_authors)
print('                               AUTHOR STATS                                 ')
print('--------------------------------------------------------------------------\n')
print(f'{author_most_quotes} has the most quotes with {most_quotes} quotes.\n')
print(f"{str(minimum)[1:-1]} have the least quotes with {least_quotes} quotes.\n")
print('--------------------------------------------------------------------------\n\n\n')


## RESULTS FOR QUOTE ANALYSIS ##
avg_length = num_of_words/num_of_quotes
# print(num_of_words)
# print(num_of_quotes)
# print(avg_length)
print('                             QUOTE ANALYSIS                                 ')
print('--------------------------------------------------------------------------\n')
print(f'Average length of quotes is: {avg_length} words\n')
print(f'The longest quote is "{longest_quote}" by {long_author} with {most_words}\n')
print(f'The shortest quote is "{shortest_quote}" by {short_author} with {least_words}\n')
print('--------------------------------------------------------------------------\n\n\n')


## RESULTS FOR TAG ANALYSIS ##
print('                               TAG ANALYSIS                                 ')
print('--------------------------------------------------------------------------\n')
sorted_tags = sorted(tags_dict.items(), key = lambda x:x[1], reverse=True)
data = list(sorted_tags)
print(f'DISTRIBUTIONS OF TAGS:')
for x,y in tags_dict.items():
    print(f'{x}: {y}')
# print(data)

print('\nTop 10 tags that appeared the most:')
for t in data[0:10]:
    print(str(t)[1:-1])
print()

print('--------------------------------------------------------------------------\n')


## DATA VISUALIZATION ##
sorted_authors = dict(sorted(author_count.items(), key = lambda x:x[1], reverse=True))
# print(sorted_authors)

out = dict(list(sorted_authors.items())[0: 10])
# print(out)

data = []

for a,b in out.items():
    data.append([a,b])

df = pd.DataFrame(data, columns=['Author', 'Number of Quotes'])

fig = px.bar(df, x='Author', y='Number of Quotes', title='Top Ten Authors Total Quotes')
fig.update_layout(title_text='<b>Top Ten Authors Total Quotes</b>', 
                  title_x=0.5, 
                  font_family='Courier New',
                  font_color='black',
                  title_font_size=36)
fig.update_xaxes(tickfont_family='Courier New Black')
fig.update_yaxes(tickfont_family='Courier New Black')
fig.show()
