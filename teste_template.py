from __future__ import annotations
from ACO_PTP import *
import time
import numpy as np

# Testa todas as combinações de parâmetro variando de 0.3 em 0.3 
def teste(graph, alpha, beta, gamma, delta):
    i = 0
    with open("<INSERIR NOME DO ARQUIVO PARA ESCRITA", "w") as file:
        for alpha in np.arange(0.3, 1, 0.3):
            ALPHA = alpha
            for beta in np.arange(0.3, 1, 0.3):
                BETA = beta
                for gamma in np.arange(0.3, 1, 0.3):
                    GAMMA = gamma
                    for delta in np.arange(0.3, 1, 0.3):
                        i += 1
                        DELTA = delta
                        start_time = time.time()
                        final_path, final_distance, final_bonus = ant_colony(graph)  # Supondo que você tenha a função ant_colony definida
                        end_time = time.time()

                        execution_time = end_time - start_time
                        
                        # Escreve os resultados no arquivo e força a atualização imediata
                        file.write("=================================================================\n")
                        file.write(f"Alpha: {ALPHA}, Beta: {BETA}, Gamma: {GAMMA}, Delta: {DELTA}\n")
                        file.write(f"Tempo de execucao: {execution_time:.4f} segundos\n")
                        file.write(f"Final Path: {final_path}\nTotal Distance: {final_distance}\nTotal Bonus: {final_bonus}\nFinal profit: {final_bonus - final_distance}\n")
                        file.write(f"Iteracao: {i}\n\n")
                        file.write("==================================================================\n")
                        file.flush()  # Força a escrita no disco imediatamente


def main():
    
    # Matriz de pesos (Arestas)
    matrix = "<INSERIR MATRIZ DE PESOS DO GRAFO>"

    # Lista de bônus (Vértices)
    bonus = "<INSERIR LISTA DE BÔNUS DO GRAFO" # a lista de bônus precisa ter a mesma quantidade de colunas da matriz de pesos
       
    global ALPHA, BETA, GAMMA, DELTA
    
    # Cria o grafo
    graph = create_graph_from_matrices(matrix, bonus)

    # Executa os testes
    teste(graph, ALPHA, BETA, GAMMA, DELTA)

if __name__ == "__main__":
    main()