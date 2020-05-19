import pdfkit, requests, hashlib, warnings, sys, time, re, base64, binascii, json, os,click
import urllib, pypandoc
import re   

from bs4 import BeautifulSoup  

from distutils.filelist import findall  
from http import cookiejar

class ToPdf():
    def deal(self, url,name,dirname):
        url= url#一篇博客的url
        dir = 'E:\\hnzskj\\政府风险防控项目\\法规1\\'
        confg = pdfkit.configuration(wkhtmltopdf='F:\\soft\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        #这里指定一下wkhtmltopdf的路径，这就是我为啥在前面让记住这个路径
        dir_name = dir+dirname+'\\'
        if os.path.exists(dir_name):
            print(dir_name+'已存在')
        else:
            print(dir_name+'不存在')
            os.makedirs(dir_name)

        print(name+"   下载中....")
        try:
            pdfkit.from_url(url, dir_name +name+'.pdf',configuration=confg)
            pypandoc.convert_file(url,'docx',outputfile=dir_name +name+'.docx')
        except Warning:
            print(name+' 下载错误！'+' sleep 3 秒')
            time.sleep(5)
            print(name+' 再次下载！')
            pdfkit.from_url(url, dir_name +name+'.pdf',configuration=confg)
            print(name+' 下载完成！')
        # from_url这个函数是从url里面获取内容
        # 这有3个参数，第一个是url，第二个是文件名，第三个就是khtmltopdf的路径
        
        #pdfkit.from_file('my.html', 'jmeter_下载文件2.pdf',configuration=confg)
        # from_file这个函数是从文件里面获取内容
        # 这有3个参数，第一个是一个html文件，第二个是文生成的pdf的名字，第三个就是khtmltopdf的路径
        
        html='''
        <div>
        <h1>title</h1>
        <p>content</p>
        </div>
        '''
        #这个html是我从一个页面上拷下来的一段，也可以
        
        #pdfkit.from_string(html, 'jmeter_下载文件3.pdf',configuration=confg)
        # from_file这个函数是从一个字符串里面获取内容
        # 这有3个参数，第一个是一个字符串，第二个是文生成的pdf的名字，第三个就是khtmltopdf的路径      
    def getHttpStatusCode(self,url):
        try:
            request = requests.get(url)
            httpStatusCode = request.status_code
            print(httpStatusCode)
            if httpStatusCode==404:
                return 0
        except requests.exceptions.HTTPError as e:
            return 0

    def spiderHtml(self,start_year,end_year,url):
        print('begin search 法规文件 from '+url)
        page = urllib.request.urlopen(url)
        contents = page.read()
        contents = contents.decode('utf-8')#解决乱码
        soup = BeautifulSoup(contents,"html.parser")  
        fagui_list_name='fagui_list.txt'
        if os.path.exists(fagui_list_name):
            with open(fagui_list_name, "r") as f:
                fagui_list = list(map(lambda x: x.strip(), f.readlines()))
            for tag in soup.find_all('div', class_='con-box'):
                type_name = tag.find('ul').find('div').get_text()
                m_li = tag.findAll("li")
                for li in m_li:
                    current_date = li.find('span').get_text()
                    current_year = int(current_date[0:4])
                    if current_year <= end_year and current_year >=start_year:
                        name = li.find('a').get_text()
                        url = li.find('a').get('href')
                        if name not in fagui_list:
                            self.deal(url,name,type_name)
                            with open(fagui_list_name,"a") as f:
                                f.write(name+"\n")
                        else:
                            print(name+'已存在!')  
        else:
            click.echo(fagui_list_name+' not exist.')
        return 1
    
    def getTypeList(self,typeName):
        if os.path.exists(typeName):
            with open(typeName, "r") as f:
                fagui_list = list(map(lambda x: x.strip(), f.readlines()))
                return fagui_list
        


 

if __name__ == '__main__':
    toPdf = ToPdf()
    timeout = 60
    dir = 'E:\\hnzskj\\政府风险防控项目\\法规\\'
    source_url="https://www.henan.gov.cn/zwgk/fgwj/"
    type_list_name='szf_fagui_type.txt'
    quiet = True
    cookie_path = 'Cookie'
    start_year=2005
    end_year=2020
    type_list = toPdf.getTypeList(type_list_name)
    for type in type_list:
        flag = 1
        url=source_url+type+'/'
        a=0
        while flag == 1:
            url1=url
            if a == 0:
                url1=url+'index.html'
            else:
                url1=url+'index_'+str(a)+'.html'

            flag1 = toPdf.spiderHtml(start_year,end_year,url1)
            flag = flag1
            print('flag = '+str(flag))
            if flag1==0:
                print(url1+'is not exists! end search')

            a = a+1
        
        print(url+' is end')
    


   
   
    
 



       





