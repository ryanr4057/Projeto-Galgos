class corrida_h:
    def __init__(self, data, pista, dist, trap, split, bends, peso, cat, tempo, pos):
        self.data = data
        self.pista = pista
        self.dist = dist
        self.trap = trap
        self.split = split
        self.bends = bends
        self.peso = peso
        self.cat = cat
        self.tempo = tempo
        self.pos = pos
    pass

class dog:
    def __init__(self, nome, corridas: corrida_h):
        self.nome = nome
        self.corridas = corridas
    pass

class race:
    def __init__(self, numero, dogs: dog):
        self.numero = numero
        self.dogs = dogs
    pass

class pista:
    def __init__(self, id, races: race):
        self.id = id
        self.races = races
    pass




