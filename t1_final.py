import spacy
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import re

nlp = spacy.load('pt_core_news_lg')

operadores_logicos = {
    " and ",
    " e ",
    " or ", 
    " ou ", 
    " então ", 
    " then "
}

class Operador:
    def __init__(self, operador, variavel_um, variavel_dois):
        self.operador = operador  # A string do operador
        self.variavel_um = variavel_um  # A variável um
        self.variavel_dois = variavel_dois  # A variável dois

class Variavel:
    """Classe para representar uma variável lógica."""
    def __init__(self, variavel):
        self.variavel = variavel  # A string da variável
        self.nome = None  # Nome associado, inicialmente nulo

################################ FUNÇÕES TABELA VERDADE ##############################
def atualiza_tabela_verdade(variaveis_premissa):    
    # Identifica as variáveis originais e negadas
    variaveis_originais = [var for var in variaveis_premissa if not var.nome.startswith('~')]
    num_variaveis = len(variaveis_originais)
    
    combinacoes = list(product([True, False], repeat=num_variaveis))
    
    tabela_verdade = []
    
    header = [var.nome for var in variaveis_premissa]
    tabela_verdade.append(header)  # Nomes das variáveis
    
    # Adiciona cada linha da tabela verdade
    for combinacao in combinacoes:
        linha = []
        
        # Adiciona valores para variáveis originais
        for var in variaveis_originais:
            linha.append(str(int(combinacao[variaveis_originais.index(var)])))  

        # Adiciona valores para variáveis negadas
        for var in variaveis_premissa:
            if var.nome.startswith('~'):
                # Encontra o índice da variável original correspondente
                original_var_name = var.nome[1]  # Remove o '~'
                original_var = next(v for v in variaveis_originais if v.nome == original_var_name)
                original_index = variaveis_originais.index(original_var)
                # Adiciona a negação
                linha.append(str(int(not combinacao[original_index])))  

        tabela_verdade.append(linha)

    return tabela_verdade

def imprimir_tabela_verdade(tabela_verdade):
    for linha in tabela_verdade:
        print("\t".join(map(str, linha)))  


def imprimir_variaveis_global():
    print([f"Variável {v.nome} = {v.variavel}" for v in variaveis_global])


def atualizar_e_imprimir_tabela_verdade():
    global tabela_verdade_global  
    tabela_verdade_global = atualiza_tabela_verdade(variaveis_global)  
    imprimir_tabela_verdade(tabela_verdade_global) 


def imprimir_tabela_verdade_epica(tabela_verdade_global, invalido, linha_problematica):
    # Cria uma cópia da tabela verdade sem modificar a original
    tabela_verdade_copia = np.array(tabela_verdade_global)  

    if tabela_verdade_copia.size == 0:
        print("A tabela verdade está vazia!")
        return

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.axis('tight')
    ax.axis('off')

    col_labels = tabela_verdade_copia[0]  
    data = tabela_verdade_copia[1:].astype(int)  

    # Substitui 0 por 'F' e 1 por 'V'
    data_substituida = np.where(data == 0, 'F', 'V')

    data_with_headers = np.vstack((col_labels, data_substituida))  

    table = ax.table(cellText=data_with_headers, cellLoc='center', loc='center')

    for (i, j), cell in table.get_celld().items():
        if i == 0:  
            cell.set_fontsize(14)
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#4CAF50')  
        else:  # Dados
            cell.set_fontsize(12)
            if i == linha_problematica:  
                cell.set_facecolor('#ffcccc')  
            else:
                cell.set_facecolor('#f2f2f2' if (i + j) % 2 == 0 else 'white')  
        cell.set_edgecolor('black')  
        cell.set_linewidth(1)  

    table.auto_set_font_size(False)
    table.scale(1.2, 1.2)  

    if invalido:
        mensagem_validade = "Argumento Inválido."
    else:
        mensagem_validade = "Argumento Válido."

    plt.figtext(0.5, 0.12, mensagem_validade, ha='center', fontsize=12, color='red' if invalido else 'green')

    plt.title('Tabela Verdade', fontsize=16, fontweight='bold')

    plt.show()

