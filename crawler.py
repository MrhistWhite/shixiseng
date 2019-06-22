import pymysql, requests, re, random
from lxml import etree
import datetime

class shixiseng_crawl():
    def __init__(self, city, word_dict, keyword):
        db = pymysql.connect('你的主机', '你的用户名', '你的密码', 'recruitment', charset='utf8')
        self.c = city
        self.cur = db.cursor()
        self.wd = word_dict
        self.db = db
        self.count = 0  # 职位计数
        self.city_count = 1  # 城市计数
        self.keyword = keyword
        self.update = 0  # 更新计数

    def walk_pages(self):

        for url in self.c:

            req = requests.get(url, headers=self.get_ua())
            html = etree.HTML(req.text)
            url_list = html.xpath('//ul[@class="position-list"]/li/div/div/a[@class="position-name"]/@href')
            page = int(re.findall('共(\d+)页', html.xpath('//li[@class="active"]/a/@title')[0])[0])

            for i in range(1, page + 1):

                if self.update == 999:
                    self.update = 0
                    break

                print('开始采集第 %d 个城市的第 %d 页，共 %d 页' % (self.city_count, i, page))
                if i == 1:
                    self.get_content(url_list)
                else:
                    new_url = url + str(i)
                    new_req = requests.get(new_url, headers=self.get_ua())
                    html = etree.HTML(new_req.text)
                    url_list = html.xpath('//ul[@class="position-list"]/li/div/div/a[@class="position-name"]/@href')

                    self.get_content(url_list)

            self.city_count += 1

    def get_content(self, url_list):

        for url in url_list:

            url = 'https://www.shixiseng.com' + url

            # 此部分是用来更新每天的数据。如果当天没有新的职位信息则停止采集

            if self.keyword == '数据':
                sql = """select url from shixiseng where url = '%s'""" % (url)
                self.cur.execute(sql)
                data = self.cur.fetchall()
                if len(data) != 0:
                    continue
                else:
                    self.update += 1
                    print('*' * 60)
                    print('当天已更新 %d 条记录' % self.update)
                    print('*' * 60)

            req = requests.get(url, headers=self.get_ua())
            text = req.text
            html = etree.HTML(text)

            try:
                salary = html.xpath('//div[@class="job_msg"]/span[@class="job_money cutom_font"]/text()')[0]
                position = html.xpath('//div[@class="con-job job_city"]/span[@class="com_position"]/text()')[0]
                degree = html.xpath('//div[@class="job_msg"]/span[@class="job_academic"]/text()')[0]
                duty = html.xpath('//div[@class="job_msg"]/span[@class="job_week cutom_font"]/text()')[0]
                duration = html.xpath('//div[@class="job_msg"]/span[@class="job_time cutom_font"]/text()')[0]
                jd = re.sub('\n|\t|\r', '', ''.join(
                    html.xpath('//div[@class="job-content"]/div/div/div/div[@class="job_detail"]/text()')))
                if jd == '':
                    raw = re.findall('<div class="job-content">.*<div class="con-job job_city">', req.text, re.S)[0]
                    jd = re.sub('<.*?>|\n|\t|&nbsp', '', raw)
                    if jd == '':
                        prefix = '-*-' * 10
                        print(prefix + '新的 JD 格式无法被捕获' + prefix)
                job_name = html.xpath('//div[@class="new_job_name"]/span/text()')[0]
                company = html.xpath('//div[@class="com_intro"]/a[@class="com-name"]/text()')[0]
                com_detail = ''.join(html.xpath('//div[@class="com-detail"]/span/text()'))

                salary = self.convert(salary)
                duty = self.convert(duty)
                duration = self.convert(duration)

                # 插入数据库
                sql = """insert into shixiseng (salary, duty, position, degree, jd, duration, job_name, company, com_detail, url, keyword, time)
                         values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')         
                """ % (
                salary, duty, position, degree, jd, duration, job_name, company, com_detail, req.url, self.keyword, datetime.datetime.now())
                try:
                    self.cur.execute(sql)
                    self.db.commit()
                    self.count += 1
                    if self.count % 10 == 0:
                        print('-' * 60)
                        print('成功采集 %d 条数据' % self.count)
                        print('-' * 60)
                except Exception as e:
                    print('*' * 60)
                    print('入库报错，错误信息为：%s' % e)
                    print('以下为出错链接采集到的信息：')
                    print(salary)
                    print(duty)
                    print(duration)
                    print(jd)
                    print(com_detail)
                    print(degree)
                    print(position)
                    print(job_name)
                    print(company)
                    print(req.url)
                    self.db.rollback()
                    print('*' * 60)

            except Exception as e:
                print('获取内容出错，错误信息为：%s' % e)
                print('出错链接为：%s' % req.url)

    def get_ua(self):
        ua_list = [
            'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
            'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
            'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0',
            'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
            'Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)',
            'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
            'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
            'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11',
            'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
            'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)'
        ]
        ua = random.choice(ua_list)
        headers = {"User-Agent": ua}

        return headers

    # 关闭数据库
    def close_db(self):
        self.db.close()

    # 字符转换函数
    def convert(self, in_string):
        f = lambda x: hex(ord(x))
        out_string = ''
        for s in in_string:
            c = f(s)
            try:
                if c in self.wd.keys():
                    out_string += self.wd[c]
                else:
                    out_string += s
            except:
                print(s)
        return out_string
