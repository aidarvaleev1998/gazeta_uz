import re
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse


def remove_tags(i, div):
    text = str(div)
    text = re.sub('</p>|</div>|</li>|<br/>|<br>|<hr/>|<hr>', '\n', text)
    text = re.sub('<p>|<p [^>]*>|<div[^>]*>|<li>|<li [^>]*>|<a>|<a [^>]*>|</a>|<span[^>]*>|</span>|<time[^>]*>|</time>|'
                  '<nobr[^>]*>|</nobr>|<img[^>]*>|<em[^>]*>|</em>|<tr[^>]*>|<td[^>]*>|</tr>|</td>|</tbody>|<tbody>|'
                  '<strong[^>]*>|</strong>|<ul[^>]*>|</ul>|<u>|</u>|<ol[^>]*>|</ol>|<h[1-6][^>]*>|</h[1-6]>|'
                  '<blockquote[^>]*>|</blockquote>|<wbr/>|<wbr>|<sub>|</sub>|<sup>|</sup>|<thead>|</thead>|\t|\r|'
                  '<i>|<i [^>]*>|</i>|<del>|<del [^>]*>|</del>|<b>|<b [^>]*>|</b>|<font[^>]*>|</font>|'
                  '<col[^>]*>|<center>|</center>|<colgroup[^>]*>|</colgroup>', '', text)
    text = re.sub('<script[^<]*</script>|<table[^<]*</table>|<figure[^<]*</figure>|'
                  '<button[^<]*</button>|<noscript[^<]*</noscript>|'
                  '<metricconverter[^<]*</metricconverter>|<u[^>]*>|'
                  '<twitterwidget[^<]*</twitterwidget>', '\n', text)
    text = re.sub('<iframe[^<]*</iframe>', '\n', text)
    text = re.sub('\n\n+', '\n', text)
    temp = re.findall('<[^>]*>', text)
    if len(temp) > 0:
        print(i, temp)
    # text = re.sub('<[^>]*>', '', text)
    return text.strip()


def download_text(i, link):
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "html.parser")
    div = soup.find(class_="article-text")
    text = remove_tags(i, div)
    return text


def to_ascii(link):
    link = list(urllib.parse.urlsplit(link.strip()))
    link[2] = urllib.parse.quote(link[2])
    link = urllib.parse.urlunsplit(link)
    return link


def download_all(ext):
    with open(f"gazeta.{ext}.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        start = 3308
        end = start + 1
        for i, link in enumerate(lines[start:end]):
            text = download_text(start + i, to_ascii(link))
            with open(f"data/{start + i}.{ext}", "w", encoding="utf-8") as g:
                g.write(text)


download_all("ru")
download_all("uz")
