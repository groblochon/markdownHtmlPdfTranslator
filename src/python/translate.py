#!/usr/bin/env python3
# Desc: Translate md in content dir
# -*- coding:utf-8 -
# pip3 install python-frontmatter markdown2 markdownify translators google-cloud-translate

import sys
import random
import frontmatter
import os
import uuid
from enum import Enum
import markdown2 as markdown # markdown -> html
from markdownify import markdownify as html2md # html -> markdown
from google.cloud import translate
import re
import shutil

################################# Config #################################
# translated to these languages
TARGET_LANGUAGES = ['en', 'zh-CN', 'zh-TW']

# src language should be set on markdown file header as 
# ```markdown
# ---
# src_language = 'en'`
# ---
# {markdown Content}
# ```
SRC_LANGUAGE_KEY = 'src_language'

# use charged google translate api or not
IS_CHARGED = False
# for CHARGED google translate api
GOOGLE_TRANSLATE_PROJECT_ID="unique-nebula-402902"

# insert space for chinese to fix CJK markdown parser bug
IS_INSERT_SPACE_FOR_CN = False
IS_USE_ZERO_WIDTH_SPACE = True # if True, use zero width space (for render), else use normal space (for plain text)
###########################################################################

#### Translator ####
class ContentType(Enum):
    TEXT = "text/plain"
    HTML = "text/html"

if not IS_CHARGED:
    import translators as ts

# Use free google translate lib `translators`
def free_translate(text, from_language, to_language, content_type=ContentType.TEXT):
    if content_type == ContentType.TEXT:
        return ts.translate_text(text, 'google', from_language, to_language)
    elif content_type == ContentType.HTML:
        return ts.translate_html(text, 'google', from_language, to_language)
    else:
        raise TypeError("Unknown content type.")


# This google translate api is charged, but it's more accurate than free_translate.
# You should config your 
# https://cloud.google.com/translate/pricing
def charged_translate(text, from_language, to_language, content_type=ContentType.TEXT):
    client = translate.TranslationServiceClient()

    response = client.translate_text(
        request={
            "parent": f"projects/{GOOGLE_TRANSLATE_PROJECT_ID}/locations/global",
            "contents": [text],
            "mime_type": content_type.value, # https://cloud.google.com/translate/docs/supported-formats
            "source_language_code": from_language,
            "target_language_code": to_language,
        }
    )

    return response.translations[0].translated_text


class Translator(Enum):
    FREE = free_translate
    CHARGED = charged_translate

TRANSLATOR = Translator.CHARGED if IS_CHARGED else  Translator.FREE
####################


def remove_translated_files(dir):
    pattern = r"^[^.]+\.[a-zA-Z-]+\.md$"
    for root, dirs, files in os.walk(dir):
        for filename in [file for file in files if re.match(pattern, file)]:
            full_path = os.path.join(root, filename)
            os.remove(full_path)
            print(f"Removing {full_path}...")

def translate_md_in_dir(dir):
    # iterate files in dir which endswith ".md" but not ".*.md"
    pattern = r"^[^.]+\.md$"
    for root, dirs, files in os.walk(dir):
        for filename in [file for file in files if re.match(pattern, file)]:
            if not filename.startswith('.'):
                full_path = os.path.join(root, filename)
                translate_md(full_path)


def translate_md(path):
    print(f"\nTranslating {path}...")
    post = frontmatter.load(path)
    if SRC_LANGUAGE_KEY not in post.metadata:
        print(f"\n{path}:\n\tNo {SRC_LANGUAGE_KEY} found in markdown header, skip.")
        return
    
    src_language = post[SRC_LANGUAGE_KEY] or 'auto'
    target_languages = [lang for lang in TARGET_LANGUAGES if lang.lower() != src_language.lower()]

    # 1. save original file
    if src_language in TARGET_LANGUAGES:
        shutil.copy(path, get_output_file_name(path, src_language))

    # origin_title = post['title']
    origin_content = post.content

    # 2. translate other languages
    for lang in target_languages:
        # translate title
        # post['title'] = TRANSLATOR(origin_title, src_language, lang, ContentType.TEXT)

        # add translated desc
        translated_url = get_translated_url(path, src_language)
        print(f"\t{translated_url}")
        translated_desc = f"*(This essay is translated from [{src_language}]({translated_url} \"Original Essay Link\"))*\n\n"
        # translate content
        post.content = translated_desc + translate_content(origin_content, src_language, lang)

        new_path = get_output_file_name(path, lang)
        frontmatter.dump(post, new_path)
        print(f"\t{new_path} created.")
    
    print(f"\n{path}:\n\tTranslated from {src_language} to {target_languages}.")


