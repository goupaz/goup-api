import requests
import bs4


class SegmentTree:
    """
    Constructor.
    Keeps a copy of the nums array provided and invokes the build_tree method.
    """

    def __init__(self, nums: list[int]):
        self.length = len(nums)
        self.tree = [0] * (4 * self.length)
        self.nums = nums

        self.__build_tree(1, 0, self.length - 1)

    """
    Build the segment tree using the nums array provided in the constructor.
    Method is private since external classes don't need to see the implementation.
    Method is invoked by the constructor during object creation.
    """

    def __build_tree(self, node: int, x: int, y: int):
        if (x > y):
            return

        if (x == y):  # Leaf node of the segment tree
            self.tree[node] = self.nums[x]
            return

        self.__build_tree(2 * node, x, (x + y) // 2)
        self.__build_tree(2 * node + 1, (x + y) // 2 + 1, y)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    """
    Updates the segment tree between [L,R] - makes each value equal to val.
    [x,y] is the current window, [L,R] is the window we want to query
    Method is private because external classes don't need to see the implementation.
    """

    def __update_tree(self, node: int, x: int, y: int, L: int, R: int,
                      val: int):  # [x,y] is the current window, [L,R] is the window we want to update
        if x > y or y < L or x > R:
            return

        if x == y:
            self.tree[node] = val
            return

        self.__update_tree(2 * node, x, (x + y) // 2, L, R, val)
        self.__update_tree(2 * node + 1, (x + y) // 2 + 1, y, L, R, val)

        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    """
    Queries the segment tree and finds the sum of [L,R].
    [x,y] is the current window, [L,R] is the window we want to query
    Method is private because external classes don't need to see the implementation.
    """

    def __query_tree(self, node: int, x: int, y: int, L: int, R: int):
        if x > y or y < L or x > R:
            return 0

        if x >= L and y <= R:
            return self.tree[node]

        return self.__query_tree(2 * node, x, (x + y) // 2, L, R) + self.__query_tree(2 * node + 1, (x + y) // 2 + 1, y,
                                                                                      L,
                                                                                      R)

    """
    Public method for querying the sum of [L,R].
    """

    def query(self, L: int, R: int):
        return self.__query_tree(1, 0, self.length - 1, L, R)


"""
Method to scrape the source url, parse the page and find the number of runs scored in each year as an array.
"""
def get_data(source_url):
    # Define constants specific to this dataset.
    runs_col_idx = 8
    start_year = 1989
    end_year = 2012

    data = requests.get(source_url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')

    table = soup.find("table", attrs={"class": "TableLined"})
    table_data = table.find_all("tr")

    # Find the headings.
    headings = []
    for td in table_data[0].find_all("td"):
        heading = td.text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
        headings.append(heading)

    runs = []

    # Find actual data in the rows excluding the last row to ignore the totals.
    for i in range(1, len(table_data) - 1):
        for idx, td in enumerate(table_data[i].find_all("td")):
            if idx == runs_col_idx:
                runs.append(int(td.text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')))

    return runs, start_year, end_year


def start_querying(segment_tree: SegmentTree, start_year: int, end_year: int):
    print('Accepting queries infinitely. Ctrl+c to exit.')
    while True:
        start, end = input(
            "Enter the start year and end year (space separated) of which you want to calculate the sum:").split()
        start, end = int(start), int(end)

        print('Entered start year:', start)
        print('Entered end year:', end)

        ans = segment_tree.query(start - start_year, max(end_year, end) - start_year)

        print(f'Number of runs Sachin scored between {start} and {end} are: {ans}')


def main():
    SOURCE_URL = 'http://www.howstat.com/cricket/statistics/Players/PlayerYears_ODI.asp?PlayerID=1735'

    runs, start_year, end_year = get_data(SOURCE_URL)

    print(runs)
    print('start_year = ', start_year)
    print('end_year = ', end_year)

    segment_tree = SegmentTree(runs)

    start_querying(segment_tree, start_year, end_year)


if __name__ == "__main__":
    main()
