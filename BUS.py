pontos = ["FIAP","Parque","Shopping","Metro"]
referencias = [21,45,60,100]#quantidade estimida pre estabelecida no ponto -
                            
registros = []

def calc_prioridade(pessoas,referencia,onibus,patio,pico):
    prioridade = 0
    capacidade = onibus * 40 #capacidade de 40 conforme padrão de micro-onibus para poder fazer uma simulação
    
    #ref
    if pessoas > referencia *1.5: #se pessoas ultrapassar 150% da ref adiciona 3
        prioridade += 3
    elif pessoas > referencia: #se ultrapassar ref adiciona só 2
        prioridade += 2
        
    #cap
    if pessoas > capacidade:
        prioridade += 3
    elif pico and pessoas >= capacidade * 0.8: # 80% da capacidade e no horario de pico
        prioridade += 2                        # (valor aleatório relacionado a demanda, poderia ser 90% tbm)
    
    #pico
    if pico:
        prioridade += 2
        
    #classificação de prioridades com base nos pontos
    if prioridade >= 6:
        return "ALTA"
    elif prioridade >= 3:
        return "MÉDIA"
    else:
        return "BAIXA"
        
########################
   
def cadastrar():
    print("\nEscolha o ponto:")
    for i in range(4):
        print(i + 1, "-", pontos[i])

    escolha = int(input("Ponto: "))
    pessoas = int(input("Quantidade de pessoas: "))
    horario = int(input("Horario (ex: 13): "))
    onibus = int(input("Ônibus em circulação: "))
    patio = int(input("Ônibus parados: "))

    pico = (6 <= horario <= 9 or 17 <= horario <= 20) #horarios de pico médio por SP
                                                      #6h - 9h .... 17h - 20h
    prioridade = calc_prioridade(
        pessoas, referencias[escolha-1],
        onibus, patio, pico
    )

    registros.append([ 
        pontos[escolha-1], pessoas, horario,
        onibus, patio, prioridade, pico
    ])

    print("\nPrioridade:", prioridade)

    if pessoas > onibus * 40 or (pico and pessoas >= onibus * 40 * 0.8):
        if patio > 0:
            print("Recomendação: Enviar ônibus do pátio.")
        else:
            print("Recomendação: Solicitar mais ônibus para o local.") 
    else:
        print("Recomendação: Não há necessidade de ação,frota suficiente.")
        
################### 

def relatorio():
    if len(registros) == 0:
        print("\nNenhum registro cadastrado.")
    else:
        total = 0
        alta = 0

        print("\n======= RELATÓRIO =======")
        for r in registros:         
            print("\nPonto:", r[0])
            print("Passageiros:", r[1])
            print("Horário:", r[2])
            print("Ônibus em circulacao:", r[3])
            print("Ônibus parados:", r[4])
            print("Prioridade:", r[5])

            total += r[1]

            if r[5] == "ALTA":
                alta += 1

        print("\n======= INDICADORES =======")
        print("Total de passageiros:", total)
        print("Média de passageiros:", total / len(registros))
        print("Registros de alta prioridade:", alta)

        if alta > 0:
            print("Conclusão: existem pontos que precisam de atenção urgente") 
        else:                                                      
            print("Conclusão: Nenhum ponto apresenta alta prioridade.")
            
##################

while True:

    print("\n======= CITIZEN TECH =======")
    print("--- BUS NOW ---")
    print("1 - Cadastrar dados")
    print("2 - Consultar relatorio")
    print("3 - Encerrar")

    escolha = input("\nEscolha: ")

    if escolha == "1":
        cadastrar()

    elif escolha == "2":
        relatorio()

    elif escolha == "3":
        print("Encerrando o programa...")
        quit()

