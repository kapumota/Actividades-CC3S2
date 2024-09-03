# Primera parte
import heapq

class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, from_node, to_node, weight):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, weight))

    def dijkstra(self, start_node):
        distances = {node: float('infinity') for node in self.edges}
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        heapq.heapify(priority_queue)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.edges[current_node]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances


# Segunda parte
import heapq

class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, from_node, to_node, weight):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, weight))

    def dijkstra(self, start_node):
        if start_node not in self.edges:
            raise ValueError("El nodo inicial no está en el grafo")

        distances = {node: float('infinity') for node in self.edges}
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        heapq.heapify(priority_queue)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.edges.get(current_node, []):
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

#Tercera parte

import heapq

class Graph:
    def __init__(self):
        """Inicializa un grafo vacío."""
        self.edges = {}

    def add_edge(self, from_node, to_node, weight):
        """
        Agrega una arista dirigida al grafo.
        :param from_node: Nodo de origen.
        :param to_node: Nodo de destino.
        :param weight: Peso de la arista.
        """
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, weight))

    def dijkstra(self, start_node):
        """
        Implementa el algoritmo de Dijkstra para encontrar la distancia más corta desde un nodo inicial.
        :param start_node: Nodo inicial.
        :return: Diccionario de distancias mínimas desde el nodo inicial a todos los demás nodos.
        """
        if start_node not in self.edges:
            raise ValueError("El nodo inicial no está en el grafo")

        distances = {node: float('infinity') for node in self.edges}
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        heapq.heapify(priority_queue)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.edges.get(current_node, []):
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

# git checkout -b feature-negative-weights


# Pesos negativos

def dijkstra(self, start_node):
    """
    Implementa el algoritmo de Dijkstra para encontrar la distancia más corta desde un nodo inicial.
    :param start_node: Nodo inicial.
    :return: Diccionario de distancias mínimas desde el nodo inicial a todos los demás nodos.
    """
    # Chequeo para asegurar que no hay pesos negativos
    for edges in self.edges.values():
        for _, weight in edges:
            if weight < 0:
                raise ValueError("El grafo contiene pesos negativos, Dijkstra no es adecuado")

    if start_node not in self.edges:
        raise ValueError("El nodo inicial no está en el grafo")

    distances = {node: float('infinity') for node in self.edges}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    heapq.heapify(priority_queue)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in self.edges.get(current_node, []):
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


# git checkout main
#git merge feature-negative-weights

# git remote add origin <url-del-repositorio>
#git push -u origin main

