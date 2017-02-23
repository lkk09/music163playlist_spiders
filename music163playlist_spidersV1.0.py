#!/usr/bin/python3


import requests,re,time,xlwt
from bs4 import BeautifulSoup


class music163(object):
    Headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    MianUrl="http://music.163.com"
    Data=[]



    def Dispatch(self):
        #爬虫调度器
        workbook = xlwt.Workbook()

        data=self.UrlManager()
        for i in data:
            url=self.MianUrl+i["href"]
            self.Downloader(url)
            self.DataStore(workbook,i["data-cat"])
        workbook.save(time.strftime("%Y-%m-%d", time.localtime())  +"_music163.xls")



    def DataStore(self,workbook,name):
        #数据存储器

        name=str(name).replace("/","-") #替换非法字符.
        sheet = workbook.add_sheet(name)
        sheet.write(0, 0, 'Title')
        sheet.write(0, 1, 'Url')
        sheet.write(0, 2, 'Creator')
        sheet.write(0, 3, 'CreatorUrl')
        sheet.write(0, 4, 'Paly')
        for i in range(len(self.Data)):

            sheet.write(i+1, 0, self.Data[i]['Title'])
            sheet.write(i+1, 1, self.Data[i]['Url'])
            sheet.write(i+1, 2, self.Data[i]['Creator'])
            sheet.write(i+1, 3, self.Data[i]['CreatorUrl'])
            sheet.write(i+1, 4, self.Data[i]['Paly'])




        self.Data = []

    def UrlManager(self):
        #url 管理器
        url="http://music.163.com/discover/playlist/"
        r=requests.get(url=url,headers=self.Headers)
        if r.status_code == 200:
            soup=BeautifulSoup(r.text,"lxml")
            data=soup.find_all("a",{"class":"s-fc1"})
            return data




    def Downloader(self,url):
        #url 解析器
        r=requests.get(url,headers=self.Headers)
        print(url,r.status_code)
        if r.status_code==200:
            soup = BeautifulSoup(r.text, "lxml")
            #解析网页
            ul=soup.find("ul",{"class":"m-cvrlst f-cb"})
            li=ul.find_all("li")
            for i in li:
                PageData = {}
                PageData["Title"] = i.p.a.text
                PageData['Url'] = self.MianUrl + i.p.a["href"]
                Creator = i.find("a", {"class": "nm nm-icn f-thide s-fc3"})
                PageData["Creator"] = Creator.text
                PageData['CreatorUrl'] = self.MianUrl + Creator["href"]
                Paly = i.find("span", {"class": "nb"})
                PageData["Paly"] = Paly.text
                self.Data.append(PageData)





            #获取下一页的url
            nextPage=soup.find("a",{"class":"zbtn znxt"})
            if nextPage is not None:
                url=self.MianUrl+nextPage["href"]
                self.Downloader(url)
            else:
                return




if __name__ == "__main__":
    musice163spider=music163()
    musice163spider.Dispatch()
