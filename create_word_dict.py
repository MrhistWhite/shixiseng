import re, os, time, requests, base64
from fontTools.ttLib import TTFont

# 字符加密破解字典
def get_word_dict(url):
    update = time.localtime(os.stat(r"自定义文件目录/font.xml").st_mtime)
    now = time.localtime()
    f = lambda x: time.strftime('%Y-%m-%d', x)

    if f(update) != f(now):

        print('--- 字符串开始更新 ---')
        req = requests.get(url)
        text = req.text
        text1 = re.findall('src: url\(".*"\)', text)[0]
        fonts_after = re.findall('base64,(.*)"',text1)[0]

        if fonts_after:
            base_font = base64.b64decode(fonts_after)  # 使用base64库对字体信息进行解析
            with open("new.woff", 'wb') as f:
                f.write(base_font)
        font_ttf = TTFont("new.woff")  # 使用TTFont对字体文件进行解析
        font_ttf.saveXML('font.xml')  # 将字体信息保存为xml文件，方便后面读取和转换内容

    with open('font.xml') as f:
        file = f.read()

    keys = re.findall('<map code="(0x.*?)" name="uni.*?"/>', file)
    values = re.findall('<map code="0x.*?" name="uni(.*?)"/>', file)

    for i in range(len(values)):
        s = values[i]
        if len(s) < 4:
            values[i] = ('\\u00' + s).encode('utf-8').decode('unicode_escape')
        else:
            values[i] = ('\\u' + s).encode('utf-8').decode('unicode_escape')

    word_dict = dict(zip(keys, values))

    return word_dict
