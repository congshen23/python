import re
from parsel import selector
import requests   #数据请求模块
import parsel     #数据解析模块
import os         #文件夹操作模块，内置模块


for page in range(1,3):
    print(f"====================正在抓爬取第{page}页====================")
    ##1、发起url请求，提取标签
    base_url = f'https://clubloli.com/a/w/page/{page}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'} 
    response = requests.get(url=base_url,headers=headers)
    html = response.text

    selector = parsel.Selector(html)     #把字符串转换成对象
    divs = selector.xpath('//div[@class="posts grids  clearfix"]/div')  #所有div  xpath语法
    # print(divs)

    ##2、取标签里的具体信息
    for div in divs:
        title = div.xpath('.//a/@title').get()    #相册标题
        title = title.replace('<','').replace('>','').replace('/','').replace(' \ ','').replace('|','').replace(':','').replace('*','').replace('?','')   ###  要改一下不然下面创建文件夹会出错
        add = div.xpath('.//a/@href').get()       #相册链接
        # print(title,add)
        print("正在创建相册：", title)

        if not os.path.exists('img\\'+ title):   #如果没有相册标题文件
            os.mkdir('img\\'+ title)            #就创建一个

    ##3、取二级链接里面的所有图片标签
        html_2 = requests.get(url=add,headers=headers).text
        selector2 = parsel.Selector(html_2) 
        img_url_list = selector2.xpath('//div[@class="article-content"]/figure/img/@src').getall()   #解析每一个图片地址
        # print(img_url_list) 

        for img_url in img_url_list:
            img_data = requests.get(url=img_url,headers=headers).content           #content二进制数据转化

            #准备文件名
            file_name = img_url.split('/')[-1] #以/为分隔符，取最后一项

            #数据保存
            with open(f'img\\{title}\\{file_name}' + file_name,mode="wb") as f:
                f.write(img_data)
                print('下载完成放入相册：'+ title,file_name)

print("===================================爬取完毕===================================")