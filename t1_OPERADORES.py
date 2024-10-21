import spacy
from itertools import product

nlp = spacy.load('pt_core_news_md')

operadores_logicos = {
    " and ",
    " e ",
    " or ", 
    " ou ", 
    " então ", 
    " then "
}

class Operador:
    """Classe para representar uma operação lógica."""
    def __init__(self, operador, variavel_um, variavel_dois):
        self.operador = operador  # A string do operador
        self.variavel_um = variavel_um  # A variável um
        self.variavel_dois = variavel_dois  # A variável dois

class Variavel:
    """Classe para representar uma variável lógica."""
    def __init__(self, variavel):
        self.variavel = variavel  # A string da variável
        self.nome = None  # Nome associado, inicialmente nulo

def remove_virgula(variaveis):
    """Remove vírgulas de cada variável na lista fornecida."""
    for variavel in variaveis:
        variavel.variavel = variavel.variavel.replace(",", "").strip()  # Remove vírgulas e espaços em branco

def adiciona_nome(variaveis_premissa):
    global contador_variaveis  # Indica que contador_variaveis é global
    letras_variaveis = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(len(variaveis_premissa)):
        variaveis_premissa[i].nome = letras_variaveis[contador_variaveis]
        contador_variaveis += 1  # Incremento correto

def atualiza_tabela_verdade(variaveis_premissa):
    """Cria e retorna uma tabela verdade para todas as variáveis acumuladas."""
    num_variaveis = len(variaveis_premissa)
    
    # Gera todas as combinações de valores de verdade (True, False) para as variáveis
    combinacoes = list(product([True, False], repeat=num_variaveis))
    
    # Cria a tabela verdade
    tabela_verdade = []
    
    # Adiciona o cabeçalho da tabela
    header = [variavel.nome for variavel in variaveis_premissa]
    tabela_verdade.append(header)  # Nomes das variáveis
    
    # Adiciona cada linha da tabela verdade
    for combinacao in combinacoes:
        linha = [str(int(valor)) for valor in combinacao]  # Converte True/False em 1/0
        tabela_verdade.append(linha)

    return tabela_verdade

def imprimir_tabela_verdade(tabela_verdade):
    """Imprime a tabela verdade formatada."""
    for linha in tabela_verdade:
        # Converte todos os elementos da linha para string antes de juntar
        print("\t".join(map(str, linha)))  # Imprime cada linha da tabela

# Armazena as variáveis e a tabela verdade globalmente
variaveis_global = []
tabela_verdade_global = []

def processar_premissa():
    global variaveis_global, tabela_verdade_global , operadores_globais # Usar variáveis e tabela verdade globais
    premissa = input("Digite a premissa:\n").lower()  # Converte a frase para minúsculas

    variaveis_premissa = extrair_variaveis(premissa)  # Extrai variáveis da premissa
    remove_virgula(variaveis_premissa)  # Remove vírgulas das variáveis
    adiciona_nome(variaveis_premissa)  # Adiciona nomes às variáveis

    adicionar_variaveis_globais(variaveis_premissa)  # Adiciona novas variáveis à lista global
    imprimir_variaveis_global()  # Imprime a lista de variáveis

    # Atualiza e imprime a tabela verdade global
    atualizar_e_imprimir_tabela_verdade()

def extrair_variaveis(premissa):
    """Extrai variáveis da premissa com base nos operadores lógicos."""
    variaveis_premissa = []
    posicao = -1

    for operador in operadores_logicos:
        posicao = premissa.find(operador)
        if posicao != -1:
            variavel = premissa[:posicao].strip()  # Pega a parte da string antes do operador
            variaveis_premissa.append(Variavel(variavel))
            premissa = premissa[posicao + len(operador):].strip()

    # Se nenhum operador for encontrado, adiciona a premissa como uma variável.
    if posicao == -1:
        variaveis_premissa.append(Variavel(premissa))

    return variaveis_premissa

def adicionar_variaveis_globais(variaveis_premissa):
    """Adiciona novas variáveis à lista global se não estiverem presentes."""
    for nova_variavel in variaveis_premissa:
        if not any(nova_variavel.variavel == v.variavel for v in variaveis_global):
            variaveis_global.append(nova_variavel)

def imprimir_variaveis_global():
    """Imprime a lista de variáveis globais com seus nomes associados."""
    print([f"Variável: {v.variavel}, Nome: {v.nome}" for v in variaveis_global])

def atualizar_e_imprimir_tabela_verdade():
    """Atualiza e imprime a tabela verdade global."""
    global tabela_verdade_global  # Usar tabela verdade global
    tabela_verdade_global = atualiza_tabela_verdade(variaveis_global)  # Atualiza a tabela de verdade
    imprimir_tabela_verdade(tabela_verdade_global)  # Imprime a tabela de verdade

