import random

class Grafo:
    def __init__(self, vertices, arestas, custos, bonus):
        self.vertices = vertices  
        self.arestas = arestas    
        self.custos = custos      
        self.bonus = bonus        

    def descobrirVizinhos(self, vertice):
        listaVizinhos = []
        for aresta in self.arestas:
            if vertice in aresta.vertices:
                vizinho = aresta.vertices[1] if aresta.vertices[0] == vertice else aresta.vertices[0]
                if vizinho not in listaVizinhos:
                    listaVizinhos.append(vizinho)
        return listaVizinhos

    def espelhar(self, v1, v2):
        for aresta in self.arestas:
            if (v1, v2) == aresta.vertices or (v2,v1) == aresta.vertices:
                return aresta
        return None

    def imprimirVertices(self):
        for vertice in self.vertices:
            print(f"Vértice {vertice.index}: Bonus {vertice.bonus}")

    def imprimirArestas(self):
        for aresta in self.arestas:
            print(f"Aresta: {aresta.vertices[0].index} - {aresta.vertices[1].index} | Custo: {aresta.custo}")

    def iniciaFeromonios(self, feromonioArestasInicial, feromoniosVerticesInicial):
        feromoniosArestas = {}
        feromoniosVertices = {}

        for aresta in self.arestas:
            feromoniosArestas[aresta] = feromonioArestasInicial
        for vertice in self.vertices:
            feromoniosVertices[vertice] = feromoniosVerticesInicial
        return feromoniosArestas, feromoniosVertices

    def construcaoDaSolucao(self, feromoniosArestas, feromoniosVertices, alpha, beta, custoLimite):
        verticeAtual = self.vertices[0]
        caminhoPercorrido = [verticeAtual]
        premioTotal = verticeAtual.bonus
        custoTotal = 0

        while True:
            vizinhos = self.descobrirVizinhos(verticeAtual)
            possibilidadesDeEscolha = []

            for vizinho in vizinhos:
                if vizinho not in caminhoPercorrido:
                    arestaAtual = self.espelhar(verticeAtual, vizinho)
                    if arestaAtual:
                        feromonioAresta = feromoniosArestas[arestaAtual] ** alpha 
                        feromonioVertice = feromoniosVertices[vizinho] ** alpha
                        custo = arestaAtual.custo
                        if custoTotal + custo <= custoLimite:
                            distancia = (1 / (custo )) ** beta

                            atratividade = feromonioAresta * feromonioVertice * distancia * vizinho.bonus
                            possibilidadesDeEscolha.append((vizinho, atratividade))

            if not possibilidadesDeEscolha:
                aresta = self.espelhar(self.vertices[0], verticeAtual)
                if aresta:
                    custoTotal += aresta.custo
                break

            somaProbabilidades = sum(prob for _, prob in possibilidadesDeEscolha)
            escolhasNormalizadas = [(v, prob / somaProbabilidades) for v, prob in possibilidadesDeEscolha]
            print(escolhasNormalizadas)
            escolha = random.choices([v for v, _ in escolhasNormalizadas], weights=[p for _, p in escolhasNormalizadas])[0]

            arestaEscolhida = self.espelhar(verticeAtual, escolha)
            custoTotal += arestaEscolhida.custo
            premioTotal += escolha.bonus
            caminhoPercorrido.append(escolha)
            verticeAtual = escolha

        return caminhoPercorrido, premioTotal, custoTotal

    def renovaFeromonios(self, feromoniosArestas, feromoniosVertices, Q, sigma, caminhos):
        for aresta in self.arestas:
            feromoniosArestas[aresta] *= (1 - sigma)
        for vertice in self.vertices:
            feromoniosVertices[vertice] *= (1 - sigma)

        for caminho, premio, custo in caminhos:
            for i in range(len(caminho) - 1):
                aresta = self.espelhar(caminho[i], caminho[i + 1])
              
                if aresta:
                    feromoniosArestas[aresta] += Q / (custo )
            for vertice in caminho:
                feromoniosVertices[vertice] += (Q  / (custo )) +( premio / custo)

    def aco(self, numFormigas, numIteracoes, alpha, beta, custoLimite, Q, sigma, feromonioInicial):
        melhorCaminho = None
        melhorPremio = 0
        feromoniosArestas, feromoniosVertices = self.iniciaFeromonios(feromonioInicial, feromonioInicial)
        melhorCusto = 10000

        for _ in range(numIteracoes):
            print(f'{_} iteração')
            caminhos = []
            for _ in range(numFormigas):
                caminho, premio, custo = self.construcaoDaSolucao(feromoniosArestas, feromoniosVertices, alpha, beta, custoLimite)
                caminhos.append((caminho, premio, custo))
                if premio > melhorPremio:
                     melhorPremio = premio
                     melhorCaminho = caminho
                     melhorCusto = custo
                
                

            self.renovaFeromonios(feromoniosArestas, feromoniosVertices, Q, sigma, caminhos)

        return melhorCaminho, melhorPremio, melhorCusto

class Aresta:
    def __init__(self, v1, v2, custo):
        self.vertices = (v1, v2)
        self.custo = custo

class Vertice:
    def __init__(self, bonus, index):
        self.bonus = bonus
        self.index = index

    def __repr__(self):
        return f"V({self.index})"
bonus = [0, 29, 5, 22, 150, 51, 27, 19, 119, 35, 147, 138, 2, 4]
vertices = [Vertice(b, i) for i, b in enumerate(bonus)]

# Matriz de adjacência
matriz_adjacencia = [
    [float('inf'), 9.1, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 15.4, 9.7, float('inf'), float('inf'), float('inf'), float('inf')],
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
    [float('inf'), float('inf'), float('inf'), 2.7, 1.8, 10, 33.2, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 0, 2.6],
    [float('inf'), float('inf'), float('inf'), 1.7, 2.3, 8.7, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 2.6, 0]
]

arestas = []
for i in range(len(matriz_adjacencia)):
    for j in range(i + 1, len(matriz_adjacencia[i])):
        if matriz_adjacencia[i][j] != float('inf'):
            arestas.append(Aresta(vertices[i], vertices[j], matriz_adjacencia[i][j]))

grafo = Grafo(vertices, arestas, custos=None, bonus=bonus)


melhorCaminho, melhorPremio, melhorCusto = grafo.aco(
    numFormigas=10,
    numIteracoes=20,
    alpha=1,
    beta=1,
    custoLimite=5000,
    Q=10,
    sigma=0.1,
    feromonioInicial=1,
)

print("Melhor Caminho:", [v.index for v in melhorCaminho])
print("Melhor Prêmio:", melhorPremio)
print(f"Custo {melhorCusto}")
