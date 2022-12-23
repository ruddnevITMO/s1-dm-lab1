import sys

class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        # Шанс символа
        self.prob = prob

        # Символ (В верхних нодах будет суммой всех нижних)
        self.symbol = symbol

        # Дочерниий объект слева (Нода)
        self.left = left

        # Дочерниий объект справа (Нода)
        self.right = right

        # 1 или 0 
        self.code = ""


codes = dict()


def encode(text):
    def getCodes(node, value=''):
        newValue = value + str(node.code)

        if (node.left or node.right):
            getCodes(node.left, newValue)
            getCodes(node.right, newValue)
        else:
            codes[node.symbol] = newValue

        return codes

    chances = []
    alphabet = []

    for character in text:
        if character not in alphabet:
            chance = text.count(character)
            chances.append([character, chance])
            alphabet.append(character)

    nodes = []

    # converting symbols and probabilities into huffman tree nodes
    for i in range(len(chances)):
        symbol = chances[i][0]
        nodes.append(Node(chances[i][1], symbol))

    while len(nodes) > 1:
        # sort all the nodes in ascending order based on their probability
        nodes.sort(key=lambda x: x.prob)
        # for node in nodes:
        #      print(node.symbol, node.prob)

        # pick 2 smallest nodes
        left = nodes[0]
        right = nodes[1]

        left.code = 1
        right.code = 0

        # combine the 2 smallest nodes to create new node
        newNode = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    symbolDictionnary = getCodes(nodes[0])
    # print("The result:", symbolDictionnary)

    # new=[[item,symbolDictionnary[item]] for item in symbolDictionnary]
    # print(len(new))
    # for i in range(len(new)):
    #     print(new[i][0], new[i][1])

    result = ''
    for character in text:
        result += symbolDictionnary[character]

    print("Filesize before:", len(text) * 8, "bits")
    print("Filesize after:",  len(result), "bits (without the dictionnary)")

    return result, symbolDictionnary


def decode(text, dictionnary):
    decodedText = symbol = ''
    for character in text:
        symbol += character
        if symbol in dictionnary:
            decodedText += dictionnary.get(symbol)
            symbol = ''
    return decodedText




if len(sys.argv) != 4:
    raise "Invalid agrument amount"

encodeOrDecode = sys.argv[1]


match encodeOrDecode:
    case '--encode':
        input_file = open(sys.argv[2], "r")
        output_file = open(sys.argv[3], "wb")

        textToEncode = input_file.readline()

        result, dictionnary = encode(textToEncode)

        # There should be outputting to a file, but it is in progress.

    case '--decode':
        input_file = open(sys.argv[2], "rb")
        output_file = open(sys.argv[3], "w")

        dictionnary = {}

        dictionnaryLength = int(input_file.readline(), 2) # Считываем мощность словаря
        for i in range(dictionnaryLength): # Считываем словарь
            a, b = map(str, input_file.readline().split())
            dictionnary.update({b: chr(int(a, 2))})
        encodedText = input_file.readline()

        result = decode(encodedText, dictionnary)

        # There should be outputting to a file, but it is in progress.

    case _:
        raise "First argument should be either --encode or --decode"



output_file.close()
input_file.close()
