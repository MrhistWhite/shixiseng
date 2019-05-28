from create_word_dict import get_word_dict
from crawler import shixiseng_crawl
from urllib.parse import quote

if __name__ == '__main__':
    keyword = 'BI'
    gz = 'https://www.shixiseng.com/interns/c-440100_?k={k}&p='.format(k=quote(keyword))
    sz = 'https://www.shixiseng.com/interns/c-440300_?k={k}&p='.format(k=quote(keyword))
    city = [gz, sz]

    word_dict = get_word_dict(city[0])
    intern = shixiseng_crawl(city, word_dict, keyword)
    intern.walk_pages()
    intern.close_db()
    print('数据采集完成')