# Compressor e descompressor de texto
## Trabalho de estruturas de arquivos do segundo semestre de 2019 do Prof. Celmar.
### Requisitos

Para revisar os requisitos do compressor de texto descrito no pdf original:

- O programa deverá comprimir e descomprimir arquivos .txt para .cmp e vice-versa.
- As frases compressas não terão caracteres que não são letras, números, virgulas e pontos.(Letras com acento não entram, caracteres especiais tipo traços, underline, barras também não entram.)
- Somente as palavras com mais de 3 caracteres serão comprimidas.
- O arquivo comprimido consistirá de três partes:
    - O **Header**, que consiste de dois bytes em ordem de maior ordem pra menor ordem.
    - O **Endereçamento**, com todas as palavras únicas _(não tem palavra repetida)_ maiores que 3 letras, separadas por uma vírgula e nada mais
    - A **Frase compressa**, que utiliza o posicionamento das palavras no endereçamento para serem comprimidas em três bytes no seguinte formato: (255) (xxx) (xxx).
- O Programa deverá ser executado no terminal com os seguintes argumentos:
    
        python compressor (-c ou -d) (nome do arquivo)

    - o argumento -c significa compressão, e o arquivo a ser comprimido deve ser um .txt.
    -   -d é descompressão, e a extensão do arquivo deve ser .cmp.


### Estrutura do código

#### Imports utilizados

Sei que é proibido usar bibliotecas externas para ajudar no programa, mas a única solução que encontrei em python para que o programa aceitasse _command-line arguments_ foi importando a lib **sys**.
Essa biblioteca nativa do python interage com o terminal e com o computador diretamente, e fornece a variável `sys.argv`, um array de string que consiste nas coisas escritas no terminal, separados por espaço.
O comando `python compressor.py -c texto.txt` resulta no seguinte `argv`:
        
        >>> import sys
        >>> sys.argv[0]
        "compressor.py"
        >>> sys.argv[1]
        "-c"
        >>> sys.argv[2]
        "texto.txt"

E termina aí o uso da unica biblioteca importada.

#### Estruturação básica do programa

Utilizei-me bastante da tipagem de variáveis no python fornecer várias ferramentas para não precisar inventar a roda diversas vezes.
Em strings, usei do split, replace, slices e conversão para bytes, naturais de strings do python:

        >>> exemplo = "Joao comeu banana"
        >>> exemplo.split(" ")
        ["Joao", "comeu", "banana"]
        >>> exemplo.replace("Joao", "Pedro")
        "Pedro comeu banana"
        >>> exemplo[0:11]
        "Joao comeu"
        >>> str.encode("exemplo")
        b'Joao comeu banana'

Acho justo explicar como o tipo byte funciona em python. O byte, sempre representado por uma letra b seguido de aspas simples, consegue ser impresso na tela sempre na seguinte forma: `b'\xff'`

ff é o byte do número 255, e bytes de numeros sempre começam com um backslash e x em seguida.
Bytes de caracteres ASCII são impressos normalmente:
`b'isso e um conjunto de bytes'`

Para manipular um byte e converter uma string ou um int para bytes, usei os seguintes métodos:

        >>> byte_exemplo = b'\xff'
        >>> int.from_bytes(byte_exemplo, 'big')
        255
        >>> byte_string = b'isso eh uma string de bytes'
        >>> byte_string
        b'isso eh uma string de bytes'
        >>> byte_string.decode('utf-8')
        'isso eh uma string de bytes'

#### Compressão

Monto o arquivo final 

    
