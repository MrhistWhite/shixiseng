# 实习僧职位更新自动推送项目
找实习的时候我们常常会出现这样的情况：每天都要打开网站浏览一遍，再一个个点进去查看JD，不断地重复。于是产生了自己写一个程序来检测职位更新，并且采集职位需求来自行进行检索从而定时将更新的职位信息推送到手机客户端的想法，采集的字段如下：
![image](https://github.com/MrhistWhite/shixiseng/blob/master/add_img/shixiseng_discription.png)
## crawler模块
- 爬虫的主体模块，结合数据采集与清洗功能于一体  
## create_word_dict
- 模块为破解字体加密的模块，实习僧的前端页面中的反爬措施对数据采集造成了障碍，需要先得到网站使用的字体映射来还原数据  
## main模块
- 主函数  
## email_sender模块
- 发送邮件的模块  
## 最终完成效果  
- 如图所示。由于JD字符过长此处不予展示，数据库中的其他字段的设置是为了方便管理此处也不作展示。最后一列设置为点击即可打开职位详情页面。
![image](https://github.com/MrhistWhite/shixiseng/blob/master/add_img/final.jpg)
## 服务优化
- 有服务器的朋友可将此程序置于后台定时执行，这样就可以真正意义上的实现自动推送功能，妈妈再也不用担心我的实习啦！
