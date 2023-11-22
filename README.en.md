---
src_language: "en"
---

# md-translate

Translate markdown file, like from `eng` to `zh-CN`. Code blocks will not be translated.

[简体中文](README.zh-cn.md) | [繁體中文](README.zh-tw.md)

## How to use?

You can use the python scripts to create your own scripts. My personal website [haroldgao.com](https://haroldgao.com) use this python version to translate my blogs to different languages.

### Python version

1. Open the [translate.py](src/python/translate.py) file;
2. Install all the dependent libs: `pip3 install python-frontmatter markdown2 markdownify translators`;
3. Change the `file` value in the script to your file path;
4. Run the python code by `python3 src/python/translate.py`

Default python config use the `Translator.FREE` which depends on the `translators` lib. It is a free non-official Google Translate lib. If you want to use a more accurate Google Translate service, you should config your own [Authenticate to Cloud Translation](https://cloud.google.com/translate/docs/authentication) and then use the `Translator.CHARGED`.


## How does it work?

Markdown has some specific marks which may be mistakenly translated. So this translation works by transform markdown to html and translate html content using Google Translate API.
