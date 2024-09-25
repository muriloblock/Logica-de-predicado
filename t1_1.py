class ParteCondicional:
    def __init__(self, texto):
        # Inicializa o texto e define o valor booleano baseado na presença de "não"
        self.texto = texto
        self.valor_bool = "não" not in texto.lower()

    def __str__(self):
        return f"{self.texto} (Valor: {self.valor_bool})"


def obter_entrada(prompt):
    """
    Solicita a entrada do usuário e retorna a frase sem espaços no início e fim.
    """
    return input(prompt).strip()


def encontrar_entao(frase):
    """
    Retorna a posição da palavra 'então' na frase.
    """
    return frase.lower().find("então")


def separar_frase(frase, pos_entao):
    """
    Separa a frase condicional em duas partes: antes e depois de 'então',
    e cria objetos ParteCondicional para cada parte.
    """
    parte_p = frase[:pos_entao].strip().replace("se", "").strip().rstrip(",")
    parte_q = frase[pos_entao + len("então"):].strip()

    # Inicializa as partes da frase condicional
    p_condicional = ParteCondicional(parte_p)
    q_condicional = ParteCondicional(parte_q)

    return p_condicional, q_condicional


def processar_frase(prompt):
    """
    Processa uma frase condicional fornecida pelo usuário e retorna as partes 'p' e 'q'.
    """
    frase = obter_entrada(prompt)
    pos_entao = encontrar_entao(frase)

    if pos_entao == -1:
        print(f"A frase fornecida deve conter a palavra 'então'.")
        return None, None

    return separar_frase(frase, pos_entao)


def comparar_frases(p_condicional, q_condicional, p_premissa, q_premissa):
    """
    Compara as partes das frases condicionais e premissas, verificando a equivalência.
    """
    if (p_condicional.texto == p_premissa.texto and q_condicional.texto == q_premissa.texto) or \
       (p_condicional.texto == q_premissa.texto and q_condicional.texto == p_premissa.texto):
        print("\nAs frases são equivalentes em termos de 'p' e 'q', considerando a ordem.")
    else:
        print("\nAs frases não são equivalentes em termos de 'p' e 'q'.")


def exibir_resultados(p_condicional, q_condicional, p_premissa, q_premissa):
    """
    Exibe as partes condicionais e seus valores booleanos.
    """
    print(f"\nFrase Condicional:")
    print(f"Parte p: {p_condicional}")
    print(f"Parte q: {q_condicional}")
    
    print(f"\nPremissa:")
    print(f"Parte p: {p_premissa}")
    print(f"Parte q: {q_premissa}")
    
    # Exibe os objetos com seus valores booleanos atualizados
    print(f"\nParte p (condicional): {p_condicional}")
    print(f"Parte q (condicional): {q_condicional}")
    print(f"Parte p (premissa): {p_premissa}")
    print(f"Parte q (premissa): {q_premissa}")


def imprimir_tabela_verdade():
    """
    Imprime a tabela verdade para a condicional p -> q.
    """
    print("\nTabela Verdade para p -> q:")
    print(f"{'p':<6}{'q':<6}{'p -> q':<8}")
    print("-" * 20)
    
    # As combinações de valores booleanos para p e q
    valores_p = [True, True, False, False]
    valores_q = [True, False, True, False]
    
    # Calcula e imprime a tabela verdade
    for p, q in zip(valores_p, valores_q):
        condicional = not p or q  # p -> q é falso apenas quando p é True e q é False
        print(f"{str(p):<6}{str(q):<6}{str(condicional):<8}")


def inferir_resultado(p_condicional, q_condicional, p_premissa, q_premissa):
    """
    Infere o resultado final baseado na premissa e na condicional.
    Verifica se o valor da condicional bate com a premissa e valida a inferência.
    """
    # Obtém os valores booleanos de p e q da condicional e da premissa
    p_valor = p_premissa.valor_bool
    q_valor = q_premissa.valor_bool
    
    # Calcula o resultado da condicional p -> q
    resultado_condicional = not p_valor or q_valor  # p -> q
    
    print(f"\nInferência:")
    print(f"p (premissa) = {p_valor}, q (premissa) = {q_valor}")
    print(f"Resultado da condicional (p -> q): {resultado_condicional}")
    
    # Verifica a validade da inferência
    if p_valor and not q_valor:
        print("A inferência é inválida, pois 'p' é verdadeiro e 'q' é falso.")
    else:
        print("A inferência é válida.")


def main():
    # Processa a frase condicional e a premissa
    p_condicional, q_condicional = processar_frase("Digite a frase condicional no formato 'se [condição], então [resultado]': ")
    if not p_condicional or not q_condicional:
        return
    
    p_premissa, q_premissa = processar_frase("Digite a premissa no formato 'se [condição], então [resultado]': ")
    if not p_premissa or not q_premissa:
        return

    # Compara as frases e exibe os resultados
    exibir_resultados(p_condicional, q_condicional, p_premissa, q_premissa)
    comparar_frases(p_condicional, q_condicional, p_premissa, q_premissa)
    
    # Imprime a tabela verdade
    imprimir_tabela_verdade()
    
    # Inferir o resultado baseado na premissa e na condicional
    inferir_resultado(p_condicional, q_condicional, p_premissa, q_premissa)


if __name__ == "__main__":
    main()
