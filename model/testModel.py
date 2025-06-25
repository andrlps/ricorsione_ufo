from model.modello import Model

model = Model()

model.buildGraph(2000, "circle")
l1, c1 = model.getPath()
l2, c2 = model.cammino_ottimo()
