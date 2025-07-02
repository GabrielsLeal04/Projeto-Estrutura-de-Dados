import networkx as nx
import matplotlib.pyplot as plt
import heapq

class Vertice:
    def __init__(self, valor):
        self.valor = valor
        self.visitado = False

class Grafo:
    def __init__(self, vertices, matriz_adjacencia):
        self.vertices = vertices
        self.matriz_adjacencia = matriz_adjacencia

    def inserir_vertice(self, valor):
        for vertice in self.vertices:
            if vertice.valor == valor:
                print('Vértice já existente!')
                return

        vertex = Vertice(valor)
        self.vertices.append(vertex)

        for linha in self.matriz_adjacencia:
            linha.append(0)

        novo_tamanho = len(self.vertices)
        nova_linha = [0] * novo_tamanho
        self.matriz_adjacencia.append(nova_linha)

        print(f"\n---> Vértice '{valor}' inserido com sucesso!")

    def _encontrar_indice_do_vertice(self, valor_procurado):
        for i, vertice in enumerate(self.vertices):
            if vertice.valor == valor_procurado:
                return i
        return None

    def adicionar_aresta(self, valor_origem, valor_destino, peso=1):
        indice_origem = self._encontrar_indice_do_vertice(valor_origem)
        indice_destino = self._encontrar_indice_do_vertice(valor_destino)

        if indice_origem is None or indice_destino is None:
            print("Um ou ambos os vértices não existem no grafo.")
            return

        self.matriz_adjacencia[indice_origem][indice_destino] = peso
        self.matriz_adjacencia[indice_destino][indice_origem] = peso

        print(f"\n---> Aresta adicionada entre '{valor_origem}' e '{valor_destino}' com peso {peso}")

    def exibir_matriz(self):
        print("\n--- Matriz de Adjacência ---")
        for linha in self.matriz_adjacencia:
            print(linha)

    def plotar_grafo(self):

      G = nx.Graph()

      # Adiciona nós
      for vertice in self.vertices:
          G.add_node(vertice.valor)

      # Adiciona arestas com pesos
      for i in range(len(self.vertices)):
          for j in range(i, len(self.vertices)):
              peso = self.matriz_adjacencia[i][j]
              if peso > 0:
                  G.add_edge(self.vertices[i].valor, self.vertices[j].valor, weight=peso)

      pos = nx.spring_layout(G, seed=42)

      # 1. Centralidade de grau → define o tamanho dos nós
      centralidade = nx.degree_centrality(G)
      tamanhos = [1000 + 4000 * centralidade[no] for no in G.nodes()]  # escala ajustável

      # 2. Cores manuais por grupo
      grupo_cores = {
          "Miguel": "skyblue",
          "Johnny": "skyblue",
          "Daniel": "lightgreen",
          "Chozen": "lightgreen",
          "Samantha": "lightgreen",
          "Robby": "lightgreen",
          "Tory": "salmon",
          "Hawk": "salmon",
          "Kreese": "salmon",
          "Terry Silver": "salmon",
          "Kyler": "salmon",
          "Kenny": "salmon"
      }
      cores = [grupo_cores.get(no, "gray") for no in G.nodes()]

      # 3. Desenha o grafo
      plt.figure(figsize=(10, 8))
      nx.draw(G, pos, with_labels=True,
              node_color=cores,
              node_size=tamanhos,
              font_size=12,
              font_weight='bold',
              edge_color='gray',
              width=2)

      # Rótulos dos pesos
      edge_labels = nx.get_edge_attributes(G, 'weight')
      nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

      plt.title("Rede de Personagens - Cobra Kai", size=18)
      plt.tight_layout()
      plt.show()

    def resetar_visitados(self):
        for vertice in self.vertices:
            vertice.visitado = False

    def dfs_recursiva(self, valor_inicial):
        indice_inicial = self._encontrar_indice_do_vertice(valor_inicial)
        if indice_inicial is None:
            print("Vértice inicial não encontrado.")
            return
        print(f"\n--- DFS a partir de '{valor_inicial}' ---")
        self._dfs_recursiva_aux(indice_inicial)

    def _dfs_recursiva_aux(self, indice_atual):
        vertice_atual = self.vertices[indice_atual]
        vertice_atual.visitado = True
        print(f"Visitando: {vertice_atual.valor}")

        for i, peso in enumerate(self.matriz_adjacencia[indice_atual]):
            if peso > 0 and not self.vertices[i].visitado:
                self._dfs_recursiva_aux(i)

    def dijkstra(self, origem, destino):
        origem_idx = self._encontrar_indice_do_vertice(origem)
        destino_idx = self._encontrar_indice_do_vertice(destino)

        if origem_idx is None or destino_idx is None:
            print("Um ou ambos os vértices não existem.")
            return

        distancias = [float('inf')] * len(self.vertices)
        anteriores = [None] * len(self.vertices)
        distancias[origem_idx] = 0
        heap = [(0, origem_idx)]

        while heap:
            dist_atual, idx_atual = heapq.heappop(heap)

            for vizinho_idx, peso in enumerate(self.matriz_adjacencia[idx_atual]):
                if peso > 0:
                    nova_dist = dist_atual + peso
                    if nova_dist < distancias[vizinho_idx]:
                        distancias[vizinho_idx] = nova_dist
                        anteriores[vizinho_idx] = idx_atual
                        heapq.heappush(heap, (nova_dist, vizinho_idx))

        # Reconstruindo o caminho
        caminho = []
        atual = destino_idx
        while atual is not None:
            caminho.insert(0, self.vertices[atual].valor)
            atual = anteriores[atual]

        print(f"\n--- Dijkstra: caminho mais curto de '{origem}' até '{destino}' ---")
        print(f"Caminho: {caminho}")
        print(f"Distância total: {distancias[destino_idx]}")


    def analisar_rede(self):
      """
      Calcula e exibe métricas da Ciência das Redes.
      """
      G = nx.Graph()

      # Adiciona nós e arestas com pesos
      for i in range(len(self.vertices)):
          G.add_node(self.vertices[i].valor)
          for j in range(i, len(self.vertices)):
              peso = self.matriz_adjacencia[i][j]
              if peso > 0:
                  G.add_edge(self.vertices[i].valor, self.vertices[j].valor, weight=peso)

      print("\n--- MÉTRICAS DA REDE ---")

      # Grau dos nós
      graus = dict(G.degree())
      print("\nGrau dos nós:")
      for no, grau in graus.items():
          print(f"{no}: {grau}")

      # Centralidade de grau
      centralidade = nx.degree_centrality(G)
      print("\nCentralidade de Grau (valores entre 0 e 1):")
      for no, cent in centralidade.items():
          print(f"{no}: {cent:.2f}")

      # Componentes conectados
      componentes = list(nx.connected_components(G))
      print(f"\nComponentes conectados: {len(componentes)}")
      for i, comp in enumerate(componentes, 1):
          print(f"Componente {i}: {comp}")

      # Diâmetro da rede (só se for conectada)
      if nx.is_connected(G):
          diam = nx.diameter(G)
          print(f"\nDiâmetro da rede: {diam}")
      else:
          print("\nA rede não é totalmente conectada, então o diâmetro não pode ser calculado.")

