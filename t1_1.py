import spacy
from difflib import SequenceMatcher


nlp = spacy.load('pt_core_news_md')

operadores_logicos = {
    " and ",
    " e ",
    " or ", 
    " ou ", 
    " então ", 
    " then "
}

def similaridade_caracteres(frase1, frase2):
    """Calcula a similaridade entre duas frases."""
    return SequenceMatcher(None, frase1, frase2).ratio()

def verificar_variaveis_existentes(variaveis, variaveis_premissa):
    for vr2 in variaveis_premissa:
        existe = False
        for vr1 in variaveis:
            similaridade = similaridade_caracteres(vr1, vr2)
            if similaridade > 0.95:
                existe = True  # A variável já existe com alta similaridade
                break  # Sai do loop se a similaridade for alta
        if not existe:
            variaveis.append(vr2)  # Adiciona a variável se não existir

def remove_virgula(variaveis):
    """Remove vírgulas de cada variável na lista fornecida."""
    for i in range(len(variaveis)):
        variaveis[i] = variaveis[i].replace(",", "").strip()  # Remove vírgulas e espaços em branco

def processar_premissa(variaveis, premissas):
    variaveis_premissa = []
    operador_premissa = ""
    premissa = input("Digite a premissa:\n")
    posicao = -1

    premissa = premissa.lower()  # Converte a frase para minúsculas

    #for operador in operadores_logicos:
    for operador in operadores_logicos:
        posicao = premissa.find(operador)
        if posicao != -1:
            variavel = premissa[:posicao].strip()  # Pega a parte da string antes do operador
            variaveis_premissa.append(variavel)
            #operador_premissa = operador
            # Remove a parte até o operador encontrado para buscar outras variáveis.
            premissa = premissa[posicao + len(operador):].strip()
            

    # Se nenhum operador for encontrado, adiciona a premissa como uma variável.
    if posicao == -1:
        variaveis_premissa.append(premissa)


    for variavel in variaveis_premissa:
        doc = nlp(variavel)
        tokens = [token.lemma_ for token in doc if not token.is_stop]
        variavel = " ".join(tokens)
    
    remove_virgula(variaveis_premissa)
    print(variaveis_premissa)
    verificar_variaveis_existentes(variaveis, variaveis_premissa)
    print(variaveis)


def processar_argumento():
    variaveis = []
    premissas = []
    conclusao = ""

    while True:
        op = input("1 para adicionar uma premissa\n2 para adicionar conclusão\n0 para sair\nSelecione uma opção: ")
        if op == "0":
            break
        elif 1:
            processar_premissa(variaveis, premissas)
        #elif 2:
           # processar_conclusao(variaveis, premissas, conclusao)
        

def main():
    processar_argumento()

if __name__ == "__main__":
    main()
