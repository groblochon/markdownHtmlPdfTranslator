---
src_language: "en"
---


[English](README.en.md) | [简体中文](README.zh-cn.md) | [繁體中文](README.zh-tw.md)

# md-translate

Translate markdown file, like from `en` to `zh-CN`. Code blocks will not be translated.

## How to use?

You can use the python scripts to create your own scripts. My personal website [haroldgao.com](https://haroldgao.com) use this python version to translate my blogs to different languages.

### Python version

1. Open the [translate.py](src/python/translate.py) file;
2. Install all the dependent libs: 
```bash
pip3 install python-frontmatter markdown2 markdownify translators google-cloud-translate
```
3. Run the python code by `python3 src/python/translate.py {md_file_path|md_dir_path}`

Default python config use the `Translator.FREE` which depends on the `translators` lib. It is a free non-official Google Translate lib. If you want to use a more accurate Google Translate service, you should config your own [Authenticate to Cloud Translation](https://cloud.google.com/translate/docs/authentication) and change the config section in the python scripts.


## How does it work?

Markdown has some specific marks which may be mistakenly translated. So this translation works by transform markdown to html and translate html content using Google Translate API.
