import copy
from calendar import month
from datetime import datetime

from database.DAO import DAO
import networkx as nx



class Model:
    def __init__(self):
        self._punteggio = 0
        self._percorso = None
        self._nodes = list()
        self._idNodes = dict()
        self._edges = list()
        self._edgesList = list()
        self._graph = None

    def getYears(self):
        return DAO.getYears()

    def getShapes(self, year):
        return DAO.getShapes(year)

    def buildGraph(self, year, shape):
        self._graph = nx.DiGraph()
        self._nodes = DAO.getNodes(year, shape)
        for node in self._nodes:
            self._idNodes[node.id] = node
        self._edges = DAO.getEdges(year, shape, self._idNodes)
        self._graph.add_nodes_from(self._nodes)
        for edge in self._edges:
            self._graph.add_edge(edge.n1, edge.n2, weight=edge.weight)
            self._edgesList.append((edge.n1, edge.n2, edge.weight))

    def getInfoGraph(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getWorse(self):
        sort_list(self._edgesList)
        return self._edgesList[:5]

    def existsGraph(self):
        if self._graph is None:
            return False
        return True

    def getPath(self):
        for nodo in self._nodes:
            self.ricorsione([nodo])
        return self._percorso, self._punteggio

    def ricorsione(self, parziale):
        if self.condizioneFinale(parziale):
            punteggio = self.calcolaPunteggio(parziale)
            if punteggio > self._punteggio:
                self._punteggio = punteggio
                self._percorso = copy.deepcopy(parziale)
        else:
            for nodo in self._graph.neighbors(parziale[-1]):
                if self.condizione(parziale, nodo):
                    parziale.append(nodo)
                    self.ricorsione(parziale)
                    parziale.pop()

    def condizione(self, parziale, nodo):
        if nodo in parziale:
            return False
        if len(parziale) == 1:
            return True
        peso1 = parziale[-1].duration
        peso2 = nodo.duration
        if peso1 > peso2:
            return False
        mese = nodo.datetime.month
        m = 0
        for n in parziale:
            if n.datetime.month == mese:
                m += 1
                if m == 3:
                    return False
        return True

    def condizioneFinale(self, parziale):
        for n in self._graph.neighbors(parziale[-1]):
            if self.condizione(parziale, n):
                return False
        return True

    def calcolaPunteggio(self, parziale):
        p = 100
        for i in range(1, len(parziale)):
            if parziale[i].datetime.month == parziale[i-1].datetime.month:
                p += 200
            else:
                p += 100
        return p

    #--------------------------------------
    def cammino_ottimo(self):
        self._percorso = []
        self._punteggio = 0

        for node in self._graph.nodes():
            parziale = [node]
            rimanenti = self.calcola_rimanenti(parziale)
            self._ricorsione(parziale, rimanenti)

        return self._percorso, self._punteggio

    def _ricorsione(self, parziale, nodi_rimanenti):
        # caseo terminale:
        if len(nodi_rimanenti) == 0:
            punteggio = self.calcola_punteggio(parziale)
            if punteggio > self._punteggio:
                self._punteggio = punteggio
                self._percorso = copy.deepcopy(parziale)
        # caso ricorsivo
        else:
            # per ogni nodo rimanente
            for nodo in nodi_rimanenti:
                # aggiungere il nodo
                parziale.append(nodo)
                # calcolare i nuovi rimanenti di questo nodo
                nuovi_rimanenti = self.calcola_rimanenti(parziale)
                # andare avanti nella ricorsione
                self._ricorsione(parziale, nuovi_rimanenti)
                # backtracking
                parziale.pop()

    def calcola_punteggio(self, parziale):
        punteggio = 0
        # termine fisso
        punteggio += 100 * len(parziale)
        # termine variabile
        for i in range(1, len(parziale)):
            nodo = parziale[i]
            nodo_precedente = parziale[i - 1]
            if nodo.datetime.month == nodo_precedente.datetime.month:
                punteggio += 200
        # return
        return punteggio

    def calcola_rimanenti(self, parziale):
        nuovi_rimanenti = []
        # prendiamo i nodi successivi
        for i in self._graph.successors(parziale[-1]):
            # di questi nodi, dobbiamo verificare il vincolo sul mese
            if (self.is_vincolo_ok(parziale, i) and
                    self.is_vincolo_durata_ok(parziale, i)):
                nuovi_rimanenti.append(i)
        return nuovi_rimanenti

    def is_vincolo_durata_ok(self, parziale, nodo):
        return nodo.duration > parziale[-1].duration

    def is_vincolo_ok(self, parziale, nodo):
        mese = nodo.datetime.month
        counter = 0
        for i in parziale:
            if i.datetime.month == mese:
                counter += 1
        if counter >= 3:
            return False
        else:
            return True

def sort_list(lista):
    lista.sort(key=lambda x: x[2], reverse=True)
