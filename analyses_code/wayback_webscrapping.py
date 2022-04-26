try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print('Import BeautifulSoup: conda install -c anaconda beautifulsoup4')
import requests
import pandas as pd


class Waybackmachine:
    def __init__(self,url):
        self.url = url

    def get_html(self,date:str):
        self.full_url = 'http://web.archive.org/web/'+date+'/'+self.url
        website = requests.get(self.full_url)
        website_html = BeautifulSoup(website.content,'html.parser')
        return website_html
    
    def look_for_table(self,website_html,caption_text:str):
        for caption in website_html.find_all('caption'):
            if caption_text in caption.get_text():
                table = caption.find_parent()
                return table
    
    def save_table(self,table,date):
        pretty_table = pd.read_html(table.prettify())
        pretty_table = pretty_table[0]
        pretty_table['date'] = date
        return pretty_table
    
    def get_date_range(self,start,end):
        all_dates = pd.date_range(start,end,freq='D').strftime('%Y%m%d')
        self.all_dates = all_dates.to_list()

    