import requests
from bs4 import BeautifulSoup
import difflib
import time

def check_website(url, prev_html):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        new_html = soup.prettify()

        # 差分を計算
        diff = difflib.unified_diff(prev_html.splitlines(keepends=True), new_html.splitlines(keepends=True))
        diff_str = ''.join(diff)

        if diff_str:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] サイト{url}に変更がありました。")
            print(diff_str)
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] サイト{url}に変更はありませんでした。")

        return new_html
    except requests.exceptions.RequestException as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error fetching {url}: {e}")
        return prev_html

if __name__ == '__main__':
    with open('urls.txt', 'r') as f:
        urls = f.read().splitlines()

    prev_htmls = {}
    while True:
        for url in urls:
            prev_htmls[url] = check_website(url, prev_htmls.get(url, ''))
        time.sleep(10)  # 15分 = 900秒
