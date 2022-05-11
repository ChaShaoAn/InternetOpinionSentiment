import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import MWETokenizer
import paddle
# nltk.download()

class GoogleCrawler():
    
    def __init__(self):
        self.url = 'https://www.google.com/search?q='    
    #  URL 萃取 From Google Search上 , using 第三方套件
    #  https://python-googlesearch.readthedocs.io/en/latest/
    def google_url_search_byOpenSource(query,tbs='qdr:m',num=10):
        array_url = [url for url in search('tsmc', tbs='qdr:m' , num=10)]
        return array_url
    # 網路擷取器
    def get_source(self,url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
    # URL 萃取 From Google Search上
    def scrape_google(self,query):

        response = self.get_source(self.url + query)
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        return links
    
# URL萃取器，有link之外，也有標題
#     qdr:h (past hour)
#     qdr:d (past day)
#     qdr:w (past week)
#     qdr:m (past month)
#     qdr:y (past year)
    def google_search(self,query,timeline='',page='0'):
        url = self.url + query + '&hl=en&tbs={timeline}&start={page}'.format(timeline=timeline,page=page)
        print('[Check][URL] URL : {url}'.format(url=url))
        response = self.get_source(url)
        return self.parse_googleResults(response)
    # Google Search Result Parsing

    def parse_googleResults(self,response):

        css_identifier_result = "tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = "yuRUbf"
        css_identifier_text = "VwiC3b"
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll("div", {"class": css_identifier_result})
        output = []
        for result in results:
            item = {
                'title': result.find(css_identifier_title).get_text(),
                'link': result.find("div", {"class": css_identifier_link}).find(href=True)['href'],
                'text': result.find("div", {"class": css_identifier_text}).get_text()
            }
            output.append(item)
        return output
    
    # 網頁解析器
    def html_parser(self,htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')
        return soup
    # 解析後，取<p>文字
    def html_getText(self,soup):
        orignal_text = ''
        for el in soup.find_all('p'):
            orignal_text += ''.join(el.find_all(text=True))
        return orignal_text
    
    def word_count(self, text):
        text = text.lower()
        if self.is_contains_chinese(text):
            counts = self.word_count_ch(text)
        else:
            counts = self.word_count_en(text)
        return counts
    
    def word_count_en(self, text):
        counts = dict()
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        tokenizer = MWETokenizer([('applied', 'materials'), ('applied', 'material')], separator=' ')
        words = tokenizer.tokenize(words)
        #words = text.replace(',','').split()
        for word in words:
            if word not in stop_words:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        return counts

    def word_count_ch(self, text):
        counts = dict()
        import jieba
        paddle.enable_static()  # 我的版本需要加這個才能work?
        jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
        jieba.load_userdict('config/custom_dict.txt')
        words = jieba.cut(text, cut_all=False)
        # print(", ".join(words))
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        print(text)
        print(counts)
        return counts

    def get_wordcount_json(self, whitelist , dict_data):
        data_array = []
        for i in whitelist:
            if i in dict_data:
                json_data = {
                    'Date' : 'Week1',
                    'Company' : i , 
                    'Count' : dict_data[i]
                }
                data_array.append(json_data)
            else:
                json_data = {
                    'Date' : 'Week1',
                    'Company' : i , 
                    'Count' : 0
                }
                data_array.append(json_data)
        return data_array

    def jsonarray_toexcel(self,data_array):
        df = pd.DataFrame(data=data_array)
        df.to_excel('result.xlsx' , index=False)
        return
    
    def is_contains_chinese(self, strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False
    
if __name__ == "__main__":
    query = "TSMC ASML"
    crawler = GoogleCrawler()
    results = crawler.google_search(query , 'qdr:w' , '10')
    print(results[:3])
    # Target_URL = 'https://taipeitimes.com/News/biz/archives/2022/01/20/2003771688'
    Target_URL = 'https://udn.com/news/story/7240/6046136'  # 測試中文新聞
    response = crawler.get_source(Target_URL)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    print(orignal_text[:100])
    result_wordcount = crawler.word_count(orignal_text)
    result_wordcount
    # whitelist = ['ASML' , 'Intel']
    whitelist = ['asml' , 'intel', '艾司摩爾', '台積電', 'tsmc']
    end_result = crawler.get_wordcount_json(whitelist , result_wordcount)
    print(end_result)
    crawler.jsonarray_toexcel(end_result)
    print('Excel is OK')