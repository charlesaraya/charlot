# 🌀 Charlot — A Minimalistic Static Site Generator
Charlot is a lightweight, fast, and SEO-friendly static site generator built from scratch in Python. It transforms a folder of Markdown files into a fully functional website using simple templates—no dependencies, no fuss.

## Features
- Converts basic syntax in Markdown files to HTML
- Basic templating with layout support
- Fast build time with clean output
- Generates pages from nested directories
- Built with maintainability and testability in mind

## How It Works
- Write all content in plain Markdown files, and add them to `/content/`.
- Add all static content (.css, images, etc.), and them to `/static/`.
- Add a simple HTML template `template.html` with `{{ Title }}` and `{{ Content }}` placeholders to render the title and gnerated html content of the page.
- Run the generator.
- The static site will be generated.

### Folder Structure

```
.
├── docs/                   # Generated HTML output
├── content/                # Your Markdown files
│   ├── index.md            # Home Page md
│   └── blog/
│       └── cat_post.md
├── static/                 # Your Markdown files
│   ├── index.css           # Style sheet
│   └── images/
│       └── cat.png
├── template.html
├── src/
│   ├── source_code.py      # Source code
│   ├── test_source_code.py # Test source code
│   └── main.py             # Main generator script
│
├── LICENSE
└── README.md
```

### Usage

```
python3 `/src/main.py`

```

### Requirements

Built with standard Python libraries. No external dependencies required.

## What I Learned
This project helped me solidify:

- File I/O operations.
- Markdown parsing.
- Basic templating.
- Working with paths and directory trees.
- Writing clean, modular, and testable Python code.
