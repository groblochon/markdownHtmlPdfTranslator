#!/usr/bin/env node
// yarn add @google-cloud/translate marked turndown gray-matter uuid prettier google-translate-api

// const translate = require("google-translate-api");
const translate = require('@iamtraction/google-translate');
const { TranslationServiceClient } = require("@google-cloud/translate");
const fs = require("fs");
const path = require("path");
const { marked } = require("marked");
const matter = require("gray-matter");
const TurndownService = require("turndown");
const { v4: uuidv4 } = require("uuid");
const prettier = require("prettier");

//#### Config ####
const TARGET_LANGUAGES = ["en", "zh-CN", "zh-TW"];
//#################

const PROJECT_ID = "xxxxxx";
const LOCATION = "global";
const PARENT = `projects/${PROJECT_ID}/locations/${LOCATION}`;
async function freeTranslate(text, fromLanguage, toLanguage, contentType = "text/plain") {
  try {
    const { text: translatedText } = await translate(text, {
      from: fromLanguage,
      to: toLanguage,
    });
    return translatedText;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}
async function chargedTranslate(text, fromLanguage, toLanguage, contentType = "text/plain") {
  const translationClient = new TranslationServiceClient();
  const request = {
    parent: PARENT,
    contents: [text],
    mimeType: contentType, // Supported formats: 'text/plain' or 'text/html'
    sourceLanguageCode: fromLanguage,
    targetLanguageCode: toLanguage,
  };

  try {
    const [response] = await translationClient.translateText(request);
    return response.translations[0].translatedText;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

class Translator {
  static get CHARGED() {
    return chargedTranslate;
  }
  static get FREE() {
    return freeTranslate;
  }
}

const TRANSLATOR = Translator.FREE;

async function translateMd(filePath) {
  console.log(`\nTranslating ${filePath}...`);

  // Read the file and parse the frontmatter
  const fileContent = fs.readFileSync(filePath, "utf8");
  const post = matter(fileContent);

  if (!post.data.src_language) {
    console.log(`\n${filePath}:\n\tNo src_language found, skip.`);
    return;
  }

  const srcLanguage = post.data.src_language;
  const targetLanguages = TARGET_LANGUAGES.filter(
    (lang) => lang.toLowerCase() !== srcLanguage.toLowerCase()
  );

  // Save the original file
  if (TARGET_LANGUAGES.includes(srcLanguage)) {
    const originalFilePath = getOutputFileName(filePath, srcLanguage);
    fs.copyFileSync(filePath, originalFilePath);
  }

  const originTitle = post.data.title;
  const originContent = post.content;

  // Translate to other languages
  for (const lang of targetLanguages) {
    // Translate title
    post.data.title = await TRANSLATOR(originTitle, srcLanguage, lang, "text/plain");

    // Add translated description
    const translatedDesc = `*(This essay is translated from ${srcLanguage})*\n\n`;

    // Translate content
    post.content = translatedDesc + (await translateContent(originContent, srcLanguage, lang));

    const newPath = getOutputFileName(filePath, lang);
    fs.writeFileSync(newPath, matter.stringify(post));
    console.log(`\t${newPath} created.`);
  }

  console.log(`\n${filePath}:\n\tTranslated from ${srcLanguage} to ${targetLanguages}.`);
}

function extractCodeBlocks(mdContent) {
  const uniquePlaceholder = uuidv4(); // Replace with unique identifier
  const pattern = /(```.*?```)/gs;
  const codeBlocks = mdContent.match(pattern);
  const textWithoutCode = mdContent.replace(pattern, uniquePlaceholder);
  return { textWithoutCode, codeBlocks, uniquePlaceholder };
}

function reinsertCodeBlocks(translatedText, codeBlocks, placeholder) {
  let result = translatedText;
  codeBlocks.forEach((codeBlock) => {
    result = result.replace(placeholder, codeBlock);
  });
  return result;
}

async function translateContent(content, fromLanguage, toLanguage) {
  const { textWithoutCode, codeBlocks, uniquePlaceholder } = extractCodeBlocks(content);

  // Convert Markdown to HTML
  const htmlContent = marked(textWithoutCode);

  // Translate the HTML content
  const translatedHtmlContent = await TRANSLATOR(
    htmlContent,
    fromLanguage,
    toLanguage,
    "text/html"
  );

  // Convert HTML back to Markdown
  const turndownService = new TurndownService({
    headingStyle: "atx",
    bulletListMarker: "-",
    emDelimiter: "*",
    strongDelimiter: "**",
    codeBlockStyle: "fenced",
  });
  const mdWithoutCode = turndownService.turndown(translatedHtmlContent);

  // Reinsert code blocks
  const mdContent = reinsertCodeBlocks(mdWithoutCode, codeBlocks, uniquePlaceholder);
  // Format the Markdown text
  const formattedText = prettier.format(mdContent, {
    parser: "markdown", // Specify the parser
    // Other Prettier options can go here (e.g., printWidth, tabWidth)
  });
  return formattedText;
}

function getOutputFileName(filepath, targetLanguage) {
  const directory = path.dirname(filepath);
  const filename = path.basename(filepath);
  const ext = path.extname(filepath);
  const baseName = path.basename(filepath, ext);

  // Check if the page bundle directory exists
  const bundleDir = path.join(directory, baseName);
  if (fs.existsSync(bundleDir) && fs.statSync(bundleDir).isDirectory()) {
    return path.join(bundleDir, `index.${targetLanguage.toLowerCase()}${ext}`);
  } else {
    return path.join(directory, `${baseName}.${targetLanguage.toLowerCase()}${ext}`);
  }
}

// How to use:
// 1. Translate one file
const file = "demo/example.md";
// translateMd(file)
//   .then(() => console.log("done"))
//   .catch((err) => console.error(err));

async function translateHello() {
  const res = await freeTranslate("Hello", "en", "zh-CN");
  console.log(res);
}

translateHello();
