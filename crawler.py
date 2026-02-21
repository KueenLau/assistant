import json
import re

import requests

# 财经热点：top 接口的 www_www_finance_suda_suda 返回空，改用新浪财经滚动新闻 API
API_URL = "https://roll.finance.sina.com.cn/api/news_list.php"
API_PARAMS = {"num": 50, "offset_num": 0}


def fetch_hot_news():
    """
    获取财经热点新闻
    :return: List[dict] [{title, url, priority}]
    """
    try:
        res = requests.get(API_URL, params=API_PARAMS)
        res.encoding = res.apparent_encoding
        # 接口返回：var jsonData = {...};
        text = res.text.strip()
        match = re.search(r"=\s*(\{.*\})\s*;?\s*$", text, re.DOTALL)
        if not match:
            return []
        data = json.loads(match.group(1))
        news_list = []
        for i, item in enumerate(data.get("list", [])):
            title = item.get("title", "").strip()
            url = item.get("url", "").strip()
            time_val = item.get("time", "0")
            try:
                priority = int(time_val)
            except (ValueError, TypeError):
                priority = 0
            if title and url:
                news_list.append({"title": title, "url": url, "priority": priority})
        news_list.sort(key=lambda x: x["priority"], reverse=True)
        return news_list[:10]
    except Exception as e:
        print("抓取新闻失败:", e)
        return []

if __name__ == '__main__':
    hot_news = fetch_hot_news()
    print('热点新闻排行榜：')
    for idx, item in enumerate(hot_news):
        print(f"{idx + 1}. [{item['title']}]({item['url']}) 财经热度: {item['priority']}")
