# ECCApp 🀄  
A simple desktop Chinese input helper that lets you look up characters using **Easy Chinese Code (ECC)**. Built with Python, powered by a cleaned ECC dataset, and wrapped in a Tkinter GUI for quick lookup and learning.

<a href="https://github.com/your-username/eccapp" target="_blank">ECCApp Repository</a>

![ECCApp Screenshot](./eccc.JPG)

---

## How It's Made:

**Tech used:** Python, Tkinter, Pandas, NumPy, CSV (ECC dataset)

This project loads an ECC code table from `data.csv` (exported from the original Excel file) and turns it into an interactive input tool.

Under the hood:

- **Data layer (Pandas):**  
  - Reads `data.csv` and keeps only the useful columns:  
    `character`, `voice_code`, `1`, `2`, `3`.  
  - Builds a helper column that concatenates the `1–3` ECC columns so prefix searches are fast.

- **Core ECC lookup logic (NumPy + Pandas):**  
  - When you type a sequence like `hi` or `hiw`, the app:
    - Converts your input into a NumPy array.
    - Scans each row to see if the first N ECC letters match what you typed.
    - If it finds a match, it shows:
      - The **Chinese character**.
      - The corresponding **voice code** (pronunciation helper).
  - If there’s no exact match, it tells you and lets you rely on prefix suggestions.

- **GUI (Tkinter + ttk):**  
  - A clean window with:
    - An **input box** for ECC letters.
    - A **“Submit (Enter)”** button and **“Clear”** button.
    - A **“Results”** area that shows:
      - **Exact Match**: character + voice code.
      - **Prefix Matches**: a list of up to 15 candidate codes and characters that start with your typed prefix.
  - You can:
    - **Double-click** a candidate in the list (or press Enter on it) to select it.
    - Use **“Copy Character”** to send the chosen character to the clipboard.
  - A small **status bar** at the bottom shows how many rows were loaded and which columns are in use.

**Flow in practice:**

1. Start the app with `python ecc.py`.
2. Type ECC letters in the input box.
3. Press **Enter** or click **“Submit”**:
   - If there’s an exact match, the character and voice code appear.
4. Watch the **prefix suggestion list** update live as you type.
5. Double-click a suggestion to fill it and copy the character if needed.

---

## Optimizations  
*(optional)*  

- Precomputed a **prefix column** so prefix search is just a simple `startswith` instead of rebuilding strings every time.
- Fixed the original logic to loop over **rows** (characters) instead of columns, which made matching reliable and easier to debug.
- Limited the prefix suggestion list to **top 15** matches for readability.
- Centralized core ECC logic in a separate function so the GUI code stays cleaner and easier to maintain.
- Added a **status bar** and basic error handling if `data.csv` can’t be loaded.

---

## Lessons Learned:

Working on ECCApp was a good mix of **data handling** and **desktop UI** work:

- Cleaned and reshaped dataset exports (Excel → CSV → filtered DataFrame).
- Saw how a small indexing mistake (looping over columns instead of rows) can completely break matching, and how to track that down with simple tests.
- Learned how to keep GUI code and core logic separate so it’s easier to tweak the algorithm without touching the interface.
- Practiced building a **small but focused tool**: not a full IME with system integration, but a neat helper for learning, testing, and exploring ECC encodings.

---

## 🔗 Other Projects: 

- [🃏 Card Battle Game](https://github.com/Zunaid990/zunaids-card-battle.git) – A fun two-player game using the Deck of Cards API. 
- [🌤️ Weather Now]([https://github.com/Zunaid990/Stopwatch-app.git](https://zunaid990.github.io/Weather-now/)) – A simple weather app that shows current temperature, humidity, and weather conditions.
