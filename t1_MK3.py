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
    combinacoes = list(product([False, True], repeat=num_variaveis))
    
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
        print("\t".join(linha))  # Imprime cada linha da tabela

# Armazena as variáveis e a tabela verdade globalmente
variaveis_global = []
tabela_verdade_global = []

def processar_premissa():
    global variaveis_global, tabela_verdade_global  # Usar variáveis e tabela verdade globais
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

def processar_argumento():
    while True:
        op = input("1 para adicionar uma premissa\n2 para adicionar conclusão\n3 para plotar a tabela de verdade\n0 para sair\nSelecione uma opção: ")
        if op == "0":
            break
        elif op == "1":
            processar_premissa()

def main():
    global contador_variaveis
    contador_variaveis = 0
    processar_argumento()

if __name__ == "__main__":
    main()
