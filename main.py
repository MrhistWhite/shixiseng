from create_word_dict import get_word_dict
from crawler import shixiseng_crawl
from urllib.parse import quote
from email_sender import sendEmail
import pandas as pd
pd.set_option('display.max_colwidth', -1)

if __name__ == '__main__':

    keyword = '数据'

    gz = 'https://www.shixiseng.com/interns/c-440100_?k={k}&p='.format(k=quote(keyword))
    sz = 'https://www.shixiseng.com/interns/c-440300_?k={k}&p='.format(k=quote(keyword))
    city = [gz,sz]

    word_dict = get_word_dict(city[0])
    intern = shixiseng_crawl(city, word_dict, keyword)
    intern.walk_pages()
    print('数据采集完成')

    sql = """SELECT * FROM shixiseng WHERE date( time ) = curdate( ) 	AND keyword LIKE '%数据%' AND jd LIKE '%python%'
        AND position LIKE '%深圳%' AND degree = '本科'"""

    intern.cur.execute(sql)
    data = intern.cur.fetchall()
    if len(data) != 0:
        data = pd.DataFrame(list(data))
        col = list(range(1,11))
        col.remove(5)
        data = data.iloc[:,col]
        data.columns = ['salary','duty','position','degree','duration','url','company','com_detail','job_name']
        sendEmail(data)
    intern.close_db()
