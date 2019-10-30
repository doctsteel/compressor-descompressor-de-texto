import sys
from collections import OrderedDict


def create_header_and_wordset(string):
    """Função precisa da frase original.
    string é obviamente do tipo str

    O retorno dessa função vem:
    header_bytes -> o header do arquivo final,
    que indica quantas palavras unicas existem no texto,
    no formato de dois bytes em ordem convencional.
    set_palavras -> conjunto de palavras únicas, em ordem.

    Exemplo:
    string = "Joao comeu, banana."
    retorno:
    header_bytes = b'\x00\x03'
    set_palavras = ["Joao", "comeu", "banana"]

    """
    # separar num array de palavras
    char_list = list(string)
    word_hold = ""
    word_list = []
    len_frase = len(string)
    for index, char in enumerate(char_list):
        if char.isalpha():  # verifica se o char eh alfanumerico
            word_hold += char
            if not len_frase - 1 == index:
                if not char_list[index+1].isalpha():
                    if len(word_hold) > 3:
                        word_list.append(word_hold)
                    word_hold = ""
            else:
                word_list.append(word_hold)
                word_hold = ""
    # criar set de palavras unicas
    set_palavras = list(OrderedDict.fromkeys(word_list))
    len_cabecalho = len(set_palavras)
    header_bytes = (len_cabecalho).to_bytes(2, byteorder='big')

    # esse método já retorna o cabeçalho,
    # e a lista de palavras sem duplicadas.
    return header_bytes, set_palavras


def list_words(set_palavras):
    """
    Recebe um array de palavras no tipo set()

    retorna no formato de bytes, todas as palavras do set
    separas por virgula.

    Exemplo:
    set_palavras = {"Joao", "comeu", "banana"}
    retorno = b'Joao,comeu,banana'

    """

    parte_2 = ""
    for palavra in set_palavras:
        parte_2 = parte_2 + palavra+','

    # esse método retorna a parte do meio do método de compressão
    # que o professor mandou fazer.
    # ou seja: retorna, em bytes, as palavras na ordem de index de acordo com a montagem no próximo método

    return str.encode(parte_2)


def create_dict(set_palavras):
    """
    Recebe set_palavras em strings
    Retorna dicionário com o endereçamento de acordo com a posição.

    Exemplo:
    set_palavras = {"Joao", "comeu", "banana"}
    retorno:
    parte_3_dict = {"Joao": b'\xff\x00\x00',
     "comeu": b'\xff\x00\x01',
     "banana": b'\xff\x00\x02'}
    """

    parte_3_dict = {}
    contador_first_byte = 0
    contador_second_byte = 0
    for palavra in set_palavras:
        parte_3_dict[palavra] = bytes(
            [255, contador_second_byte, contador_first_byte])
        contador_first_byte += 1
        if contador_first_byte == 256:
            contador_first_byte = 0
            contador_second_byte += 1

    # cria o padrão dos tres bytes 255 0 0 que o professor pediu na terceira parte do retorno.

    return parte_3_dict


def compress_string(stringdict, stringmaltratada):
    """ É chamado a partir do -c na linha de comando e logo em seguida o nome do arquivo
        Sintaxe:
        python compressor.py -c texto.txt 

    """


    aux_word = ""
    final = b''
    len_frase = len(stringmaltratada)

    for index, char in enumerate(stringmaltratada):
        if char.isalpha():
            aux_word+=char
            if not len_frase - 1 == index: 
                if not stringmaltratada[index+1].isalpha():
                    final += stringdict.get(aux_word, str.encode(aux_word))
                    aux_word = ""
            else:
                final+= stringdict.get(aux_word, str.encode(aux_word))
                aux_word=""
        if not char.isalpha():
            final+= str.encode(char)
    # agora, transformando essa lista no formato pedido.

    return final



# condicional de inicio do programa:
# se o programa for executado com -c, é pra Comprimir.

if sys.argv[1] == '-c':

    arquivo = open(sys.argv[2])
    frase = arquivo.read()
#    print("texto a ser comprimido: \n" + frase)



    header, word_set = create_header_and_wordset(frase)

    part_2 = list_words(word_set)
    word_dict = create_dict(word_set)
    compressed_string_list = compress_string(word_dict, frase)
    final = header + part_2 + compressed_string_list


    file_comprimido = open("{}.cmp".format(sys.argv[2]), 'wb')
    file_comprimido.write(final)
    file_comprimido.close()
    print("texto comprimido com sucesso no arquivo {}.cmp.".format(sys.argv[2]))
    arquivo.close()
    print("pra constar, arquivo compresso sendo exibido na tela.")
    print(final)



# Se rodar com -d, é pra Descomprimir.

if sys.argv[1] == '-d':
    arquivo = open(sys.argv[2], 'rb')
    headaer = int.from_bytes(arquivo.read(2), byteorder='big')
    d = arquivo.read()
    wordmap = []#array com rrn
    reference = 0
    while headaer > 0:
        reference = d.find(b',')#define referencia como a virgula do header 
        wordmap.append(d[:reference])#corta o arq ate posicao tal
        d = d[reference+1:]
        headaer -= 1
    frase_lista_bytes = []
    index_num = 0
    while index_num < len(d):
        if d[index_num] == 255:
            frase_lista_bytes.append(d[index_num:index_num+3])
        index_num+=1
    frase_dict_enderecos = {}
    index_num = 0
    while index_num < len(wordmap):
        d = d.replace(b'\xff'+(index_num).to_bytes(2,'big'), wordmap[index_num])
        index_num += 1
    
    nome_de_arquivo= sys.argv[2]
    nome_de_arquivo = nome_de_arquivo[:-4]
    descomprimido = open("{}".format(nome_de_arquivo), 'w')
    descomprimido.write(d.decode('utf-8'))
    descomprimido.close()
    arquivo.close()
    print(d.decode('utf-8'))




# Em ambos os métodos ele tenta ler de um arquivo, e na hora de salvar os resultados ele tenta criar antes caso não exista.
# Não importei nenhuma biblioteca que fosse interferir com o próprio algoritmo, só a sys que era necessário pra executar e 
# a collections, que fornece o tipo de dado OrderedDict, que auxilia com a criação de um conjunto ordenado.

# Caveira do mal extremamente importante para o trabalho:
#                       :::!~!!!!!:.
#                   .xUHWH!! !!?M88WHX:.
#                 .X*#M@$!!  !X!M$$$$$$WWx:.
#                :!!!!!!?H! :!$!$$$$$$$$$$8X:
#               !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
#              :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
#              ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
#                !:~~~ .:!M"T#$$$$WX??#MRRMMM!
#                ~?WuxiW*`   `"#$$$$8!!!!??!!!
#              :X- M$$$$       `"T#$T~!8$WUXU~
#             :%`  ~#$$$m:        ~!~ ?$$$$$$
#           :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
# .....   -~~:<` !    ~?T#$$@@W@*?$$      /`
# W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
# #"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
# :::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
# .~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
# Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
# $R@i.~~ !     :   ~$$$$$B$$en:``
# ?MXT@Wx.~    :     ~"##*$$$$M~

