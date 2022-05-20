class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
        #print("sptSet2", sptSet)
        # Initialize minimum distance for next node
        min = 1e7

        #print("self.V", self.V)

        # Search not nearest vertex not in the
        # shortest path tree
        min_index = 0
        for v in range(self.V):
            # print(v)
            # print(sptSet[v])

            # A donde puedo ir con distancia mínima y que no haya ido antes
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        # dist: Vector con valores iniciales de distancia infinitos.
        dist = [1e7] * self.V
        dist[src] = 0  # la distancia del nodo inicial a sí mismo es cero
        # sptSet: Vector con valores iniciales False de dimensión V
        sptSet = [False] * self.V

        #print("sptSet1: ", sptSet)

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            # Se actualiza la distancia u,v si esta es inferior a la distancia actual para llegar a v, si v no ha sido visitada aún y si u y v son adjacentes (hay distancia)
            # Esto se hace para todos los v del rango de vértices.
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                   sptSet[v] == False and
                   dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]

        self.printSolution(dist)