def entao(operador, tabela_verdade):
    """Calcula a operação lógica 'A então B' e adiciona o resultado à tabela verdade."""
    variavel_a = operador.variavel_um
    variavel_b = operador.variavel_dois

    nova_coluna = []  # Armazena os resultados da operação

    for linha in tabela_verdade[1:]:  # Ignora o cabeçalho
        a = bool(int(linha[variaveis_global.index(variavel_a)]))  # Converte para booleano
        b = bool(int(linha[variaveis_global.index(variavel_b)]))  # Converte para booleano
        resultado = not a or b  # A operação 'A então B'
        nova_coluna.append(int(resultado))  # Adiciona 1 para True, 0 para False

    # Adiciona a nova coluna à tabela verdade
    tabela_verdade[0].append('A então B')  # Adiciona o cabeçalho da nova coluna
    for i, linha in enumerate(tabela_verdade[1:], start=1):
        linha.append(nova_coluna[i - 1])  # Adiciona o resultado em cada linha correspondente

def e(operador, tabela_verdade):
    """Calcula a operação lógica 'A e B' e adiciona o resultado à tabela verdade."""
    variavel_a = operador.variavel_um
    variavel_b = operador.variavel_dois

    nova_coluna = []  # Armazena os resultados da operação

    for linha in tabela_verdade[1:]:  # Ignora o cabeçalho
        a = bool(int(linha[variaveis_global.index(variavel_a)]))  # Converte para booleano
        b = bool(int(linha[variaveis_global.index(variavel_b)]))  # Converte para booleano
        resultado = a and b  # A operação 'A e B'
        nova_coluna.append(int(resultado))  # Adiciona 1 para True, 0 para False

    # Adiciona a nova coluna à tabela verdade
    tabela_verdade[0].append('A e B')  # Adiciona o cabeçalho da nova coluna
    for i, linha in enumerate(tabela_verdade[1:], start=1):
        linha.append(nova_coluna[i - 1])  # Adiciona o resultado em cada linha correspondente

def ou(operador, tabela_verdade):
    """Calcula a operação lógica 'A ou B' e adiciona o resultado à tabela verdade."""
    variavel_a = operador.variavel_um
    variavel_b = operador.variavel_dois

    nova_coluna = []  # Armazena os resultados da operação

    for linha in tabela_verdade[1:]:  # Ignora o cabeçalho
        a = bool(int(linha[variaveis_global.index(variavel_a)]))  # Converte para booleano
        b = bool(int(linha[variaveis_global.index(variavel_b)]))  # Converte para booleano
        resultado = a or b  # A operação 'A ou B'
        nova_coluna.append(int(resultado))  # Adiciona 1 para True, 0 para False

    # Adiciona a nova coluna à tabela verdade
    tabela_verdade[0].append('A ou B')  # Adiciona o cabeçalho da nova coluna
    for i, linha in enumerate(tabela_verdade[1:], start=1):
        linha.append(nova_coluna[i - 1])  # Adiciona o resultado em cada linha correspondente


def processa_conclusao():
    global tabela_verdade_global  # Usar tabela verdade global
    if len(variaveis_global) < 2:
        print("Por favor, adicione pelo menos duas variáveis para a conclusão.")
        return
    
    # Solicita ao usuário quais variáveis usar para a operação "então"
    print("Selecione as variáveis para a operação 'então':")
    for i, variavel in enumerate(variaveis_global):
        print(f"{i + 1}: {variavel.nome} (Valor: {variavel.variavel})")
    
    # Lê as entradas do usuário
    escolha_a = int(input("Selecione a primeira variável (A): ")) - 1
    escolha_b = int(input("Selecione a segunda variável (B): ")) - 1
    
    # Obtem as variáveis selecionadas
    p = variaveis_global[escolha_a]
    q = variaveis_global[escolha_b]


    op1 = Operador("entao",p,q)
    op2 = Operador("e",p,q)
    op3 = Operador("ou",p,q)
    
    # Chama a função entao
    entao(op1, tabela_verdade_global)
    e(op2,tabela_verdade_global)
    ou(op3, tabela_verdade_global)
    # Imprime a tabela verdade atualizada
    imprimir_tabela_verdade(tabela_verdade_global)

def processar_argumento():
    while True:
        op = input("1 para adicionar uma premissa\n2 para adicionar conclusão\n3 para plotar a tabela de verdade\n0 para sair\nSelecione uma opção: ")
        if op == "0":
            break
        elif op == "1":
            processar_premissa()
        elif op == "2":
            processa_conclusao()
        elif op == "3":
            imprimir_tabela_verdade(tabela_verdade_global)

def main():
    global contador_variaveis
    contador_variaveis = 0
    processar_argumento()

if __name__ == "__main__":
    main()
