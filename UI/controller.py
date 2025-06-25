import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._shape = None
        self._year = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        if self._shape is None or self._year is None:
            self._view.txt_result1.controls.append(ft.Text(f"Selezionare un anno e una forma."))
            self._view.update_page()
            return
        self._model.buildGraph(self._year, self._shape)
        archi, nodi = self._model.getInfoGraph()
        self._view.txt_result1.controls.append(ft.Text(f"Nodi {nodi}, archi {archi}"))
        peggiori = self._model.getWorse()
        for peggiore in peggiori:
            self._view.txt_result1.controls.append(ft.Text(f"{peggiore[0].id}-{peggiore[1].id} {peggiore[2]}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        if not self._model.existsGraph():
            self._view.txt_result2.controls.append(ft.Text(f"Prima di procedere creare il grafo."))
            self._view.update_page()
            return
        percorso, punteggio = self._model.getPath()
        self._view.txt_result2.controls.append(ft.Text(f"Punteggio {punteggio}"))
        for p in percorso:
            self._view.txt_result2.controls.append(ft.Text(f"{p.id}"))
        self._view.update_page()

    def fill_ddyear(self):
        self._view.ddyear.options.clear()
        for year in self._model.getYears():
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def fill_ddshape(self, e):
        self._view.ddshape.options.clear()
        self._year = self._view.ddyear.value
        for shape in self._model.getShapes(self._year):
            self._view.ddshape.options.append(ft.dropdown.Option(key=shape, data=shape, on_click=self.pickShape))
        self._view.update_page()

    def pickShape(self, e):
        self._shape = e.control.data



