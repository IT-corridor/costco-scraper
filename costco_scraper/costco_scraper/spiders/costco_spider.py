import re
import scrapy
import requests
import json

from scrapy.selector import Selector


class CostcoSpider(scrapy.Spider):
    name = "costco"

    header = {
            'Host': 'www.costco.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.costco.com/',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
            'Cookie': 'hl_p=2afe8118-2ddc-4668-a5f5-69ecb4e174b4; AMCVS_97B21CFE5329614E0A490D45%40AdobeOrg=1; AMCV_97B21CFE5329614E0A490D45%40AdobeOrg=-1330315163%7CMCIDTS%7C17225%7CMCMID%7C46504056737436331013923092520674821883%7CMCAAMLH-1488841099%7C7%7CMCAAMB-1488841099%7CcIBAx_aQzFEHcPoEv0GwcQ%7CMCOPTOUT-1488243499s%7CNONE%7CMCAID%7CNONE; spid=41696B99-29B7-4AD4-9931-B82044AB8A5F; s=undefined; WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=ZzphjJ5imwc2khIEaUZZv0GHfmo%3d%0a%3b2017%2d02%2d27+15%3a02%3a09%2e872%5f1488236522430%2d140425%5f10301%5f%2d1002%2c%2d1%2cUSD%5f10301; WC_ACTIVEPOINTER=%2d1%2c10301; WC_USERACTIVITY_-1002=%2d1002%2c10301%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2chAev4P5zVpKYL3uQt4tYs30fIWMchuamGtyK1WNYKb2jYMWZGJ9H7STR3Y2NkIUcfEOR8AMfM6qq%0aZw8qbZRzSHUgbTDoYoVDUTvJ7HiJHuTm3sISf%2fSwjEviTrOCorTrAYHtSGojI5wQ%2fGDQ7WHFXpeq%0aaS1IumBdtU2Zy9mOvHovP3g%2fURy3YoeNgq3cxb1ODQW11DsPxrdzc0JoVchRMg%3d%3d; WC_GENERIC_ACTIVITYDATA=[4998293655%3atrue%3afalse%3a0%3a1dcjlbTjxYw009tqNW4xMIU9ltI%3d][com.ibm.commerce.context.audit.AuditContext|1488236522430%2d140425][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|%2d1%26USD%26%2d1%26USD][com.ibm.commerce.catalog.businesscontext.CatalogContext|10701%26null%26false%26false%26false][com.ibm.commerce.context.base.BaseContext|10301%26%2d1002%26%2d1002%26%2d1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000001002%264000000000000001002%26null%26%2d2000%26null%26null%26null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; BVImplmain_site=2070; BVBRANDID=6aff88e1-f1c9-422b-8f03-313ffe200d13; BVBRANDSID=1b0695d7-c7ce-44ea-a769-8b481d79316a; C_CLIENT_SESSION_ID=11da9079-1d04-4210-b3ed-1b2eafc3d836; JSESSIONID=0000luqPhp9_HS7gq3P-MRwj2iF:175b17ndl; WC_AUTHENTICATION_-1002=%2d1002%2c5M9R2fZEDWOZ1d8MBwy40LOFIV0%3d; ak_bmsc=08A485079047F511CFFD694EDB36178ACDB1473DD56900000AAFB458C8FD7240~plUYMxh+v7XvPGbykquoO75LNkvWcN+wuNudPEDCpz9JLZXa6wVMaFo6NRvGRBrDne2FQIkprFb4GVcYkzfMNsj6A7OezPdlitVqG6ZooyhwI8YiDrMgv5f0tVvYXbjQy0UPA1e8eZbuPjXwsuzpU3oqYxJnJz5iKg60i2TZ0xE5abD+cr75/dtGOfcmOIJLnUsJffIP0Pzb+8oeZ536uK/g==; s_sq=%5B%5BB%5D%5D; s_cc=true; sp_ssid=1488237818564; rr_rcs=eF4FwbsNgDAMBcAmFbs8hO34twFrhIRIFHTA_NyV5f6ea6xMBKoRLB5sqQEzgMrbd7JsxxCFnVNQfSa6k6KmWtuceHb_AWW8EUU'
        }

    def start_requests(self):
        categories = [
            # 'alcohol-monitors',
            # 'automatic-defibrillator',
            # 'blood-pressure-health-monitors',
            # 'electrical-muscle-stimulation',
            # 'family-planning',
            # 'home-health-care-first-aid',
            # 'hot-cold-therapy',
            # 'light-therapy',
            # 'usb-flash-drives',
            # '70-inch-tvs-and-above'
            # 'hd-ip-nvr-security-systems'
            # 'all-rings',
            # 'french-door-refrigerators',
            # 'motor-oil',
            'furniture'
        ]

        return [scrapy.Request('https://www.costco.com/{}.html'.format(item), headers=self.header, callback=self.parse) for item in categories]

    def parse(self, response):
        products = response.css('div.product')
        cates = response.css('div.categoryclist div.col-md-3 a::attr(href)').extract()

        if products:
            for product in products:
                detail = product.css('a.thumbnail::attr(href)').extract_first()
                price = product.css('div.price::text').extract_first()
                rating = product.xpath(".//meta[@itemprop='ratingValue']/@content").extract_first()
                reviewCount = product.xpath(".//meta[@itemprop='reviewCount']/@content").extract_first()
                promo = product.css('p.promo::text').extract_first()
                
                if detail:
                    request = scrapy.Request(detail, headers=self.header, callback=self.detail)
                    request.meta['price'] = price
                    request.meta['rating'] = rating
                    request.meta['promo'] = promo
                    request.meta['reviewCount'] = reviewCount
                    yield request
        else:
            for url in cates:
                yield scrapy.Request(url, headers=self.header, callback=self.parse)


    def detail(self, response):
        sel = Selector(response)
        pid = response.url[-14:-5]
        url = 'https://scontent.webcollage.net/costco/power-page?ird=true&channel-product-id=' + pid
       
        quantity = re.search(r'\s*"maxQty" : "(.+?)",',response.body)
        quantity = quantity.group(1) if quantity else '0'
        min_quantity = re.search(r'\s*"minQty" : "(.+?)",',response.body)
        min_quantity = min_quantity.group(1) if min_quantity else '0'

        if int(quantity) == 9999:
            quantity = self.get_real_quantity({
                'ajaxFlag': True,
                'actionType': sel.xpath("//input[@name='actionType']/@value").extract_first(),
                'backURL': sel.xpath("//input[@name='backURL']/@value").extract_first(),
                'catalogId': sel.xpath("//input[@name='catalogId']/@value").extract_first(),
                'langId': sel.xpath("//input[@name='langId']/@value").extract_first(),
                'storeId': sel.xpath("//input[@name='storeId']/@value").extract_first(),
                'authToken': sel.xpath("//input[@name='authToken']/@value").extract_first(),
                'productBeanId': sel.xpath("//input[@name='productBeanId']/@value").extract_first(),
                'categoryId': sel.xpath("//input[@name='categoryId']/@value").extract_first(),
                'catEntryId': sel.xpath("//input[@name='catEntryId']/@value").extract_first(),
                'addedItem': sel.xpath("//input[@name='addedItem']/@value").extract_first(),
                'catalogEntryId_1': sel.xpath("//input[@name='catEntryId']/@value").extract_first(),
                'quantity': 9999,
                'quantity_1': 9999
            })

        des_key = response.css('div.product-info-specs li span::text').extract()
        des_val = response.css('div.product-info-specs li::text').extract()
        description = self.get_description(des_key, des_val)
        special = sel.xpath("//div[@class='product-info-description']/div[contains(@style, 'text-align:center;')]/text()").extract_first()

        yield {
            'id': response.css('p.item-number span::attr(data-sku)').extract_first(),
            'title': response.css('h1::text').extract_first(),
            'price': response.meta['price'],
            'picture': sel.xpath("//img[@id='initialProductImage']/@src").extract_first(),
            'rating': response.meta['rating'],
            'review_count': response.meta['reviewCount'],
            'promo': response.meta['promo'],
            'delivery_time': response.css('p.primary-clause::text').extract_first(),
            'bullet_points': '\n'.join(response.css('ul.pdp-features li::text').extract()),
            'details': description,
            'quantity': quantity,
            'min_quantity': min_quantity,
            'special': special
        }        

    def get_description(self, des_key, des_val):
        description = ''
        if des_key:
            des_val = [item.strip() for item in des_val if item.strip()]
            for idx in range(len(des_val)):
                description += '{} {}\n'.format(des_key[idx].strip().encode('utf-8'), 
                                                des_val[idx].strip().encode('utf-8'))
        return description.replace(',', '')

    def get_real_quantity(self, body):
        url = 'https://www.costco.com/AjaxManageShoppingCartCmd'
        header = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'334',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie':'spid=BB039764-30D4-488E-A2DA-3416AB5F90D4; s=undefined; hl_p=ae4eb09f-121c-45cf-a807-78a231307294; WC_SESSION_ESTABLISHED=true; WC_ACTIVEPOINTER=%2d1%2c10301; BVImplmain_site=2070; BVBRANDID=9c062aa4-9478-4cc7-8684-f1c52f41118b; AMCVS_97B21CFE5329614E0A490D45%40AdobeOrg=1; WC_PERSISTENT=1BGhult3vWEtlQhpFPW%2fYyGLB%2f8%3d%0a%3b2017%2d03%2d02+07%3a59%3a56%2e301%5f1487263129490%2d838314%5f10301%5f308580336%2c%2d1%2cUSD%5f10301; WC_USERACTIVITY_308580336=308580336%2c10301%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cNPXKfRraLy80H%2facJBFuHUYe3X6iYFGrmBkLoO8pkRG%2fOKYM0Ow8VkcWzCfYx3%2bjEAxPYsnEhIvv%0aI322SzD41rPlK4uX0SGC1rkdkBuu9JeakMfDdJAgGEeK2LE%2fyrt2aTbJUxqqvmaAn0Xzt3aMHf%2b2%0aY0ZUSc2fxbvQDhb3B%2fsevHlNC4Gi8wDnS%2fIntMBnskY%2bRs1g%2btevRm2Lw5k0Fw%3d%3d; BVBRANDSID=cafd4e57-a4aa-47ec-a502-9c0a0b82318d; rr_rcs=eF4NxrENgDAMBMAmFbs8yju2E2_AGkkQEgUdMD9cdSk9cxvTKqN3WDOBuhB5FP1nHjzoecpyvfe5r0KC2ppWD8shFSEAP2Y1EJs; cartCountCookie=1; lastAddedProductId=169831; s_sq=%5B%5BB%5D%5D; C_CLIENT_SESSION_ID=c1672e8d-e50c-4830-862f-007dbffa13f5; WC_AUTHENTICATION_308580336=308580336%2cerDLv1iRML0kyZxjQKZ7DFQJnno%3d; JSESSIONID=0000AkynmIuDDqCCUolR-UPdrns:163c2eho3; ak_bmsc=5BF67D91DB9A91E1ED5BFFF822ECFF3917C663CF22580000095CB85822E90155~pl5UxYn+5vCqxw2Jd99L1zXHJyj3xUPoeqyk74K1w/HJlcCh3okhDXLL1qHo//44Y1pacZ5iTLrzfDpXpL8+RVq2PiRULQ0Xd+KgQ9ddWhr/MZjcx2Z14dUcxJE3VqOTVDRS7ZzDTapWJxcgG+oaPE9cMs9XtNPc+zcct1iunG/tvDwFO63ibb+skGm8hLaqJ0gW43h8VFh+K3sWiApRspwQ==; sp_ssid=1488477229844; WRUIDAWS=1120658076230015; __CT_Data=gpv=58&apv_59_www33=58&cpv_59_www33=58&rpv_59_www33=58; AMCV_97B21CFE5329614E0A490D45%40AdobeOrg=-1330315163%7CMCIDTS%7C17228%7CMCMID%7C14749491232221946818716045741455311554%7CMCAID%7CNONE%7CMCOPTOUT-1488484459s%7CNONE; s_cc=true',
            'DNT':'1',
            'Host':'www.costco.com',
            'Origin':'https://www.costco.com',
            'Referer':'https://www.costco.com/Round-Brilliant-3.00-ctw-VS2-Clarity%2c-I-Color-Diamond-Platinum-Three-Stone-Ring.product.11043679.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'        
        }

        res = requests.post(url=url, headers=header, data=body)
        try:
            quantity_ = res.json()['orderErrMsgObj']['1']
        except Exception, e:
            print '==============================', res.json()
            if 'errorMessage' in res.json():
                return 0
            return '9999'       # orderErrMsgObj
        quantity = re.search(r'\s*only (.+?) are\s*', quantity_)
        return quantity.group(1) if quantity else '9999'
