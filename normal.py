import sys # Нам нужна библиотека sys, чтобы принимать аргументы выполения

class Node: # Класс узла дерева
    def __init__(self, symbol, occurences, firstChild=None, secondChild=None): # Конструктор класса узла
        self.symbol = symbol # Символ (В верхних узлах будет суммой всех нижних)
        self.occurences = occurences # Шанс символа
        self.firstChild = firstChild # Первый дочерниий узел 
        self.secondChild = secondChild # Второй дочерниий узел справа
        self.code = "" # 1 или 0


# Мы используем эту функцию один раз, пропуская в нее корень дерева, оттуда рекурсивно получаем все коды символов
def getCodes(node, value=''): # Формируем словарь вида {символ: двоичный-код}
    global codes # Указываем, что мы используем глобальный словарь codes

    newValue = value + str(node.code) # Добавляем к текущему коду код текущего узла
    if (node.firstChild and node.secondChild): # В алгоритме Хаффмана у узла всегда либо 2 ребенка, либо 0, поэтому здесь можно написать просто node.firstChild/node.secondChild или через or(). Данный способ выбран для простоты понимания.
        getCodes(node.firstChild, newValue) # Ссылаемся на первый узел-ребенок
        getCodes(node.secondChild, newValue) # Ссылаемся на второй узел-ребенок
    else: # Когда у узла 0 детей, это значит, что мы спустились к отдельным символам. 
        codes[node.symbol] = str(newValue) # Возьмем для отдельных символов значения newValue и запишем в словарь codes.


def occurencesToCodes(occurs): # Переводим словарь вида {символ: количество-таких-символов-в-тексте} в {символ: двоичный-код}
    nodes = [] # Создаем массив узлов

    for key in occurs.keys(): # Идем по словарю occurs
        nodes.append(Node(key, occurs[key])) # Создаем узлы для каждого символа

    while len(nodes) > 1: #
        nodes.sort(key=lambda x: x.occurences) # Сортируем в порядке возрастания по occurences

        first = nodes[0]  # Делаем так, что первый узел - меньший, 
        second = nodes[1] # а второй - больший из двух наименьших

        first.code = 1  # Присваиваем код первому узлу
        second.code = 0 # Присваиваем код второму узлу

        parentNode = Node(first.symbol + second.symbol, first.occurences + second.occurences, first, second) # Создаем родительский узел, например из символа A с 3 повлениями и символа B с 4 появлениями мы получим узел AB, который будет иметь 7 появлений и A и B как первый и второй узел-ребенок соответственно 

        nodes.remove(first)      # Убираем первый узел
        nodes.remove(second)     # Убираем второй узел
        nodes.append(parentNode) # И ставим на их место родительский узел

    getCodes(nodes[0]) # По итогу остается только один узел - корень дерева. Из него мы может получить коды всех символов.


def decode(encodedText):
    codesInverted = {} # Создаем обратный словарю codes словарь вида {двоичный-код: символ}
    for key in codes.keys(): # Идем по ключам словаря codes
        codesInverted.update({codes[key]:key}) # Отправляем в словарь двоичный код в качестве ключа и символ в качестве значения

    decodedText = currCode = '' # Создаем переменную декодированного текста decodedText и временную переменную currCode
    for character in encodedText: # Идем посимвольно в закодированном тексте
        currCode += character # Добавляем к непрошедшим проверку ниже символам новый символ
        if currCode in codesInverted.keys(): # Если текущий код есть в нашем словаре, то мы его переводим и добавляем в декодированный текст
            decodedText += codesInverted.get(currCode).replace(newLineSymbol, "\n") # Получаем декодированное значение символа и меняем наш неиспользуемый символ на перенос строки
            currCode = '' # Обнуляем временную переменную, так как мы уже получили из неё полный символ
    return decodedText # Возвращаем декодированный текст



if len(sys.argv) != 4: # Если аргументов слишком много или недостаточно, завершаем выполенние программы
    print("Invalid agrument amount") # Выводим объяснение завершения программы
    sys.exit(0) # Завершаем выполение программы

codes = {} # Создаем глобальный словарь вида {символ: двоичный-код}
newLineSymbol = "" # Задаем символ, который будет заменять перенос строки в нашем тексте. Он не должен присутствовать в тексте, поэтому выбрал DELETE

