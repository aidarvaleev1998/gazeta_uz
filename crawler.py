import urllib.request
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


class PageIterator(object):
    def __init__(self, curr_date, link):
        self.curr_page = 1
        self.curr_date = curr_date
        self.link = link
        self.cache = []
        self.cache = self.get_divs()

    @staticmethod
    def equal(x, y):
        if len(x) == len(y) == 0:
            return True
        elif len(x) != len(y):
            return False
        return PageIterator.div2tuple(x[0])[1] == PageIterator.div2tuple(y[0])[1]

    def get_divs(self):
        page = urllib.request.urlopen(self.link + str(self.curr_page))
        soup = BeautifulSoup(page, "html.parser")
        divs = soup.find_all(class_="rnBlock")
        if PageIterator.equal(divs, self.cache):
            divs = []
        return divs

    @staticmethod
    def tuple2date(tuple):
        _, page_link = tuple
        date = page_link[25:35].split('/')
        date = datetime(int(date[0]), int(date[1]), int(date[2]))
        return date

    @staticmethod
    def div2tuple(div_block):
        img_link = div_block.contents[1].contents[1]["data-src"]
        page_link = "https://www.gazeta.uz" + div_block.contents[1]['href']
        return img_link, page_link

    def get_next(self):
        if len(self.cache) == 0:
            return []

        pages = list(map(PageIterator.div2tuple, self.cache))

        while len(pages) > 0 and PageIterator.tuple2date(pages[-1]) >= self.curr_date:
            self.curr_page += 1
            self.cache = self.get_divs()
            if len(self.cache) == 0:
                break
            pages += list(map(PageIterator.div2tuple, self.cache))

        pages = [p for p in pages if PageIterator.tuple2date(p) == self.curr_date]

        self.curr_date -= timedelta(1)
        return pages


class SiteIterator(object):
    def __init__(self, curr_date, link):
        self.news = PageIterator(curr_date, link + "/news?page=")
        self.articles = PageIterator(curr_date, link + "/articles?page=")
        self.media = PageIterator(curr_date, link + "/media?page=")

    def get_next(self):
        return self.news.get_next() + self.articles.get_next() + self.media.get_next()


def find(ru_page, uz_pages):
    img_link = ru_page[0]
    for uz_p in uz_pages:
        if uz_p[0] == img_link:
            return uz_p
    return None


def preprocess(ru, uz):
    ru_text, uz_text = ru[1], uz[1]
    return ru_text, uz_text


def main():
    n = 0
    curr_date = datetime(2016, 9, 12)

    ru_iterator = SiteIterator(curr_date, "https://www.gazeta.uz/ru/list")
    uz_iterator = SiteIterator(curr_date, "https://www.gazeta.uz/uz/list")

    uz_prev = []
    uz_curr = uz_iterator.get_next()

    end_date = datetime(2011, 12, 4)
    while curr_date > end_date:
        ru_curr = ru_iterator.get_next()
        uz_next = uz_iterator.get_next()

        for ru_page in ru_curr:
            uz_page = find(ru_page, uz_prev + uz_curr + uz_next)
            if uz_page is not None:
                n += 1
                ru_page, uz_page = preprocess(ru_page, uz_page)
                with open("gazeta.ru.txt", "a", encoding="utf-8") as f:
                    f.write(ru_page + "\n")
                with open("gazeta.uz.txt", "a", encoding="utf-8") as f:
                    f.write(uz_page +  "\n")

        uz_prev = uz_curr
        uz_curr = uz_next

        print(curr_date, f'n={n}')
        curr_date -= timedelta(1)


main()