nomes = [
    # Protagonistas e Alunos Principais
    "Miguel", "Robby", "Samantha", "Hawk", "Tory", "Demetri", "Kenny",
    # Senseis
    "Johnny", "Daniel", "Kreese", "Chozen", "Terry Silver",
    # Família
    "Amanda", "Carmen", "Anthony",
    # Personagens Secundários
    "Kyler", "Moon", "Yasmine", "Stingray", "Shawn"
]

vertices = [Vertice(nome) for nome in nomes]
matriz = [[0]*len(vertices) for _ in range(len(vertices))]

# Criar o grafo
g = Grafo(vertices, matriz)

# Adicionar arestas com pesos (quanto menor o peso, mais forte a relação)

# Relações (Peso 1)
g.adicionar_aresta("Miguel", "Johnny", 1)
g.adicionar_aresta("Robby", "Daniel", 1)
g.adicionar_aresta("Samantha", "Daniel", 1)
g.adicionar_aresta("Kreese", "Tory", 1)
g.adicionar_aresta("Chozen", "Daniel", 1)
g.adicionar_aresta("Terry Silver", "Kenny", 1)
g.adicionar_aresta("Amanda", "Daniel", 1)
g.adicionar_aresta("Carmen", "Johnny", 1)
g.adicionar_aresta("Carmen", "Miguel", 1)

# Relações de Amizade(Peso 2)
g.adicionar_aresta("Miguel", "Hawk", 2)
g.adicionar_aresta("Samantha", "Miguel", 2) 
g.adicionar_aresta("Hawk", "Demetri", 2)   
g.adicionar_aresta("Johnny", "Daniel", 2)   
g.adicionar_aresta("Kreese", "Terry Silver", 2) 
g.adicionar_aresta("Moon", "Samantha", 2)
g.adicionar_aresta("Moon", "Yasmine", 2)

# Relações de Rivalidade ou Conexões Fracas (Peso 3 a 5)
g.adicionar_aresta("Miguel", "Robby", 4)      
g.adicionar_aresta("Samantha", "Tory", 5)    
g.adicionar_aresta("Johnny", "Kreese", 4)     
g.adicionar_aresta("Daniel", "Kreese", 5)     
g.adicionar_aresta("Daniel", "Terry Silver", 5) 
g.adicionar_aresta("Kenny", "Anthony", 4)    
g.adicionar_aresta("Kyler", "Hawk", 3)
g.adicionar_aresta("Stingray", "Kreese", 3)
g.adicionar_aresta("Robby", "Shawn", 3)      

g.plotar_grafo()

# Executar as análises
g.dfs_recursiva("Terry Silver")

g.resetar_visitados()

g.dijkstra("Kenny", "Amanda")

g.analisar_rede()

g.exibir_matriz()
