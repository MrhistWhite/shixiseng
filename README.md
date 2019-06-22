# shixiseng
找实习的时候我们常常会出现这样的情况：每天都要打开网站浏览一遍，再一个个点进去查看JD，不断地重复。于是产生了自己写一个程序来检测职位更新，并且采集职位需求来自行进行检索的想法，采集的字段如下：
![image](https://github.com/MrhistWhite/shixiseng/blob/master/add_img/shixiseng_discription.png)
**crawler** 模块为爬虫的主体模块，结合数据采集与清洗功能于一体  
**create_word_dict** 模块为破解字体加密的模块，实习僧的前端页面中的反爬措施对数据采集造成了障碍，需要先得到网站使用的字体映射来还原数据  
**main** 文件为主函数  
**email_sender** 模块为发送邮件的模块  
最终完成的效果如图：  
![image](https://github.com/MrhistWhite/shixiseng/blob/master/add_img/final.png)
