# -*- coding: utf-8 -*-
#author:Haochun Wang

# import scrapy
from scrapy.spiders import Spider
import re
# from scrapy import *
import re, sys
import requests
import math

# if sys.getdefaultencoding() != 'utf-8':
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
url = 'http://www.boc.cn/sourcedb/whpj/index.html'  # Bank of China currency website
html = requests.get(url).content.decode('utf8')
a = html.index('<td>澳大利亚元</td>')  # get the position of AUS dollar
s = html[a:a + 300]  # narrow down the range
rate_res = float(re.findall('<td>(.*?)</td>', s)[3])  # Regex get the currency
rate_res = math.ceil(rate_res*0.1)*0.1

class ChemistSpider(Spider):
    name = "chemist_cn"
    allowed_domains = ["www.chemistwarehouse.hk"]
    start_urls = [
        "http://www.chemistwarehouse.hk/Shop-Online/587/Swisse",
        "http://www.chemistwarehouse.hk/Shop-Online/587/Swisse?page=2",
        "http://www.chemistwarehouse.hk/Shop-Online/587/Swisse?page=3",
        "http://www.chemistwarehouse.hk/Shop-Online/587/Swisse?page=4",
        "http://www.chemistwarehouse.hk/Shop-Online/587/Swisse?page=5",

        "http://www.chemistwarehouse.hk/Shop-Online/513/Blackmores",
        "http://www.chemistwarehouse.hk/Shop-Online/513/Blackmores?page=2",
        "http://www.chemistwarehouse.hk/Shop-Online/513/Blackmores?page=3",
        "http://www.chemistwarehouse.hk/Shop-Online/513/Blackmores?page=4",
        "http://www.chemistwarehouse.hk/Shop-Online/513/Blackmores?page=5",
        "http://www.chemistwarehouse.hk/Shop-Online/513/Blackmores?page=6",
        "http://www.chemistwarehouse.hk/Shop-Online/513/Blackmores?page=7",

        "http://www.chemistwarehouse.hk/Shop-Online/660/Nature-s-Way",
        "http://www.chemistwarehouse.hk/Shop-Online/660/Nature-s-Way?page=2",
        "http://www.chemistwarehouse.hk/Shop-Online/660/Nature-s-Way?page=3",
        "http://www.chemistwarehouse.hk/Shop-Online/660/Nature-s-Way?page=4",

        "http://www.chemistwarehouse.hk/Shop-Online/722/Healthy-Care",
        "http://www.chemistwarehouse.hk/Shop-Online/722/Healthy-Care?page=2",
        "http://www.chemistwarehouse.hk/Shop-Online/722/Healthy-Care?page=3",
        "http://www.chemistwarehouse.hk/Shop-Online/722/Healthy-Care?page=4",
        "http://www.chemistwarehouse.hk/Shop-Online/722/Healthy-Care?page=5",

        "http://www.chemistwarehouse.hk/Shop-Online/2128/Bio-Island"
    ]

    def parse(self, response):
        product_container = response.selector.xpath('//a[@class="product-container"]').getall()
        
        with open("product_container.txt","a+",encoding="utf-8") as file:
            file.write(str(product_container)+"\n")
            file.close()
        # with open("pricesv.txt","w") as file:
        #     file.write(str(type(pricesv)))
        #     file.write(str(pricesv))
        #     file.close()

        product_list = []
        p1 = r"(?<=title=\")[\s\w']*"
        pattern1 = re.compile(p1)

        p2 = r"(?<=<span class=\"Price\">\$).\d*.\d*"
        pattern2 = re.compile(p2)

        p3 = r"(?<=<span class=\"Save\">)[\s\w]*.*[\s\w]*(?=</span>)"
        pattern3 = re.compile(p3)

        ps = r"(?<=\$)[\d.]*"
        patterns = re.compile(ps)

        for item in product_container:
            name = re.search(pattern1,item)
            price = re.search(pattern2,item)
            save = re.search(pattern3,item)

            if name:
                name_item = name.group(0)
                # with open("name_space.txt","a+",encoding = "utf-8") as file:
                #     file.write(str(name_item)+"\n")
                #     file.close()

                price_item = price.group(0)
                # with open("price_space.txt","a+") as file:
                #     file.write(str(price_item)+"\n")
                #     file.close()        

                if save:
                    save_item = save.group(0)
                    with open("save_list.txt","a+",encoding="utf-8") as file:
                        file.write(save_item+"\n")
                    save_item = re.search(patterns,save_item).group(0)
                    
                    # save_item.strip("$")
                    discount_item = '%.2f' % (float(price_item) / (float(price_item) + float(save_item)))
                else:
                    discount_item = "1"
                
                price_item_cny = '%.2f' % (float(price_item) * rate_res )
                product_list.append([name_item,price_item,price_item_cny,discount_item])
            else:
                pass
        with open("res_tmp.txt", "a+",encoding="utf-8") as b:
            for item in product_list:
                b.writelines(str(item) + '\n')





        # for j in price_split_list:
        #     price = re.search(pattern2, j)
        #     price_res_lst.append(price.group(0))

        # for j in pricesv:
        #     price = re.search(pattern2, j)
        #     if price:
        #         price = price.group(0)
        #         price_res_lst.append(price)
        #         price_item = float(price)
        #     else:
        #         price_item = 0

        #     # u = i.split('class="Price">')
        #     # price_item = float(j.split('\n')[0][1:])
        #     if 'class="Save"' in j:
        #         save_item = re.search(pattern3, j)
        #         save_item = float(save_item.group(0).strip().strip("$"))
        #         discount = '%.2f' % (price_item / (price_item + save_item))
        #         discount_res_lst.append(discount)

        #         org_price = str(price_item + save_item)
        #         org_price_res_lst.append(org_price)
        #     else:
        #         discount_res_lst.append("1")
        
        # with open("res_tmp.txt", "a+") as b:
        #     for k in range(len(name_res_lst)):
        #         b.writelines(name_res_lst[k] + ', '+price_res_lst[k].split(' ')[0] + ', ' +
        #                         str((float(price_res_lst[k].split(' ')[0])) * (rate_res + 0.3))
        #                         + ', ' + str(discount_res_lst[k]) + '\n')


