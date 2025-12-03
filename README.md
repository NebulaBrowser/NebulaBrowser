# OUR DISCORD COMMUNITY https://discord.gg/uR3gUY8KnK

# NebulaBrowser 🌌

**NebulaBrowser** is a lightweight, minimal web browser built with **Python + PyQt5**, designed as a personal custom browser with a dark interface, simplicity, and control in mind.

> Version: **1.1.0** UPDATE

---

## ✨ Concept

Modern browsers are huge: tons of menus, background services, tracking, extensions — they eat resources and distract.  
NebulaBrowser is meant to be:

- small and understandable;
- a browser you can actually read and modify;
- a convenient tool for YouTube, search and everyday browsing;
- a clean example of a cross-platform PyQt5 application.

---

## 🆕 New Experimental Features (1.1.0)

These are early features that improve NebulaBrowser’s usability, but may not yet be perfectly stable:

- **Extensions menu**  
  Includes:  
  - AdBlock  
  - Auto Dark Mode  
  - YouTube Ad-Skip  
  - x16 Video Speed Mode  

- **YouTube Auto Ad-Skip**
- **Basic AdBlock system**
- **x16 Video Speed toggle for YouTube**

*(may be laggy — we are still working on this)*

---

## 🚀 Features in NebulaBrowser 1.0.0

### Interface & Navigation

- 🧭 Navigation buttons:
  - **←** – go back  
  - **→** – go forward  
  - **⟳** – reload page  
  - **+** – open a new tab (defaults to `https://www.google.com`)
- 📜 Address bar:
  - type full URL or just a domain/query (if it doesn’t start with `http`, `https://` is added automatically)
  - updates automatically when you navigate
- 🧩 Multiple tabs:
  - open several pages at once
  - close tabs via the built-in close button
  - links with `target="_blank"` open in a new tab

### Look & Feel

- 🌑 **Dark theme** by default:
  - dark window, toolbar and tab area
  - light, readable text
- 🎚 Minimal toolbar:
  - only essential buttons and address bar
  - symbols instead of noisy icons and labels

### Web Engine

- ⚙️ Powered by **QtWebEngine** (Chromium-based engine):
  - supports modern HTML5 / CSS3 / JavaScript

### Downloads

- 📥 File downloads:
  - uses the `downloadRequested` callback
  - saves files to the system **Downloads** folder
- 📊 Downloads bar at the bottom:
  - file name
  - progress bar with percentage
  - **Open** button to open the downloaded file
- 📂 Opening downloaded files:
  - uses system default applications via OS file associations

### Profiles & Storage

- 🧩 Browser profile: `NebulaProfile`
  - in-memory HTTP cache (`MemoryHttpCache`)
  - persistent cookies policy enabled
  - sessions/cookies can survive between runs (depending on site restrictions)

### Cross-platform

- 🪟 **Windows**
  - start via `NebulaBrowser.bat` or `python NebulaBrowser.py`
- 🍏 **macOS**
  - start via `./NebulaBrowser.sh` or `python3 NebulaBrowser.py`
- 🐧 **Linux**
  - same as macOS, as long as Python and PyQt are installed

---

## 🧱 Tech Stack

- **Python 3.x**
- **PyQt5**
- **PyQtWebEngine**
- QtWebEngine (Chromium-based)