def get_translated_url(path, lang: str):
    print(f"\nGetting translated url for {path}...")
    directory, filename = os.path.split(path)
    base_name, ext = os.path.splitext(filename)
    segment = f"{base_name}.{lang.lower()}{ext}"

    return f"{segment}"


def extract_code_blocks(md_content):
    unique_placeholder = str(uuid.uuid4().int) + str(random.randint(1000, 9999)) # Generates a unique identifier
    pattern = re.compile(r'(```.*?```)', re.DOTALL)
    code_blocks = pattern.findall(md_content)
    text_without_code = pattern.sub(unique_placeholder, md_content)
    return text_without_code, code_blocks, unique_placeholder


def reinsert_code_blocks(translated_text: str, code_blocks, placeholder):
    parts = translated_text.split(placeholder)
    result = parts[0]
    for i in range(len(code_blocks)):
        result += "\n" + code_blocks[i] + parts[i + 1]
    return result


def translate_content(content, from_language, to_language):
    text_without_code, code_blocks, placeholder = extract_code_blocks(content)
    html_content = markdown.markdown(text_without_code)
    html_content = TRANSLATOR(html_content, from_language, to_language, ContentType.HTML)
    md_without_code = html2md(html_content, heading_style="ATX", bullets="-", escape_underscores=False, )
    if IS_INSERT_SPACE_FOR_CN and to_language.startswith('zh'):
        md_without_code = insert_space_for_cn(md_without_code)
    md_content = reinsert_code_blocks(md_without_code, code_blocks, placeholder)
    return md_content


def get_output_file_name(filepath: str, target_language: str):
    directory, filename = os.path.split(filepath)
    base_name, ext = os.path.splitext(filename)

    # Check if the page bundle exists, if so, use the index.xxx.md file
    if os.path.isdir(os.path.join(directory, base_name)):
        return os.path.join(directory, base_name, f"index.{target_language.lower()}{ext}")
    else:
        return os.path.join(directory, f'{base_name}.{target_language.lower()}{ext}')

def insert_space_for_cn(md_text):
    # Pattern to match * and ** pairs
    pattern = r"(\*\*?)(.+?)(\1)"
    ZERO_WIDTH_SPACE = "&#8203;"
    space = ZERO_WIDTH_SPACE if IS_USE_ZERO_WIDTH_SPACE else " "

    # Replacement function
    def replace(match):
        start, text, end = match.groups()
        return f"{space}{start}{text}{end}{space}"

    # Replace in the entire text
    return re.sub(pattern, replace, md_text)


# How to use:
# 1. Translate one file
# file = 'demo/example.md'
# translate_md(file)
#
# 2. Translate all files
# content_dir = '/Users/gaoxiang/Public/github/xiangaoole.github.io-tmp/content/post/'
# translate_md_in_dir(content_dir)
#
# 3. Remove translated files
# content_dir = '/Users/gaoxiang/Public/github/xiangaoole.github.io-tmp/content/'
# remove_translated_files(content_dir)

if __name__ == '__main__':
    filename = sys.argv[1]
    # is file or dir
    if os.path.isfile(filename):
        translate_md(filename)
    elif os.path.isdir(filename):
        translate_md_in_dir(filename)
    else:
        print(f"Error: {filename} is not a file or dir.")
        exit(1)