import flet as ft
import networkx as nx
from model.team import Team


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model

    def fillDD(self):
        listYears = self.model.passYears()
        for year in listYears:
            self.view.ddYear.options.append(ft.dropdown.Option(key=year, text=year))
        self.view.update_page()

    def fillDDTeams(self):
        if self.view.ddYearValue is not None:
            self.view._txtOutSquadre.clean()
            year = int(self.view.ddYearValue)
            listTeams = self.model.passTeams(year)
            self.view._txtOutSquadre.controls.append(ft.Text(f"Squadre presenti nell'anno {year} = {len(listTeams)}"))
            for team in listTeams:
                self.view.ddTeams.options.append(ft.dropdown.Option(key=team.teamCode, text=team.__str__()))
                self.view._txtOutSquadre.controls.append(ft.Text(team.__str__()))
            self.view.update_page()
        else:
            self.view._txtOutSquadre.controls.append(ft.Text(f"Seleziona un anno"))
            self.view.update_page()


    def handleCreaGrafo(self, e):
        self.view._txt_result.clean()
        year = int(self.view.ddYearValue)
        self.model.createGraph(year)
        graph = self.model.graph
        self.view._txt_result.controls.append(ft.Text(f"Il numero di vertici è: {graph.number_of_nodes()}, il numero di archi è: {graph.number_of_edges()} "))
        self.view.update_page()

    def handleDettagli(self, e):
        self.view._txt_result.clean()
        graph = self.model.graph
        sourceId = self.view.ddTeamsValue
        listEdgesNeigh = []
        source = self.model.idMapTeams[sourceId]
        for successor in graph.neighbors(source):
            weight = graph.get_edge_data(source, successor).get('weight', 0)
            listEdgesNeigh.append((source, successor, weight))
        listEdgesNeigh.sort(key=lambda x: x[2], reverse=True)

        for i in range(0, len(listEdgesNeigh)-1):
            print(listEdgesNeigh[i][1].__str__())
            print(listEdgesNeigh[i][2])
            successor = listEdgesNeigh[i][1].__str__()
            weight = listEdgesNeigh[i][2]
            self.view._txt_result.controls.append(ft.Text(f"{successor}      {weight} "))
        self.view.update_page()



    def handlePercorso(self, e):
        self.view._txt_result.clean()
        graph = self.model.graph
        optPath, optPathPoints = self.model.getOptPath(self.view.ddTeamsValue)
        self.view._txt_result.controls.append(ft.Text(
            f"Peso del percorso ottimo: {optPathPoints}"))

        for i in range(0, len(optPath)-1):
            self.view._txt_result.controls.append(ft.Text(f"{optPath[i].__str__()} --> {optPath[i+1].__str__()} | weight: {graph.get_edge_data(optPath[i], optPath[i+1]).get('weight', 0)}"))

        self.view.update_page()











