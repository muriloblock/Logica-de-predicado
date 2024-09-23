class ParteCondicional:
    def __init__(self, texto):
        self.texto = texto
        # Define o valor booleano como False se a palavra "não" estiver presente
        self.valor_bool = False if "não" in texto.lower() else True

    def __str__(self):
        return f"{self.texto} (Valor: {self.valor_bool})"


def obter_entrada(prompt):
    """
    Solicita a entrada do usuário e retorna a frase.
    """
    return input(prompt).strip()


def encontrar_entao(frase):
    """
    Encontra a posição da palavra 'então' na frase condicional.
    """
    return frase.lower().find("então")


def separar_frase(frase, pos_entao):
    """
    Separa a frase condicional em duas partes: antes e depois de 'então'.
    Cria objetos ParteCondicional para cada parte.
    """
    parte_p = frase[:pos_entao].strip().replace("se", "").strip().rstrip(",").strip()
    parte_q = frase[pos_entao + len("então"):].strip()
    
    # Inicializa ambas as partes com o valor booleano ajustado com base na palavra "não"
    p_condicional = ParteCondicional(parte_p)
    q_condicional = ParteCondicional(parte_q)
    
    return p_condicional, q_condicional


def main():
    # Solicita as frases condicionais
    frase_condicional = obter_entrada("Digite a frase condicional no formato 'se [condição], então [resultado]': ")
    premissa = obter_entrada("Digite a premissa no formato 'se [condição], então [resultado]': ")
    
    # Processa a frase condicional
    pos_entao = encontrar_entao(frase_condicional)
    
    if pos_entao == -1:
        print("A frase condicional deve conter a palavra 'então'.")
        return

    p_condicional, q_condicional = separar_frase(frase_condicional, pos_entao)
    
    # Processa a premissa
    pos_entao_premissa = encontrar_entao(premissa)
    
    if pos_entao_premissa == -1:
        print("A premissa deve conter a palavra 'então'.")
        return

    p_premissa, q_premissa = separar_frase(premissa, pos_entao_premissa)
    
    # Exibe os resultados
    print(f"Frase Condicional:")
    print(f"Parte p: {p_condicional}")
    print(f"Parte q: {q_condicional}")
    
    print(f"\nPremissa:")
    print(f"Parte p: {p_premissa}")
    print(f"Parte q: {q_premissa}")
    
    # Compara as partes das frases considerando a possibilidade de inversão
    if (p_condicional.texto == p_premissa.texto and q_condicional.texto == q_premissa.texto) or \
       (p_condicional.texto == q_premissa.texto and q_condicional.texto == p_premissa.texto):
        print("\nAs frases são equivalentes em termos de 'p' e 'q', considerando a ordem.")
    else:
        print("\nAs frases não são equivalentes em termos de 'p' e 'q'.")
    
    # Exibe os objetos com seus valores booleanos atualizados
    print(f"\nParte p (condicional): {p_condicional}")
    print(f"Parte q (condicional): {q_condicional}")
    print(f"Parte p (premissa): {p_premissa}")
    print(f"Parte q (premissa): {q_premissa}")


if __name__ == "__main__":
    main()