################################ FUNÇÕES PROCESSAMENTO DAS FRASES ##############################
def verifica_variavel_negada():
    for i in range(len(variaveis_global)):
        variavel_i_normalizada = variaveis_global[i].variavel.lower().replace("não ", "").strip()

        for j in range(i + 1, len(variaveis_global)):
            variavel_j_normalizada = variaveis_global[j].variavel.lower().replace("não ", "").strip()

            # Verifica se as variáveis são iguais (ou seja, são negações uma da outra)
            if variavel_i_normalizada == variavel_j_normalizada:
                # Renomeia a variável negada com o prefixo ~, mantendo o nome da variável original
                if "não " in variaveis_global[i].variavel.lower():
                    variaveis_global[i].nome = "~" + variaveis_global[j].nome  # A primeira variável (negada) recebe ~B
                else:
                    variaveis_global[j].nome = "~" + variaveis_global[i].nome  # A segunda variável (negada) recebe ~A


def remove_pontuacao(variaveis):
    for variavel in variaveis:
        variavel.variavel = variavel.variavel.replace(",", "").replace(".", "").strip()  # Remove vírgulas e espaços em branco

        
def remove_se(variaveis):
    for variavel in variaveis:
        variavel.variavel = re.sub(r'(^se\s+|(?<=\s)se(?=\s)|(?<=\s)se$)', '', variavel.variavel).strip()



def adicionar_variavel_global(variaveis_premissa):
    letras_existentes = {vr.nome for vr in variaveis_global}  # Coleta letras existentes
    next_letter_index = 65 

    # Enquanto a letra que estamos tentando usar já existir, incrementamos o índice
    while chr(next_letter_index) in letras_existentes:
        next_letter_index += 1

    for nova_variavel in variaveis_premissa:
        # Verifica se a nova variável já existe
        if not any(nova_variavel.variavel == v.variavel for v in variaveis_global):
            nova_variavel.nome = chr(next_letter_index)  # Atribui a letra atual
            variaveis_global.append(nova_variavel)  
            next_letter_index += 1 
        else:
            # A variável já existe, então atribua a letra que ela já tinha
            for v in variaveis_global:
                if v.variavel == nova_variavel.variavel:
                    nova_variavel.nome = v.nome  
                    break


def normalizar_frase(texto):
    doc = nlp(texto)
    tokens_lematizados = []
    skip_next = False

    for i, token in enumerate(doc):
        if skip_next:
            skip_next = False
            continue

        if token.text.lower() == "não" and i + 1 < len(doc):
            next_token = doc[i + 1]
            tokens_lematizados.append(f"não {next_token.lemma_}")
            skip_next = True
        else:
            tokens_lematizados.append(token.lemma_)

    return " ".join(tokens_lematizados)


def extrair_variaveis(premissa):
    #Extrai variáveis e operadores da premissa, adicionando-os à lista global de operadores
    variaveis_premissa = []
    operadores_encontrados = []  

    # Loop pelos operadores lógicos
    for operador in operadores_logicos:
        posicao = premissa.find(operador)
        while posicao != -1:  
            variavel = premissa[:posicao].strip()  # Pega a parte da string antes do operador
            variaveis_premissa.append(Variavel(variavel))  # Adiciona a variável

            operadores_encontrados.append(operador)

            # Atualiza a premissa para continuar a busca
            premissa = premissa[posicao + len(operador):].strip()
            posicao = premissa.find(operador)  # Reencontra o operador na nova string

    # Adiciona a última variável, se existir
    if premissa:
        variaveis_premissa.append(Variavel(premissa.strip()))
    for operador in operadores_encontrados:
        if len(variaveis_premissa) >= 2:
            operadores_globais.append(Operador(operador, variaveis_premissa[-2], variaveis_premissa[-1]))

    if len(variaveis_premissa) == 1:
        operadores_globais.append(Operador("", variaveis_premissa[-1], None))

    return variaveis_premissa


