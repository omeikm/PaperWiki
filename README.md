# 📚 Representation Learning PaperWiki

A warm, academic-styled personal knowledge base and automated paper wiki dedicated to **Representation Learning** literature. Built with an agent-driven development workflow (`AGENTS.md` & `NOTE_AGENT.md`) and designed for researchers who want both clean aesthetics and efficient note-keeping.

---

## ✨ Key Features

* **Warm Academic Aesthetic:** Designed with a cozy paper-white background (`#FAF8F5`), serif headings for an editorial feel, and soft charcoal text to reduce reading fatigue during long research sessions.
* **Dual-Agent Architecture:**
  * **Research Assistant (`NOTE_AGENT.md`):** Automatically scans PDFs, extracts core insights, and generates structured Markdown notes with key figures.
  * **Frontend Engineer (`AGENTS.md`):** Monitors note changes, renders responsive paper pages, and updates the homepage index incrementally.
* **Micro-Interactions (Vanilla JS + LocalStorage):**
  * 🏷️ **Tag-based Filtering:** Instantly filter papers on the homepage by research tags (e.g., `#Contrastive Learning`, `#NLP`).
  * 📊 **Reading Progress Bar:** Track your reading depth dynamically at the top of each paper page.
  * 🔖 **Reading Status / Mood Badge:** Toggle your digestion state (`🌱 Budding`, `☕ Digesting`, `💡 Inspired`, `🤯 Mind Blown`) saved locally.
  * 📌 **Sticky Note Takeaways:** Custom hand-written sticky note styling for personal research reflections.
* **Modular Codebase:** Clean separation of concerns with modularized JavaScript (`assets/js/`) and reusable CSS design tokens.

---

## 📂 Project Structure

```text
/
├── AGENTS.md                  # Frontend & Sync Agent Specification
├── NOTE_AGENT.md              # Research Note Extraction Agent Specification
├── README.md                  # Project Overview
├── index.html                 # Homepage with tag filtering and paper grid
├── pdfs/                      # Original paper PDF files
├── notes/                     # Markdown raw notes (Provided or Agent-generated)
├── assets/
│   ├── css/
│   │   └── style.css          # Warm Academic design system & sticky-note styles
│   ├── js/                    # Modular JavaScript features
│   │   ├── filter.js          # Homepage tag filtering
│   │   ├── progress.js        # Reading progress bar
│   │   ├── mood-badge.js      # LocalStorage reading status manager
│   │   └── accordion.js       # Section collapsible toggles
│   └── images/                # Extracted paper architecture & experimental figures
└── papers/                    # Rendered standalone HTML paper pages

```

---

## 🤖 Dual-Agent Workflow

This project utilizes a standardized agent specification workflow to ensure 100% consistency and zero-regression incremental updates:

1. **Step 1: Extract Notes (`NOTE_AGENT`)**
Place your downloaded paper PDF into the `pdfs/` folder, then prompt your AI agent using `NOTE_AGENT.md` to automatically generate structured Markdown notes into `notes/`.
2. **Step 2: Sync & Render Web (`AGENTS.md`)**
Prompt your AI agent using `AGENTS.md` to detect changes in `notes/`, render/update the corresponding `papers/*.html` pages, and update the top of the homepage index without altering untouched historical records.

---

## 🚀 Getting Started

1. Clone or open this repository in **VS Code**.
2. Ensure you have the `AGENTS.md` and `NOTE_AGENT.md` files in your root directory.
3. Drop your paper PDFs into `pdfs/` and let the agents handle the rest!
4. Open `index.html` locally or deploy via **GitHub Pages** to enjoy your personal paper wiki.

---

## 📄 License

Note: The MIT License applies only to the code, specifications, and notes in this repository. Original research paper PDFs in the `pdfs/` folder belong to their respective publishers and are excluded. PDFs are not uploading to repo as they can be downloaded by your own.