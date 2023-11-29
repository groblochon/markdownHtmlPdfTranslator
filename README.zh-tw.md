---
src_language: en
---

*(This essay is translated from [en](README.en.md "Original Essay Link"))*

[English](README.en.md) |[簡體中文](README.zh-cn.md)|[繁體中文](README.zh-tw.md)

# md-翻譯

翻譯 markdown 文件，例如從`en`到`zh-CN` 。程式碼區塊不會被翻譯。

## 如何使用？

對於大多數使用者來說，無需任何程式設計知識，您就可以開啟網頁[mdtranslator.haroldgao.com](https://mdtranslator.haroldgao.com/)來翻譯您的 Markdown 內容。

對於專業用戶，您可以使用 python 腳本來建立自己的腳本。我的個人網站[haroldgao.com](https://haroldgao.com)使用這個 python 版本將我的部落格翻譯成不同的語言。

###  1 翻譯網頁中的markdown內容

[mdtranslator.haroldgao.com](https://mdtranslator.haroldgao.com/) ：

![翻譯網頁中的 Markdown 內容](demo/web.png)

###  2 在終端機上運行Python腳本

1. 取得[translate.py](src/python/translate.py)檔並安裝所有依賴函式庫：
```bash
git clone https://github.com/xiangaoole/md-translate.git md_translate
cd md_translate
pip3 install python-frontmatter markdown2 markdownify translators google-cloud-translate
```
2. 透過`python3 src/python/translate.py {md_file_path|md_dir_path}`執行 python 程式碼

預設 python 配置使用`Translator.FREE` ，取決於`translators`庫。它是一個免費的非官方谷歌翻譯庫。如果您想使用更準確的 Google 翻譯服務，您應該設定自己的[雲端翻譯驗證](https://cloud.google.com/translate/docs/authentication)並變更 python 腳本中的設定部分。

###  3 在你自己的python腳本中使用python模組

1. 取得[translate.py](src/python/translate.py)檔並安裝所有依賴函式庫：
```bash
git clone https://github.com/xiangaoole/md-translate.git md_translate
# All the libs are only tested on python3.9
pip3 install python-frontmatter markdown2 markdownify translators google-cloud-translate
```
2. 在 python 腳本中導入 python 模組：
```python
from md_translate.src.python.translate import translate_content

translation = translate_content(md_text, source_lang, target_lang)
print(f"Translated text: {translation}")
```

## 它是如何運作的？

 Markdown 有一些特定的標記，可能會被錯誤翻譯。因此，此翻譯的工作原理是將 markdown 轉換為 html，並使用 Google Translate API 翻譯 html 內容。