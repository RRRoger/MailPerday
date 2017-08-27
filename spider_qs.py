# -*- coding: utf-8 -*-  
import urllib2  
import re  
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

class QiuBai():  
    def getPage(self, pageIndex):  
        try:  
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex) 
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'  
            request = urllib2.Request(url, headers = {'User-Agent': user_agent})  
            response = urllib2.urlopen(request)  
            pageCode = response.read().decode('utf-8')
            return pageCode  
        except urllib2.URLError, e:  
            if hasattr(e, "reason"):  
                print u"连接糗事百科失败，错误原因", e.reason  
                return None

    def getPageItems(self, pageIndex):  
        pageCode = self.getPage(pageIndex)  
        if not pageCode:  
            print "页面加载失败。。。"  
            return None  
        pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?"content">(.*?)</div>.*?number">(.*?)</.*?number">(.*?)</.',re.S)  
        items = re.findall(pattern, pageCode)  
        pageStories = []  
        for item in items:  
            replaceBR = re.compile('<br/>')  
            text = re.sub(replaceBR,"\n",item[1])
            if len(text) > 100:
                pageStories.append(text)
            # pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])  
        return pageStories

    def get_beautiful_html(self):
        css_txt = """
            <style type="text/css">
                span {   
                    text-indent:2em;
                    font: .8em Arial, Tahoma, Verdana;
                    background: #fff url(../images/bg.gif) repeat-x; 
                    color: #777;
                }
            </style>
        """
        pageStories = self.getPageItems(1)
        body = "<br/><br/><br/>".join(pageStories)
        return css_txt + body



