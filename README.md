---
src_language: "en"
---

[English](README.en.md) | [简体中文](README.zh-cn.md) | [繁體中文](README.zh-tw.md)

# Markdown Translator

Translate markdown file, like from `en` to `zh-CN`. Code blocks will not be translated.

## How to use?

For most users, you can open the web page [mdtranslator.haroldgao.com](https://mdtranslator.haroldgao.com/) to translate your markdown content without any knowledge for programming.

For professional users, you can use the python scripts to create your own scripts. My personal website [haroldgao.com](https://haroldgao.com) use this python version to translate my blogs to different languages.


### 1 Translate markdown content in a web page

[mdtranslator.haroldgao.com](https://mdtranslator.haroldgao.com/):

![Translate markdown content in a web page](demo/web.png)


### 2 Run Python Scripts on terminal

1. Get the [translate.py](src/python/translate.py) file and install all the dependent libs:
```bash
git clone https://github.com/xiangaoole/md-translate.git md_translate
cd md_translate
pip3 install python-frontmatter markdown2 markdownify translators google-cloud-translate
```
2. Run the python code by `python3 src/python/translate.py {md_file_path|md_dir_path}`

Default python config use the `Translator.FREE` which depends on the `translators` lib. It is a free non-official Google Translate lib. If you want to use a more accurate Google Translate service, you should config your own [Authenticate to Cloud Translation](https://cloud.google.com/translate/docs/authentication) and change the config section in the python scripts.

### 3 Use python module in your own python scripts

1. Get the [translate.py](src/python/translate.py) file and install all the dependent libs:
```bash
git clone https://github.com/xiangaoole/md-translate.git md_translate
# All the libs are only tested on python3.9
pip3 install python-frontmatter markdown2 markdownify translators google-cloud-translate
```
2. Import the python module in your python scripts:
```python
from md_translate.src.python.translate import translate_content

translation = translate_content(md_text, source_lang, target_lang)
print(f"Translated text: {translation}")
```

## How does it work?

Markdown has some specific marks which may be mistakenly translated. So this translation works by transform markdown to html and translate html content using Google Translate API.
