import requests
import bs4
from collections import defaultdict


adj = defaultdict(list)

def build_graph(source_url, level):
    if level == 0:
        return

    data = requests.get(source_url)
    # print('Scraping url = ', source_url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')

    # Find the unique Wikipedia urls in this page.
    unique_links = set()

    for link in soup.select("a"):
        if 'href' in link.attrs:
            if link['href'][:6] == "/wiki/":  # This check ensures that we are only checking for Wikipedia urls
                unique_links.add("https://en.wikipedia.org" + link['href'])

    # Add the urls in the adjacency list.
    for link in unique_links:
        adj[source_url].append(link)

    # For each url, scrape the page and build the graph recursively until we reach 'level' number of levels.
    for url in unique_links:
        build_graph(url, level-1)

def dfs(u, dest_url, visited):
    if u == dest_url:
        return True

    # Mark this vertex as visited.
    visited[u] = True

    for v in adj[u]:
        if v not in visited or visited[v] is False:
            if dfs(v, dest_url, visited):
                return True

    visited[u] = False
    return False

def find_path(source_url, dest_url) -> bool:
    visited = defaultdict(bool)
    return dfs(source_url, dest_url, visited)


if __name__ == "__main__":
    SOURCE_URL = 'https://en.wikipedia.org/wiki/Open-source_software'
    DESTINATION_URL = 'https://en.wikipedia.org/wiki/Mitchell_Baker'
    LEVELS = 2

    # Build the graph.
    build_graph(SOURCE_URL, LEVELS)

    is_found = find_path(SOURCE_URL, DESTINATION_URL)

    print('is_found = ', is_found)

