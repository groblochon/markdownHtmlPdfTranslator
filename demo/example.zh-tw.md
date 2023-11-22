---
src_language: en
title: 把事情做好：我的收穫
---

*(This essay is translated from en)*

*《Get Things Done》*是大衛艾倫（David Allen）撰寫的一本自助書籍，介紹了安排日常任務的一些基本方法，以便您可以過上富有成效且無壓力的生活。這是我的收穫。

 GTD的工作流程由5個步驟組成（但記住，不需要同時完成所有步驟）：

1. **捕獲**。將所有事情拋諸腦後，並隨時將它們寫到您的**📥收件匣**中。
2. **闡明**。找個時間檢查收件匣中的項目。*是否可行？*如果這些東西只是您可能想做但不是現在的想法，您可以將其留在**🔮 有一天的**清單中。如果它是您其他目標有幫助的材料的參考，請將其收集到您的**📚參考**系統中。
3. **組織起來**。*您的可操作項目是否需要多個步驟？*如果是這樣，請將其轉換為**⚙️專案**並找到第一步來完成它。如果一個動作可以在 2 分鐘內完成，就去做（不考慮其優先順序）。*現在可以進行步驟嗎？*如果是這樣，請將其放入您的**⚡️下**一個待辦事項清單中。或者，在您的**📅日曆**中安排一個未來的時間來完成它或**🤝將**其委託給其他人。
4. **反映**。每週檢查您的**收件匣**、**代表**清單、**下一步**行動，並根據需要重新組織它們。
5. **從事**。從**「下**一個待辦事項」清單中選擇一個待辦事項並立即執行。

![GTD 的程序](https://assets.website-files.com/608aecd1e643ecaa961a7a67/634cd40129d4e1311a6c292a_GTD%2001.png)

讓我們用一些`python`程式碼區塊來測試：

 ```python
import os

def get_output_file_name(filepath: str, target_language: str):
    directory, filename = os.path.split(filepath)
    base_name, ext = os.path.splitext(filename)

    # Check if the page bundle exists, if so, use the index.xxx.md file
    if os.path.isdir(os.path.join(directory, base_name)):
        return os.path.join(directory, base_name, f"index.{target_language.lower()}{ext}")
    else:
        return os.path.join(directory, f'{base_name}.{target_language.lower()}{ext}')

```