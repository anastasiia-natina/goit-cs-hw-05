import concurrent.futures
import matplotlib.pyplot as plt
import requests
from collections import Counter
from typing import Dict, List


def download_text(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error downloading text: {response.status_code}")


def map_reduce_word_frequency(text: str) -> Dict[str, int]:
    def mapper(word: str):
        return word.lower(), 1

    def reducer(word: str, counts: List[int]):
        return word, sum(counts)

    words = text.split()
    word_counts = Counter()
    for word in words:
        word_counts.update([mapper(word)])

    return dict(reducer(word, [word_counts[word]]) for word in word_counts)


def visualize_top_words(word_counts: Dict[str, int], top_n=10):
    top_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    labels, values = zip(*top_words)

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.title(f"Top-{top_n} Most Frequently Used Words")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def process_url(url: str) -> Dict[str, int]:
    try:
        text = download_text(url)
        word_counts = map_reduce_word_frequency(text)
        return word_counts
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return {}


def main():
    urls = [
        "https://gutenberg.net.au/ebooks01/0100021.txt"
    ]

    aggregated_word_counts = Counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                word_counts = future.result()
                aggregated_word_counts.update(word_counts)
            except Exception as e:
                print(f"Error processing URL {url}: {e}")

    visualize_top_words(aggregated_word_counts, top_n=10)


if __name__ == "__main__":
    main()