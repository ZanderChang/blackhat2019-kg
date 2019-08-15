from requests_html import HTMLSession
from requests_html import HTML
import os
import csv

TARGET = 'https://www.blackhat.com/us-19/briefings/schedule/index.html'


def getHTML(url, file='full.html'):
    session = HTMLSession()
    r = session.get(url)
    print(len(r.html.links))
    r.html.render()
    print(len(r.html.links))
    with open(file, 'w', encoding='utf-8') as fp:
        fp.write(r.html.html)


def HTML2csv(htmlfile, csvfile):
    fp = open(htmlfile, 'r', encoding='utf-8')
    html = HTML(html=fp.read())
    fp.close()

    data = html.find('.data-container')
    links = html.find('.data-container a')
    data_links = []
    for link in links:
        if 'sd_link' in link.attrs['class']:
            data_links.append(link)
    assert len(data) == len(data_links)

    csv_fp = open(csvfile, 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_fp)
    header = ['title', 'speaker', 'track', 'url']
    writer.writerow(header)

    for i, d in enumerate(data):
        d = d.text.split('\n')
        title = d[0]
        speaker = d[2][9:].replace(', ', ',')
        track = d[4]
        for j in range(5, len(d)):
            if 'Format' in d[j]:
                break
            track += d[j]
        url = TARGET + data_links[i].attrs['href']

        row = [title, speaker, track, url]
        writer.writerow(row)
    
    print(len(data))
    csv_fp.close()

if __name__ == "__main__":
    # getHTML(TARGET)
    HTML2csv('full.html', 'blackhat2019.csv')
