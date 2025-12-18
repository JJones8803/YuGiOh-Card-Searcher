# Modules for project
import sys
import requests as rq
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout,
                             QListWidget, QListWidgetItem) 
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap
import urllib.parse

# --- DUEL LINKS STYLE SHEET ---
DUEL_LINKS_STYLE_SHEET = """
QWidget {
    background-color: #1A1A1A;
    color: #FFFFFF;
    font-family: Arial, sans-serif;
    font-size: 14pt;
}
card_Searcher {
    border: 3px solid #FFD700;
    border-radius: 10px;
    padding: 10px;
}
QLabel {
    color: #FFFFFF;
    background: transparent;
    padding: 5px;
}
#cardLabel { 
    font-size: 18pt;
    font-weight: bold;
    color: #FFD700;
}
QLineEdit {
    background-color: #333333;
    color: #00FFFF;
    border: 2px solid #555555;
    border-radius: 5px;
    padding: 5px;
}
QPushButton {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #444444, stop: 1 #222222);
    color: #FFD700;
    border: 2px solid #FFD700;
    border-radius: 8px;
    padding: 10px 15px;
    font-weight: bold;
}
cardInfoWindow {
    background-color: #111111;
    border: 3px solid #00FFFF;
}
"""

# --- SEARCH RESULTS WINDOW CLASS ---
class searchResultsWindow(QWidget):
    def __init__(self, card_list, parent_searcher):
        super().__init__()
        self.setObjectName("cardInfoWindow") 
        self.setWindowTitle("Search Results")
        self.parent_searcher = parent_searcher
        
        vbox = QVBoxLayout(self)
        title = QLabel(f"Found {len(card_list)} matches (Names followed by Effects):")
        vbox.addWidget(title)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListWidget { background-color: #222; color: #EEE; }")
        
        self.card_data_map = {}
        
        # We NO LONGER sort the whole list alphabetically here, 
        # so we can keep Name matches at the top.
        for card in card_list:
            card_name = card.get('name')
            item = QListWidgetItem(card_name)
            self.list_widget.addItem(item)
            self.card_data_map[card_name] = card

        vbox.addWidget(self.list_widget)
        self.list_widget.itemDoubleClicked.connect(self.openSelectedCard)
        self.resize(450, 550)

    def openSelectedCard(self, item):
        card_data = self.card_data_map.get(item.text())
        self.parent_searcher.displayCardInfoSingle(card_data)

# --- CARD INFO WINDOW CLASS ---
class cardInfoWindow(QWidget):
    def __init__(self, cardData):
        super().__init__()
        self.setObjectName("cardInfoWindow") 
        self.setWindowTitle(cardData.get('name', 'Card Data'))
        
        cardName = cardData.get('name', 'N/A')
        cardType = cardData.get('type', 'N/A')
        cardAttribute = cardData.get('attribute', 'N/A')
        cardRace = cardData.get('race', 'N/A')
        image_url = cardData.get('card_images', [{'image_url': ''}])[0].get('image_url')
        description = cardData.get('desc', 'No description available.')
        
        stats_lines = []
        if 'Monster' in cardType:
            stats_lines.append(f"Card Kind: {cardType} ({cardAttribute})")
            level_or_rank = f"Level: {cardData.get('level', 'N/A')}"
            if 'Link' in cardType: level_or_rank = f"Link: {cardData.get('linkval', 'N/A')}"
            elif 'Xyz' in cardType: level_or_rank = f"Rank: {cardData.get('rank', 'N/A')}"
            stats_lines.append(f"• {level_or_rank}")
            
            atk = cardData.get('atk', 'N/A')
            defense = cardData.get('def', 'N/A')
            atk_disp = '?' if atk == -1 else str(atk)
            def_disp = '?' if defense == -1 else str(defense)
            stats_lines.append(f"• ATK/DEF: {atk_disp}/{def_disp}")
        else:
            stats_lines.append(f"Card Kind: {cardType}")
        
        stats_lines.append(f"• Type: {cardRace}")
        
        layout = QVBoxLayout()
        nameLabel = QLabel(f"<b>{cardName}</b>")
        nameLabel.setAlignment(Qt.AlignCenter)
        statsLabel = QLabel("\n".join(stats_lines))
        statsLabel.setAlignment(Qt.AlignCenter)

        artLabel = QLabel()
        try:
            pixmap = QPixmap()
            imageData = rq.get(image_url).content
            pixmap.loadFromData(imageData)
            artLabel.setPixmap(pixmap.scaled(250, 350, Qt.KeepAspectRatio))
        except: artLabel.setText("Image Error")
        artLabel.setAlignment(Qt.AlignCenter)

        descLabel = QLabel(description)
        descLabel.setWordWrap(True)
        
        layout.addWidget(nameLabel)
        layout.addWidget(statsLabel)
        layout.addWidget(artLabel)
        layout.addWidget(descLabel)
        
        self.setLayout(layout)
        self.adjustSize() 

# --- MAIN CARD SEARCHER CLASS ---
class card_Searcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("card_Searcher")
        self.cardLabel = QLabel("Enter card name: ", self)
        self.cardInput = QLineEdit(self)
        self.getCardButton = QPushButton("Get Card", self)
        self.cardArt = QLabel(self)
        self.cardDescriptionLabel = QLabel(self)
        
        # Load default image
        pixmap = QPixmap("/home/dragonzx/Documents/Coding Projects/YuGiOh Card Searcher/YGOcard.jpeg")
        self.cardArt.setPixmap(pixmap.scaled(150, 225))
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YuGiOh Card Searcher")
        vbox = QVBoxLayout()
        vbox.addWidget(self.cardLabel)
        vbox.addWidget(self.cardInput)
        vbox.addWidget(self.getCardButton)
        vbox.addSpacing(20)
        vbox.addWidget(self.cardArt)
        vbox.addWidget(self.cardDescriptionLabel)
        self.setLayout(vbox)
        
        self.cardLabel.setAlignment(Qt.AlignCenter)
        self.cardInput.setAlignment(Qt.AlignCenter)
        self.cardArt.setAlignment(Qt.AlignCenter)
        self.cardDescriptionLabel.setAlignment(Qt.AlignCenter)
        self.cardLabel.setObjectName("cardLabel")
        
        self.getCardButton.clicked.connect(self.getCardInfo)
        self.cardInput.returnPressed.connect(self.getCardInfo) 

    def getCardInfo(self):
        query = self.cardInput.text().strip()
        if not query: return

        self.cardDescriptionLabel.setText("Searching...") # Visual feedback
        QApplication.processEvents() # Ensure the label updates immediately

        base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?"
        name_results = []
        desc_results = []
        seen_ids = set()

        try:
            # 1. SEARCH NAMES FIRST
            encoded_query = urllib.parse.quote(query)
            res_name = rq.get(f"{base_url}fname={encoded_query}")
            if res_name.status_code == 200:
                data = res_name.json().get("data", [])
                for card in data:
                    if card['id'] not in seen_ids:
                        name_results.append(card)
                        seen_ids.add(card['id'])
                # Alphabetize name results
                name_results.sort(key=lambda x: x['name'])

            # 2. SEARCH DESCRIPTIONS SECOND (Support Search)
            # Find cards that mention the names we just found (Crucial for Ra -> Ancient Chant)
            for card in name_results[:5]: # Only check top 5 name matches for support to save time
                official_name = card['name']
                if query.lower() in official_name.lower():
                    # We use quotes around the name for an exact phrase search in descriptions
                    enc_official = urllib.parse.quote(f'"{official_name}"')
                    res_support = rq.get(f"{base_url}desc={enc_official}")
                    if res_support.status_code == 200:
                        s_data = res_support.json().get("data", [])
                        for s_card in s_data:
                            if s_card['id'] not in seen_ids:
                                desc_results.append(s_card)
                                seen_ids.add(s_card['id'])

            # 3. BROAD DESCRIPTION SEARCH (Fallback for query)
            res_desc = rq.get(f"{base_url}desc={encoded_query}")
            if res_desc.status_code == 200:
                data = res_desc.json().get("data", [])
                for card in data:
                    if card['id'] not in seen_ids:
                        desc_results.append(card)
                        seen_ids.add(card['id'])
            
            # Alphabetize description results
            desc_results.sort(key=lambda x: x['name'])

            self.cardDescriptionLabel.setText("") # Clear feedback
            
            # Combine: Name matches first, then description matches
            final_list = name_results + desc_results
            
            if not final_list:
                self.displayError(f"No results for '{query}'")
            elif len(final_list) == 1:
                self.displayCardInfoSingle(final_list[0])
            else:
                self.showSearchResults(final_list)
                
        except Exception as e:
            self.displayError(f"Search Error: {e}")

    def showSearchResults(self, card_list):
        self.results_window = searchResultsWindow(card_list, self)
        self.results_window.show()

    def displayCardInfoSingle(self, cardData):
        self.infoWindow = cardInfoWindow(cardData) 
        self.infoWindow.show()
            
    def displayError(self, message):
        self.cardDescriptionLabel.setText(message)
        self.cardDescriptionLabel.setStyleSheet("color: #FF5555; font-weight: bold;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DUEL_LINKS_STYLE_SHEET) 
    cardSearcher = card_Searcher()
    cardSearcher.show()
    sys.exit(app.exec_())