def processar_premissa(premissa):
    global variaveis_global, tabela_verdade_global, operadores_globais  

    variaveis_premissa = extrair_variaveis(premissa)  
    remove_pontuacao(variaveis_premissa)  
    remove_se(variaveis_premissa)

    for variavel in variaveis_premissa:
        variavel.variavel = normalizar_frase(variavel.variavel).lower()
        print(f"VARIÁVEL NORMALIZADA: {variavel.variavel}")

    adicionar_variavel_global(variaveis_premissa)  # Adiciona nomes às variáveis
    verifica_variavel_negada()

################################ FUNÇÕES DA LÓGICA DOS ARGUMENTOS ##############################

def entao(operador, tabela_verdade):
    # Calcula a operação lógica 'A então B' e adiciona o resultado à tabela verdade
    variavel_a = operador.variavel_um.nome 
    variavel_b = operador.variavel_dois.nome

    nova_coluna = []  

    for linha in tabela_verdade[1:]: 
        # Encontra o índice da variável A
        index_a = next(i for i, var in enumerate(tabela_verdade[0]) if var == variavel_a)
        a = bool(int(linha[index_a]))  
        
        # Encontra o índice da variável B
        index_b = next(i for i, var in enumerate(tabela_verdade[0]) if var == variavel_b)
        b = bool(int(linha[index_b]))  
        
        resultado = not a or b  # A operação 'A então B'
        nova_coluna.append(int(resultado))  

    # Adiciona a nova coluna à tabela verdade
    tabela_verdade[0].append(f"{variavel_a} então {variavel_b}")  
    for i, linha in enumerate(tabela_verdade[1:], start=1):
        linha.append(nova_coluna[i - 1])  


def e(operador, tabela_verdade):
    # Calcula a operação lógica 'A e B' e adiciona o resultado à tabela verdade
    variavel_a = operador.variavel_um.nome  
    variavel_b = operador.variavel_dois.nome

    nova_coluna = [] 

    for linha in tabela_verdade[1:]: 
        # Encontra o índice da variável A
        index_a = next(i for i, var in enumerate(tabela_verdade[0]) if var == variavel_a)
        a = bool(int(linha[index_a]))  
        
        # Encontra o índice da variável B
        index_b = next(i for i, var in enumerate(tabela_verdade[0]) if var == variavel_b)
        b = bool(int(linha[index_b])) 
        
        resultado = a and b  
        nova_coluna.append(int(resultado))  

    # Adiciona a nova coluna à tabela verdade
    tabela_verdade[0].append(f"{variavel_a} e {variavel_b}")  
    for i, linha in enumerate(tabela_verdade[1:], start=1):
        linha.append(nova_coluna[i - 1])  

def ou(operador, tabela_verdade):
    # Calcula a operação lógica 'A ou B' e adiciona o resultado à tabela verdade
    variavel_a = operador.variavel_um.nome  
    variavel_b = operador.variavel_dois.nome

    nova_coluna = [] 

    for linha in tabela_verdade[1:]:  
        # Encontra o índice da variável A
        index_a = next(i for i, var in enumerate(tabela_verdade[0]) if var == variavel_a)
        a = bool(int(linha[index_a]))  
        
        # Encontra o índice da variável B
        index_b = next(i for i, var in enumerate(tabela_verdade[0]) if var == variavel_b)
        b = bool(int(linha[index_b]))  
        
        resultado = a or b  
        nova_coluna.append(int(resultado))  

    # Adiciona a nova coluna à tabela verdade
    tabela_verdade[0].append(f"{variavel_a} ou {variavel_b}")  # Adiciona o cabeçalho da nova coluna
    for i, linha in enumerate(tabela_verdade[1:], start=1):
        linha.append(nova_coluna[i - 1])  


