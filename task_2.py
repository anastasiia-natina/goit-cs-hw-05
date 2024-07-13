import threading
import matplotlib.pyplot as plt
import requests
from collections import Counter
from typing import Dict

def download_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Помилка завантаження тексту: {response.status_code}")


def map_reduce_word_frequency(text):

    def mapper(word):
        return word.lower(), 1

    def reducer(word, counts):
        return word, sum(counts)

    words = text.split()
    word_counts = Counter(map(mapper, words))
    return dict(reducer(word, word_counts[word]) for word in word_counts)

def visualize_top_words(word_counts, top_n=10):
    top_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    labels, values = zip(*top_words)

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.xlabel("Слово")
    plt.ylabel("Частота")
    plt.title(f"Топ-{top_n} найчастіше вживаних слів")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def main():
    url = "https://gutenberg.net.au/ebooks01/0100021.txt" 

    try:
        text = download_text(url)
        word_counts = map_reduce_word_frequency(text)
        visualize_top_words(word_counts)
    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()