---
src_language: en
---

*(This essay is translated from en)*

# md-翻譯

翻譯 markdown 文件，例如從`eng`到`zh-CN` 。程式碼區塊不會被翻譯。

[簡體中文](README.zh-cn.md)|[繁體中文](README.zh-tw.md)

## 如何使用？

您可以使用 python 腳本來建立自己的腳本。我的個人網站[haroldgao.com](https://haroldgao.com)使用這個 python 版本將我的部落格翻譯成不同的語言。

###  Python版本

1. 打開[translate.py](src/python/translate.py)檔；
2. 安裝所有依賴函式庫： `pip3 install python-frontmatter markdown2 markdownify translators` ；
3. 將腳本中的`file`值更改為您的文件路徑；
4. 透過`python3 src/python/translate.py`運行 python 程式碼

預設 python 配置使用`Translator.FREE` ，取決於`translators`庫。它是一個免費的非官方谷歌翻譯庫。如果您想使用更準確的 Google 翻譯服務，您應該設定自己的[Authenticate to Cloud Translation](https://cloud.google.com/translate/docs/authentication) ，然後使用`Translator.CHARGED` 。

## 它是如何運作的？

 Markdown 有一些特定的標記，可能會被錯誤翻譯。因此，此翻譯的工作原理是將 markdown 轉換為 html，並使用 Google Translate API 翻譯 html 內容。