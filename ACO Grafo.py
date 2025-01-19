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
                # if premio > melhorPremio:
                  #  melhorPremio = premio
                  #  melhorCaminho = caminho
                  # melhorCusto = custo
                valor = premio/custo
                valorAntigo = melhorPremio/melhorCusto
                print(valor, valorAntigo)
                if valor > valorAntigo:
                    melhorCaminho = caminho
                    melhorPremio = premio
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

vertices = [Vertice(bonus=i+1 if i==1 else i, index=i) for i in range(10)]

arestas = [Aresta(v1=vertices[i], v2=vertices[i+1], custo=i+1) for i in range(9)] 

arestas.append(Aresta(vertices[0], vertices[2], 4))  # Aresta entre V0 e V2
arestas.append(Aresta(vertices[1], vertices[2], 3))  # Aresta entre V0 e V2
arestas.append(Aresta(vertices[0], vertices[1], 4))  # Aresta entre V0 e V2
arestas.append(Aresta(vertices[9], vertices[6], 6))  # Aresta entre V0 e V2
arestas.append(Aresta(vertices[9], vertices[7], 6))  # Aresta entre V0 e V2


arestas.append(Aresta(vertices[8], vertices[4], 8))  # Aresta entre V0 e V2




for aresta in arestas:
    print(f"Aresta entre V{aresta.vertices[0].index} e V{aresta.vertices[1].index}")
for bonus in vertices:
    print(bonus.bonus)
grafo = Grafo(vertices, arestas, custos=None, bonus=None)

melhorCaminho, melhorPremio, melhorCusto= grafo.aco(
    numFormigas=1,
    numIteracoes=1,
    alpha=2,
    beta=2,
    custoLimite=2000,
    Q=10,
    sigma=0.1,
    feromonioInicial=1,
)

print("Melhor Caminho:", [v.index for v in melhorCaminho])
print("Melhor Prêmio:", melhorPremio)
print(f"Custo {melhorCusto}")