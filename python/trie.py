import requests
import bs4
import re

URL = 'https://en.wikipedia.org/wiki/Open-source_software'

class Utilities:
    @staticmethod
    def parse_page(url):
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')

        text = ""
        for para in soup.select("p"):
            text += para.text

        return text

    @staticmethod
    def remove_special_characters(text):
        return re.sub(r'\W+', ' ', text)

class Trie:
    class TrieNode:
        """Structure for each node of the Trie."""
        def __init__(self):
            self.children = {}
            self.is_end = False

    def __init__(self):
        """Initialize Trie."""
        self.root = self.TrieNode()

    def insert(self, word):
        """Insert a word into the trie."""
        curr = self.root

        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = self.TrieNode()
            curr = curr.children[ch]

        curr.is_end = True

    def search(self, word):
        """Search whether a word is present in the Trie or not."""
        curr = self.root

        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]

        return curr.is_end

    def search_prefix(self, prefix):
        """Seach whether this prefix is present in the page or not."""
        curr = self.root

        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]

        return True


if __name__ == "__main__":
    text = Utilities.parse_page(URL)
    words = Utilities.remove_special_characters(text).split()

    # Create a Trie.
    trie = Trie()

    # Add all the words in the trie.
    for word in words:
        print(word),
        trie.insert(word)

    # Search for words in the page.
    while (True):
        search_word = input("Enter a word to search (Ctrl + C to quit): ")
        print("Word is found." if trie.search(search_word) else "Word is not found.")