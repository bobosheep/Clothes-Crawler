
import time
import queue
import datetime

from scrapy.selector import Selector


def ParseLativ(cur_url, response):
    
    item = dict({
                "site":"",
                "name":"",
                "gender":"",
                "category":"",
                "url":"",
                "objID":"",
                "image_urls":"",
                "price":"",
                "store_price":"",
                "color":"",
                "colors":"",
                "sizes":"",
                "last_updated":""
            })
    for obj in response.xpath('//*[@id="exhibit"]/div[2]'):
            
            name = response.xpath('//*[@id="productImg"]/@title').extract_first()
            color = response.xpath('//span[@id="icolor"]/text()').extract_first()
            if name == [] or name is None:
                continue

            nameSplit = name.split('-')
            for spl in nameSplit :
                if not ( spl.find('男') or spl.find('女') or spl.find('童') )and  not (spl == nameSplit[0]):
                    nameSplit[0] += spl
            item['name'] = nameSplit[0]
            item['site'] = 'lativ'
            
            if item['name'] == [] or item['name'] is None:
                continue
            item['color'] = color
            print(item['name'])
            print(item['color']) 
            item['url'] = cur_url
            item['objID'] = response.xpath('//*[@id="isn"]/text()').extract_first()
            item['image_urls'] = response.xpath('//*[@id="productImg"]/@src').extract_first() 
            item['colors'] = response.xpath('//*[@id="exhibit"]/div[2]/div[3]/div[2]/div[3]/a/img/@title').extract()
            item['sizes'] = response.xpath('//*[@id="sizelist"]/a/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            if name.find('女') > 0:
                item['gender'] = '女'
            elif name.find('男') > 0:
                item['gender'] = '男'
            else :
                item['gender'] = '其他'

            #衣服類
            if  nameSplit[0].find('衫') >= 0  \
                or nameSplit[0].find('背心') >= 0 or nameSplit[0].find('洋裝') >= 0:
                item['category'] = '衣服'
            #外套類
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 or nameSplit[0].find('夾克') >= 0 or nameSplit[0].find('大衣') >= 0:
                item['category'] = '外套'
            #內衣類
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0 or nameSplit[0].find('罩') >= 0:
                item['category'] = '內衣'
            #內褲類
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                    or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0 or nameSplit[0].find('內褲') >= 0:
                item['category'] = '內褲'
            #褲裙類
            elif nameSplit[0].find('褲') >= 0 or nameSplit[0].find('裙') >= 0:
                item['category'] = '褲裙'
            #鞋類
            elif nameSplit[0].find('鞋') >= 0 :
                item['category'] = '鞋'
            elif nameSplit[0].find('T') >= 0 or nameSplit[0].find('衣') >= 0 :
                item['category'] = '衣服'
            #配件
            else :
                item['category'] = '其他'
            
            
            if response.xpath('//*[@id="store_price"]/text()').extract_first():
                #優惠價
                item['price'] = response.xpath('//*[@id="specialPrice"]/text()').extract_first()
                #原價
                item['store_price'] = response.xpath('//*[@id="store_price"]/text()').extract_first()
            else :  #可能沒有優惠價
                #價格
                item['price'] = response.xpath('//*[@id="price"]/text()').extract_first()
           

        #End for
    
    return item