def operador_unico(operador, tabela_verdade):
    variavel_a = operador.variavel_um.nome  # Assume que variavel_um é uma instância da classe Variavel

    nova_coluna = []  

    for linha in tabela_verdade[1:]: 
        # Encontra o índice da variável A
        index_a = next(i for i, var in enumerate(tabela_verdade[0]) if var == variavel_a)
        a = bool(int(linha[index_a])) 
        
        resultado = a 
        nova_coluna.append(int(resultado))  

    # Adiciona a nova coluna à tabela verdade
    tabela_verdade[0].append(f"INF {variavel_a}")  
    for i, linha in enumerate(tabela_verdade[1:], start=1):
        linha.append(nova_coluna[i - 1])  


def verifica_premissas_e_conclusao():
    global tabela_verdade_global, variaveis_global
    
    num_colunas_variaveis = len(variaveis_global)  # Número de colunas que contêm variáveis
    num_colunas_total = len(tabela_verdade_global[0])  # Total de colunas na tabela verdade
    num_colunas_premissas = num_colunas_total - num_colunas_variaveis - 1  # Total de colunas de premissas (excluindo a conclusão)

    encontrou_linha_problematica = False  # Variável para rastrear se há alguma linha problemática

    for index, linha in enumerate(tabela_verdade_global[1:], start=1): 
        # Verifica se todas as premissas são verdadeiras (1) e a conclusão é falsa (0)
        todas_premissas_true = all(int(linha[i]) == 1 for i in range(num_colunas_variaveis, num_colunas_variaveis + num_colunas_premissas))
        conclusao_false = int(linha[-1]) == 0  # A última coluna é a conclusão

        if todas_premissas_true and conclusao_false:
            print(f"Encontrada linha problemática na linha {index}: {linha} (todas as premissas verdadeiras, conclusão falsa)")
            encontrou_linha_problematica = True 
            return True, index  

    if not encontrou_linha_problematica:
        print("Nenhuma linha contraditória foi encontrada. As premissas e a conclusão estão corretas.")
        return False, None
        

def processa_conclusao():
    global tabela_verdade_global
    if len(variaveis_global) < 2:
        print("Por favor, adicione pelo menos duas variáveis para a conclusão.")
        return
    conclusao = input("Digite a conclusão:\n").lower()
    processar_premissa(conclusao)
    atualizar_e_imprimir_tabela_verdade()

    for operador in operadores_globais:
        if operador.operador == " então ":
            entao(operador, tabela_verdade_global)
        elif operador.operador == " e ":
            e(operador, tabela_verdade_global)
        elif operador.operador == " ou ":
            ou(operador, tabela_verdade_global)
        elif operador.operador == "":
            operador_unico(operador, tabela_verdade_global)

    # Verifica se existe uma linha onde todas as premissas são True e a conclusão é False
    invalido, linha_problematica = verifica_premissas_e_conclusao()

    if invalido:
        print("True")
    else:
        print("False")
    imprimir_variaveis_global()
    # Imprime a tabela verdade atualizada
    imprimir_tabela_verdade(tabela_verdade_global)
    
    return invalido, linha_problematica


variaveis_global = []
tabela_verdade_global = []
operadores_globais = []


def processar_argumento():
    while True:
        op = input("1 para adicionar uma premissa\n2 para adicionar conclusão\n\n0 para sair\nSelecione uma opção: ")
        if op == "0":
            break
        elif op == "1":
            premissa = input("Digite a premissa:\n").lower()
            processar_premissa(premissa)
            imprimir_variaveis_global()  
            atualizar_e_imprimir_tabela_verdade()
        

        elif op == "2":
            invalido, linha_problematica = processa_conclusao()
            imprimir_tabela_verdade_epica(tabela_verdade_global, invalido, linha_problematica)
            print("Tchau")
            break
       


if __name__ == "__main__":
    processar_argumento()
