class Solucion:

    def __init__(self, id, vectorRepresentacion, aptitud, esValido):
        self._id = id
        self._vectorRepresentacion = vectorRepresentacion
        self._aptitud = False
        self._esValido = -1

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def vectorRepresentacion(self):
        return self._vectorRepresentacion

    @vectorRepresentacion.setter
    def vectorRepresentacion(self, vectorRepresentacion):
        self._vectorRepresentacion = vectorRepresentacion

    @property
    def aptitud(self):
        return self._aptitud

    @aptitud.setter
    def aptitud(self, aptitud):
        self._aptitud = aptitud

    @property
    def esValido(self):
        return self._esValido

    @esValido.setter
    def esValido(self, esValido):
        self._esValido = esValido    