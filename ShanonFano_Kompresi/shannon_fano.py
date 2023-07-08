from PIL import Image
import heapq


class Node:
    def __init__(self, symbol=None, frequency=None, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_frequency_table(data):
    frequency_table = {}
    for symbol in data:
        frequency_table[symbol] = frequency_table.get(symbol, 0) + 1
    return frequency_table


def build_huffman_tree(frequency_table):
    heap = []
    for symbol, frequency in frequency_table.items():
        node = Node(symbol=symbol, frequency=frequency)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged_node = Node(
            frequency=node1.frequency + node2.frequency,
            left=node1,
            right=node2
        )
        heapq.heappush(heap, merged_node)

    return heap[0]


def build_codewords_mapping(node, codeword='', codewords_mapping=None):
    if codewords_mapping is None:
        codewords_mapping = {}

    if node.symbol is not None:
        codewords_mapping[node.symbol] = codeword
    else:
        build_codewords_mapping(node.left, codeword + '0', codewords_mapping)
        build_codewords_mapping(node.right, codeword + '1', codewords_mapping)

    return codewords_mapping


def compress(file):
    image = Image.open(file)
    data = list(image.getdata())

    frequency_table = build_frequency_table(data)
    huffman_tree = build_huffman_tree(frequency_table)
    codewords_mapping = build_codewords_mapping(huffman_tree)

    compressed_data = ''.join(codewords_mapping[symbol] for symbol in data)

    return image.point(lambda i: 255 if i > 128 else 0)
