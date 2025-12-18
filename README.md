# 🎴 Yu-Gi-Oh! Card Searcher

A Python desktop application built with PyQt5 that interfaces with the YGOProDeck API. It features a custom "Duel Links" inspired UI and an advanced Relay Search algorithm to find cards and their specific support pieces.

## 🚀 Features
- **Relay Search Logic:** Finds the official card name first, then uses that exact string to scan all other card effects for support (e.g., searching "Ra" finds "Ancient Chant").
- (card description/effect searching is currently bugged (help plz)
- **Duel Links Inspired Aesthetic:** High-contrast dark theme with gold and cyan accents.
- **Dynamic Previews:** Displays official card art and detailed stats (ATK/DEF/Level/Type).
- **Auto-Deduplication:** Ensures you don't see the same card twice, even if it matches multiple search criteria.

## 🛠️ Setup
1. Install Python 3.x.
2. Install requirements: `pip install PyQt5 requests`.
3. Ensure `YGOcard.jpeg` is in the project folder.
4. Run: `python YGO.py`.

## 📜 Credits
Data and images provided by [YGOProDeck](https://ygoprodeck.com/).
