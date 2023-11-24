---
src_language: en
---

*(This essay is translated from en)*

[English](README.en.md) |[簡體中文](README.zh-cn.md)|[繁體中文](README.zh-tw.md)

# md-翻譯

翻譯 markdown 文件，例如從`en`到`zh-CN` 。程式碼區塊不會被翻譯。

## 如何使用？

您可以使用 python 腳本來建立自己的腳本。我的個人網站[haroldgao.com](https://haroldgao.com)使用這個 python 版本將我的部落格翻譯成不同的語言。

###  Python版本

1. 打開[translate.py](src/python/translate.py)檔；
2. 安裝所有依賴函式庫：
```bash
pip3 install python-frontmatter markdown2 markdownify translators google-cloud-translate
```
3. 透過`python3 src/python/translate.py {md_file_path|md_dir_path}`執行 python 程式碼

預設 python 配置使用`Translator.FREE` ，取決於`translators`庫。它是一個免費的非官方谷歌翻譯庫。如果您想使用更準確的 Google 翻譯服務，您應該設定自己的[雲端翻譯驗證](https://cloud.google.com/translate/docs/authentication)並變更 python 腳本中的設定部分。

## 它是如何運作的？

 Markdown 有一些特定的標記，可能會被錯誤翻譯。因此，此翻譯的工作原理是將 markdown 轉換為 html，並使用 Google Translate API 翻譯 html 內容。