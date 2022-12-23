import sys

class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        # Шанс символа
        self.prob = prob

        # Символ (В верхних нодах будет суммой всех нижних)
        self.symbol = symbol

        # Дочерниий объект (Нода)
        self.left = left

        # right node
        self.right = right

        # 1 или 0
        self.code = ""


codes = dict()


def getCodes(node, value=''):
    newValue = value + str(node.code)

    if (node.left or node.right):
        getCodes(node.left, newValue)
        getCodes(node.right, newValue)
    else:
        codes[node.symbol] = newValue

    return codes


def encode(text):
    chances = []
    alphabet = []

    text = text.replace("\n", "Ⓐ")
    # print(text)
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
        newNode = Node(left.prob+right.prob, left.symbol +
                       right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    symbolDictionnary = getCodes(nodes[0])
    print("The result:", symbolDictionnary)

    result = ''
    for character in text:
        result += symbolDictionnary[character]

    print("Filesize before:", len(text) * 8, "bits")
    print("Filesize after:",  len(result), "bits")

    return result, symbolDictionnary


def decode(text, dictionnary):
    arr = [[dictionnary[item], item]for item in dictionnary]
    decodedText = symbol = ''
    for character in text:
        symbol += character
        for i in range(len(arr)):
            if arr[i][1] == symbol:
                decodedText += arr[i][0]
                symbol = ''
    return decodedText.replace("Ⓐ", "\n")



# if len(sys.argv) < 4:
#     raise "Not enough arguments"
# else:
#     method = sys.argv[1]
#     input_file = sys.argv[2]
#     output_file = sys.argv[3]
# match method:
#     case '--encode':
#         encode(input_file,output_file)
#     case '--decode':
#         decode(input_file,output_file)





text = "fuckdima"
print(text)
resultText, testDictionnary = encode(text)
print("Encoded text", resultText)
print("Decoded text", decode(resultText, {'111': ' ', '110': 'Ⓐ', '101': 'd', '100': 'i', '011': 'm', '010': 'a', '0011': 'f', '0010': 'u', '0001': 'c', '0000': 'k'}))
