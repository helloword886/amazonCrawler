import csv
import urllib

import requests
from parsel import Selector


# 发送请求，获得返回内容
def get_content(url):
    kv = {
    'referer': 'https://www.amazon.com/Arshiner-Classic-Sleeve-Leotard-Ballet/dp/B097PWMMV8',
   'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    resp = requests.get(url=url,headers=kv)
    content = resp.content.decode('utf-8')
    return content


# 下载图片
def down_image(imgUrl,name):
    # 解析服务器响应的文件
  # 下载图片到文件夹，路径为当前项目下的fengjingimage文件夹
   urllib.request.urlretrieve(url=imgUrl, filename='./amazonimage/' + name + '.jpg')

try:
    url = 'https://www.amazon.com/Arshiner-Classic-Sleeve-Leotard-Ballet/dp/B097PWMMV8'
    content = get_content(url)
    print(content)
    select = Selector(text=content)
    itemTitle = select.xpath('//span[@id="productTitle"]/text()').extract_first()
    itemPrice = select.css('.a-offscreen::text').extract_first()
    imgUrls = select.xpath('//*[@id="thumbImages"]/ul/li//img[contains(@src,",50_.jpg")]/@src').extract()
    itemInfo = select.xpath('//*[@id="feature-bullets"]//text()').extract()
    print(itemTitle,itemPrice, imgUrls,itemInfo)
    # ::把文本信息写入到csv中
    with open('亚马逊.csv', mode='a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([url, itemTitle, itemPrice,imgUrls,itemInfo])
    # ::text: 提取到要再去抓的video、图片的url，再去抓取
    for imgUrl in imgUrls:
        #这里一定要替换，否则是个缩略图，没啥用
        imgUrl =  imgUrl.replace(',50_','');
        #下面没写完，图片抓取并存入本地，TODO
        #down_image(imgUrl,'haha')
except:
    print('爬取失败')
