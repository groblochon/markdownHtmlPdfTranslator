---
title: "Get Things Done: My Take Away"
src_language: "en"
---

*Get Things Done* is a self-help book written by David Allen, which introduces some basic methods to arrange your daily tasks so that you can live a productive and stressless life. Here are my takeaways.

The workflow of GTD consists of 5 steps (but remember, no need to finished all the steps at the same time):

1. **Capture**. Get all things out of your mind and write down them to your **📥Inbox** at any time.
2. **Clarify**. Find a time to check items in your inbox. *Is it actionable?* If the stuff is just an idea that you might want to do but not now, you can leave it to a **🔮someday** list. If it is a reference to materials helpful to your other goals, collect it to your **📚Reference** system.
3. **Organize**. *Does your actionable item need more than one step?* If so convert it to a **⚙️Project** and find the fist step to do it. If a action can be done within 2 minutes, just do it (without considering its priority). *Does the step can be got about right now?* If so put it into your **⚡️Next** to-do list. Or else, arrange a future time to do it in your **📅Calendar** or **🤝Delegate** it to others.
4. **Reflect**. Review your **Inbox**, **Delegate** list, **Next** actions weekly and reorganize them if needed.
5. **Engage**. Pick one to-do from your **Next** to-do list and do it right now.

![The procedure for GTD](https://assets.website-files.com/608aecd1e643ecaa961a7a67/634cd40129d4e1311a6c292a_GTD%2001.png)

Let's test with some `python` code block:

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

