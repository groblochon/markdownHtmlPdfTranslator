---
src_language: en
title: 把事情做好：我的收获
---

*(This essay is translated from en)*

*《Get Things Done》*是大卫·艾伦（David Allen）撰写的一本自助书籍，介绍了安排日常任务的一些基本方法，以便您可以过上富有成效且无压力的生活。这是我的收获。

 GTD的工作流程由5个步骤组成（但记住，不需要同时完成所有步骤）：

1. **捕获**。将所有事情抛诸脑后，并随时将它们写到您的**📥收件箱**中。
2. **阐明**。找个时间检查收件箱中的项目。*是否可行？*如果这些东西只是您可能想做但不是现在的一个想法，您可以将其留在**🔮 有一天的**列表中。如果它是对您其他目标有帮助的材料的参考，请将其收集到您的**📚参考**系统中。
3. **组织起来**。*您的可操作项目是否需要多个步骤？*如果是这样，请将其转换为**⚙️项目**并找到第一步来完成它。如果一个动作可以在 2 分钟内完成，就去做（不考虑其优先级）。*现在可以进行步骤吗？*如果是这样，请将其放入您的**⚡️下**一个待办事项列表中。或者，在您的**📅日历**中安排一个未来的时间来完成它或**🤝将**其委托给其他人。
4. **反映**。每周检查您的**收件箱**、**代表**列表、**下一步**行动，并根据需要重新组织它们。
5. **从事**。从**“下**一个待办事项”列表中选择一个待办事项并立即执行。

![GTD 的程序](https://assets.website-files.com/608aecd1e643ecaa961a7a67/634cd40129d4e1311a6c292a_GTD%2001.png)

让我们用一些`python`代码块进行测试：

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