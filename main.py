#encoding=utf8

import requests
import json
import re
import webbrowser
from wox import Wox, WoxAPI

class TaobaoSearch(Wox):

    def query(self, key):
        # Proxy settings
        proxies = {}
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
              "http": "http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
              "https": "https://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
            }
        
        # Will get JSONP like this:
        # a({"result":[["supreme 专柜","-0.0913396613357576"],["supreme女款","-0.0835718389527911"],["supreme 拖鞋","-0.13509051105714978"],["supreme手机带","-0.08977411179087814"],["supreme 手机壳","-0.0889726103492413"],["supreme 贴纸","-0.13929491581574951"],["supreme 雷射手机壳","-0.08998385048588592"],["supreme黑色","-0.0840886950226317"],["supreme上衣","-0.1087479730214029"],["supreme钻 手机壳","-0.09439478365334535"]],"tmall":"supreme"})
        req = requests.get("https://suggest.taobao.com/sug?code=utf-8&q=%s&callback=a" % key)

        # Keep what u typed first of line...
        results = [{
            "Title": key, 
            "SubTitle": "search %s directly" % key,
            "IcoPath":"images/taobao.png", 
            "JsonRPCAction": {
                "method": "openUrl", 
                "parameters": ["https://s.taobao.com/search?q=%s" % key]
            }
        }] if key else []

        # Get `result` value using reg
        matched_raw = re.findall(r"\"result\":(\[.+\])", req.text)
        if len(matched_raw) <= 0:
            return results

        # Map to result
        matched = json.loads(matched_raw[0])

        for r in matched:
            if r == key:
                continue
            results.append(self.makeResult(r[0]))

        return results

    def makeResult(self, key):
        return {
            "Title": key, 
            "SubTitle": "suggestted by Taobao",
            "IcoPath":"images/taobao.png", 
            "JsonRPCAction": {
                "method": "openUrl", 
                "parameters": ["https://s.taobao.com/search?q=%s" % key]
            }
        }

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    TaobaoSearch()