match sys.argv[1]: # Проверяем первый аргумент выполнения программы
    case '--encode': # Если пользователь собирается закодировать текст
        input_file = open(sys.argv[2], 'r')   # Открываем файл, с которого будем читать текст
        output_file = open(sys.argv[3], 'wb') # Открываем файл, в который будем побайтово записывать 
        newLineInBytes = "\n".encode("utf-8") # Делаем закодированный перенос строки
        
        text = ''.join(input_file.readlines()).replace("\n", newLineSymbol) # Получаем полный текст из файла, заменяя перенос строки на неиспользуемый символ DELETE
        
        occurs = {} # Из текста получаем словарь вида {символ: количество-таких-символов-в-тексте}
        for symbol in text: # Идем посимвольно по тексту
            if symbol not in occurs.keys(): # Избегаем повторения, проверяя, добавили ли мы уже этот символ в словарь
                occurenceCount = text.count(symbol) # Считаем количество появлений этого символа
                occurs.update({str(symbol): int(occurenceCount)})


        output_file.write(len(occurs).to_bytes(2, byteorder="big") + newLineInBytes) # Записываем первую линию с количеством разных символов в тексте
        for key in occurs.keys():
            symbolInBytes = (key + " ").encode("utf-8") # Делаем закодированный сивол
            codeInBytes = int(occurs[key]).to_bytes(2,"big") # Делаем закодированное значение
            
            fullByteLine =  symbolInBytes + codeInBytes + newLineInBytes # Создаем полную строку
            output_file.write(fullByteLine) # Записываем её
            
        occurencesToCodes(occurs) # Формируем глобальный словарь codes вида {символ: двоичный-код}

        textInCodes = "" # Формируем строку с закодированным текстом
        for character in text: # Идём по каждому символу в тексте
            textInCodes += codes[character] # Добавляем символ в закодированном виде в отдельную строку


        while len(textInCodes) > 8: # Действуем, пока в тексте достаточно битов на запись полного байта
            output_file.write(int(textInCodes[0:8],2).to_bytes(1,"big")) # Пишем по байту за раз
            textInCodes = textInCodes[8:] # Убираем из текста записанный байт

        lastBits = textInCodes # Для понимания, ведь остались только <8 битов

        extra_bits = 8-len(lastBits) # Посчитать, сколько нулей нужно добавить к остатку, чтобы получился полный байт                
        currByte = lastBits + "0" * extra_bits # Добавляем эти нули
        output_file.write(int(currByte,2).to_bytes(1,byteorder="big")) # Записываем байт с остатоком и доп нулями  
        output_file.write(extra_bits.to_bytes(1,byteorder="big")) # Записывайм байт с количеством доп нулей в конце
    case '--decode': # Если пользователь собирается декодировать текст
        input_file = open(sys.argv[2], 'rb') # Открываем файл, из которого будем читать в байтах
        output_file = open(sys.argv[3], 'w') # Открываем файл, в который будем записывать

        occurs = {} # Создаем словарь формата {символ: количество-таких-символов-в-тексте}

        dictLength = int.from_bytes(input_file.readline()[:-1], byteorder="big") # Получаем из 
        for lineIndex in range(dictLength): # Проходим через каждую строку текста, где есть словарь
            line = input_file.readline() # Берем эту строку
            occurs.update({chr(line[0]): int.from_bytes(line[2:], "big")}) # Записываем первый байт как символ, а оставшиеся байты в строке как количество таких символов в тексте

        encodedText = "" # Считываем зашифрованный 
        for line in input_file.readlines(): # Нам приходится работать с несколькими строками, так как текст может иметь переносы строки, сделанные случайно другими кодами
            for character in line: # Идем по всей строке
                binCharacter = str(bin(character))[2:] # Создаем двоичное представление символа
                encodedText += '0' * (8 - len(binCharacter)) + binCharacter # Добавляем байтовое представление символа с незначащими нулями

        lastZeroCount = int(encodedText[-8:], 2) # Берет последний байт и достает из него количество лишних нулей
        encodedText = encodedText[:-(lastZeroCount + 8)] # # Убираем из конечной строки лишние нули в конце и байт с их количеством

        occurencesToCodes(occurs)   # Генерирует глобальный словарь codes
        decodedText = decode(encodedText) # Декодирует конечный текст, используя глобальный словарь codes
        output_file.write(decodedText) # Записываем в файл результат
    
    case _: # На случай, если мы получим не --encode и не --decode в первом аргументе, завершаем выполенение
        print("First argument should be either --encode or --decode") # Выводим объяснение завершения программы
        sys.exit() # Завершаем выполение программы

input_file.close()  # Закрываем входной файл
output_file.close() # Закрываем файла результата выполнения