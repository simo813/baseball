import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.optPathPoints = None
        self.optPath = None
        self.DAO = DAO()
        self.idMapTeams = {}
        self.graph = None


    def passYears(self):
        listYears = self.DAO.getYears()
        return listYears

    def passTeams(self, year):
        self.idMapTeams = {}
        listTeams = self.DAO.getTeams(year)
        for team in listTeams:
            self.idMapTeams[team.teamCode] = team
        return listTeams

    def createGraph(self, year):
        listTeams = self.DAO.getTeams(year)
        listEdges = self.DAO.getEdges(year)
        self.graph = nx.Graph()
        self.graph.add_nodes_from(listTeams)
        for edge in listEdges:
            weight = self.idMapTeams[edge[0]].salaries + self.idMapTeams[edge[1]].salaries
            self.graph.add_edge(self.idMapTeams[edge[0]], self.idMapTeams[edge[1]], weight = weight)


    def getOptPath(self, sourceId):
        self.optPath = []
        self.optPathPoints = 0
        source = self.idMapTeams[sourceId]

        self.recursion(
            source=source,
            partial=[source],
            partialPoints=0,
            weightPrec = 0
        )
        print("\nENTRATO\n")
        print(self.optPath)
        print(self.optPathPoints)
        print("\nFINE\n")

        return self.optPath, self.optPathPoints

    def recursion(self, source, partial, partialPoints, weightPrec):
        graph = self.graph

        if partialPoints > self.optPathPoints:
            print("\n---------------------------------")
            print(partialPoints)
            self.optPathPoints = partialPoints
            self.optPath = copy.deepcopy(partial)


        for successor in graph.neighbors(source):
            if successor not in partial:
                weightActual = graph.get_edge_data(source, successor).get('weight', 0)
                if weightPrec == 0:
                    print("Prima iterazione")
                    partial.append(successor)
                    self.recursion(successor, partial, partialPoints + weightActual, weightActual)
                    print("NUOVA RICORSIONE\n")
                    partial.pop()
                elif weightActual < weightPrec:
                    print("successore ha peso decrescente")
                    partial.append(successor)
                    self.recursion(successor, partial, partialPoints + weightActual, weightActual)
                    print("NUOVA RICORSIONE\n")
                    partial.pop()




