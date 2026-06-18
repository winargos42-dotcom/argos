---
argos_import: project_file
source_path: hf-harrier/README.md
source_abs: F:\debug\argoss\hf-harrier\README.md
source_ext: .md
source_sha256: 4395e6f0580dcb068276f2b6377200c8a41b412eae662c0e24f3f199ca14b1de
text_sha256: 1f814f6b440fca7a948fb159ccaabc8d9864446b6dd28a116e24aa4758c1790d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# README.md

- Source: `hf-harrier/README.md`
- Extract: `text`
- SHA256: `4395e6f0580dcb068276f2b6377200c8a41b412eae662c0e24f3f199ca14b1de`

## Content

---
title: Sentence Transformers All MiniLM L6 V2
emoji: 🌖
colorFrom: green
colorTo: pink
sdk: docker
pinned: false
license: apache-2.0
short_description: ARGOSSS
hf_oauth: true
hf_oauth_scopes:
- inference-api
---

To get started working with quarto we recommend you first [install quarto](https://quarto.org/docs/get-started/) locally so that you can render the site without Docker.
We also recommend the [Quarto VS Code Extension](https://marketplace.visualstudio.com/items?itemName=quarto.quarto) which provides syntax highlighting, code completion, a preview button and more.

The quarto source is located in `src` and you can preview the site with:

```
quarto preview src
```

A web browser should open up with a live preview of the site.

## Making changes

The `src/_quarto.yml` contains the site-level configuration for the quarto website and tells quarto which files to render, and how they should be organized.
For example if you wanted to modify the [site navigation](https://quarto.org/docs/reference/site-navigation.html) you should modify this file.

Quarto can render markdown, ipynb, and .qmd files, and you can mix formats in a single document.

## Executing code

One of the main virtues of Quarto is that it lets you combine code and text in a single document.
By default if you include a code chunk in your document, Quarto will execute that code and include the output in the rendered document.
This is great for reproducibility and for creating documents that are always up-to-date.

```{python}
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data
tips = sns.load_dataset("tips")

# Create a seaborn plot
sns.set_style("whitegrid")
g = sns.lmplot(x="total_bill", y="tip", data=tips, aspect=2)
g = (g.set_axis_labels("Total bill (USD)", "Tip").set(xlim=(0, 60), ylim=(0, 12)))

plt.title("Tip by Total Bill")
plt.show()
```

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
