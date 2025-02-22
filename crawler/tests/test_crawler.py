import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import crawler_sample
def test_google_search():
    crawler = crawler_sample.GoogleCrawler()
    query = "TSMC Ingas"
    results = crawler.google_search(query)
    assert len(results) > 0

def test_get_source():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    assert response.status_code == 200

def test_html_parser():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    results = soup.findAll("div")
    assert len(results) > 0

def test_scrape_google():
    query = 'https://www.google.com/search?q='+"TSMC Ingas"
    crawler = crawler_sample.GoogleCrawler()
    results = crawler.scrape_google(query)
    assert len(results) > 0


def test_html_getText():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    assert len(orignal_text) > 0


def test_word_count_en():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    result_wordcount = crawler.word_count(orignal_text)
    whitelist = ['TSMC']
    end_result = crawler.get_wordcount_json(whitelist , result_wordcount)
    assert end_result[0]['Count'] > 0


def test_word_count_en_with_applied_materials():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.globenewswire.com/news-release/2022/05/26/2451160/0/en/Applied-Materials-New-Ioniq-PVD-System-Solves-Wiring-Resistance-Challenges-of-2D-Scaling.html'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    result_wordcount = crawler.word_count(orignal_text)
    whitelist = ['Applied Materials']
    end_result = crawler.get_wordcount_json(whitelist , result_wordcount)
    assert end_result[0]['Count'] > 0


def test_word_count_ch():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.techbang.com/posts/95836-applied-materials-introduces-3d-gaa-transistor-technology'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    result_wordcount = crawler.word_count(orignal_text)
    whitelist = ['應用材料']
    end_result = crawler.get_wordcount_json(whitelist , result_wordcount)
    assert end_result[0]['Count'] > 0


def test_word_count_ch_with_applied_materials():
    crawler = crawler_sample.GoogleCrawler()
    target_url = 'https://www.techbang.com/posts/95836-applied-materials-introduces-3d-gaa-transistor-technology'
    response = crawler.get_source(target_url)
    soup = crawler.html_parser(response.text)
    orignal_text = crawler.html_getText(soup)
    result_wordcount = crawler.word_count(orignal_text)
    whitelist = ['Applied Materials']
    end_result = crawler.get_wordcount_json(whitelist , result_wordcount)
    assert end_result[0]['Count'] > 0