from __future__ import annotations
from ACO_PTP import *
import time
import numpy as np

# Testa todas as combinações de parâmetro variando de 0.3 em 0.3 
def teste(graph, alpha, beta, gamma, delta):
    i = 0
    with open("resultados_testes_salvador.txt", "w") as file:
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
    # Definindo a matriz fornecida
    matrix = [
    [0, 9.1, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 14.5, 9.7, float('inf'), float('inf'), float('inf'), float('inf')],
    [9.1, 0, 6.8, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
    [float('inf'), 6.8, 0, 6.1, 8.2, float('inf'), 27, 18.7, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
    [float('inf'), float('inf'), 6.1, 0, 3.7, 9.5, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 2.7, 1.7],
    [float('inf'), float('inf'), 8.2, 3.7, 0, 10.4, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 1.8, 2.3],
    [float('inf'), float('inf'), float('inf'), 9.5, 10.4, 0, 28.2, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 10, 8.7],
    [float('inf'), float('inf'), 27, float('inf'), float('inf'), 28.1, 0, 14.5, float('inf'), float('inf'), float('inf'), 14.4, 33.2, float('inf')],
    [float('inf'), float('inf'), 18.7, float('inf'), float('inf'), float('inf'), 14.5, 0, 6.4, float('inf'), 8.4, 7.3, float('inf'), float('inf')],
    [15.4, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 6.4, 0, 7, 10.8, float('inf'), float('inf'), float('inf')],
    [9.7, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 7, 0, float('inf'), 8.1, float('inf'), float('inf')],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 8.4, 10.8, float('inf'), 0, 6.3, float('inf'), float('inf')],
    [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 14.4, 7.3, float('inf'), 8.1, 6.3, 0, float('inf'), float('inf')],
    [float('inf'), float('inf'), float('inf'), 2.7, 1.8, 10, 33.2, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 0, 2.6],
    [float('inf'), float('inf'), float('inf'), 1.7, 2.3, 8.7, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 2.6, 0]
]

    bonus = [0, 29, 5, 22, 150, 51, 27, 19, 119, 35, 147, 138, 2, 4] 
       
    global ALPHA, BETA, GAMMA, DELTA
    
    graph = create_graph_from_matrices(matrix, bonus)
    
    teste(graph, ALPHA, BETA, GAMMA, DELTA)

if __name__ == "__main__":
    main()