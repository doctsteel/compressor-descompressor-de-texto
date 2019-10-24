import sys

def create_header_and_wordset(string):
    """Função precisa da frase original.
    string é obviamente do tipo str
    
    O retorno dessa função vem em três:
    header_bytes -> o header do arquivo final,
    que indica quantas palavras unicas existem no texto,
    no formato de dois bytes em ordem convencional.
    set_palavras -> lista de palavras únicas, sem ordem alguma. Usei da tipagem de set() em python.
    dict_virgulas_pontos -> dicionário com os index de cada virgula e ponto
    da frase inserida no arquivo a ser comprimido.

    Exemplo:
    string = "Joao comeu, banana."
    retorno:
    header_bytes = b'\x00\x03'
    set_palavras = {"Joao", "comeu", "banana"}
    dict_virgulas_pontos = {'virgulas': [2], 'pontos':[5]}
    """
    # separar num array de palavras
    dict_virgulas_pontos = {'virgulas':[], 'pontos':[]}

    enfase_nas_virgulas = string.replace(',', ' ,')# Casos especiais, fazendo a separacao da virgula
    e_tambem_nos_pontos = enfase_nas_virgulas.replace('.',' .')#Mesma coisa de cima só que pontos
    splitado = e_tambem_nos_pontos.split(' ')#separa as palavras baseado espaços vazios
    for index, each in enumerate(splitado):#retorno index e seu valor, enumerarando o array 
        if each == ',':                     #se o elemento for virgula
            dict_virgulas_pontos['virgulas'].append(index)#insere a referencia de virgula no dict baseado no index da frase split 
            
        elif each == '.':
            dict_virgulas_pontos['pontos'].append(index+1)
    
    string_sem_virgula = string.replace(',', ' ')
    string_sem_pontuacao = string_sem_virgula.replace('.',' ')
    array_palavras = string_sem_pontuacao.split(' ')
    
    # criar set de palavras unicas
    set_palavras = []
    for palavra in array_palavras:
        if len(palavra) > 3:
            set_palavras.append(palavra)
    set_palavras = set(set_palavras)
    len_cabecalho = len(set_palavras)
    header_bytes = (len_cabecalho).to_bytes(2, byteorder='big')

    # esse método já retorna o cabeçalho,
    # a lista de palavras únicas(é descartado todas repetidas até sobrar uma só) 
    # e a posição das virgulas e dos pontos.
    print(set_palavras)

    return header_bytes, set_palavras, dict_virgulas_pontos


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


def compress_string(stringdict, stringmaltratada, arrvirgulas):
    """
    Recebe um dicionário de strings para bytes,
    uma string original a ser traduzida,
    e um dicionário com as posições de virgulas e pontos na frase.

    Exemplo:

    stringdict = {"Joao": b'\xff\x00\x00',
     "comeu": b'\xff\x00\x01',
     "banana": b'\xff\x00\x02'}

    stringmaltratada = "Joao comeu, banana."

    arrvirgulas = {'virgulas': [2], 'pontos':[5]}
    retorno:
    
    retorno = b'\xff\x00\x00 \xff\x00\x01, \xff\x00\x02.'

    
    """
    # método bem feio, mas é o que tive cabeça pra escrever até as 3 da manhã, honestamente.
    # esse método recoloca e transforma em bytes as virgulas e os pontos que constam na frase.

    string_meio_limpo = stringmaltratada.replace(',',' ')
    string_full_limpo = string_meio_limpo.replace('.',' ')

    stringoriginalcortada = string_full_limpo.split(' ')
    conta_espacos = 0
    for each in arrvirgulas['virgulas']:
        stringoriginalcortada.insert(each + conta_espacos,',')
        conta_espacos += 1
    for each in arrvirgulas['pontos']:
        stringoriginalcortada.insert(each + conta_espacos, '.')
        conta_espacos += 1
    # A MELHOR LINHA DO CÓDIGO
    # Funciona assim: é uma interpretação de lista.
    # estou criando a lista 'translated' pra cada elemento que exista no dict palavra-> bytes.
    # se a palavra não existe no dicionário de bytes (elemento menor que 4 letras),
    # retorno a própria palavra mesmo. Se existe bytes atrelados, retorno os bytes daquela palavra.
    translated = [stringdict.get(i, str.encode(i)) for i in stringoriginalcortada]
    # agora, transformando essa lista no formato pedido.

    return translated



# condicional de inicio do programa:
# se o programa for executado com -c, é pra Comprimir.
# o sys,argv[0] eh reservado para o nome do programa, o segundo parametro em comprimir ou descomprimir, o terceiro eh o nome do arquivo a ser usado
if sys.argv[1] == '-c':

    arquivo = open(sys.argv[2])
    frase = arquivo.read()
#    print("texto a ser comprimido: \n" + frase)



    header, word_set, commas = create_header_and_wordset(frase)

    part_2 = list_words(word_set)
    word_dict = create_dict(word_set)
    compressed_string_list = compress_string(word_dict, frase, commas)
    final = header + part_2
    length = len(compressed_string_list)
    i = 0
    for element in compressed_string_list:
        final += element 
        i += 1
        if i != length:
            final += str.encode(' ')
    final = final.replace(b' .', b'.')#nao sei mas precisa disso, veremos para ficar certinho
    final = final.replace(b' .', b'.')
    final = final.replace(b' , ', b',')

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
    
    print('Resultado da descompressao: ')
    print(d.decode('utf-8'))
    



# Em ambos os métodos ele tenta ler de um arquivo, e na hora de salvar os resultados ele tenta criar antes caso não exista.
# Não importei nenhuma biblioteca que fosse interferir com o próprio algoritmo, só a sys que era necessário pra executar como o professor quis.

#é isso galera amo voces boa noite pois já são 5 da manha e eu voltei cedo da aula pra ficar fazendo isso desde as 9


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
