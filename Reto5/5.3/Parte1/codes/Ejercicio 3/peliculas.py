from mrjob.job import MRJob, MRStep

class PeliculaVistaRating(MRJob):
    def mapper(self, key, line):
        usuario, movie, rating, genre, date = line.split(",")
        if line.startswith("Usuario"):  # skip the header line
            pass
        else:
            yield usuario, [movie, rating]

    def reducer(self, usuario, data):
        data = list(data)
        yield usuario, [len(data), sum([int(x[1]) for x in data])/len(data)]


class DiaVistas(MRJob):
    def mapper(self, key, line):
        usuario, movie, rating, genre, date = line.split(",")
        if line.startswith("Usuario"):  # skip the header line
            pass
        else:
            yield None, [date, movie]

    def reducer(self, _, data):
        data = list(data)
        values = {}
        for key, val in data:
            if key not in values:
                values[key] = 0
            values[key] += 1
        diamax, pelmax = max(values.items(), key=lambda x: x[1])
        diamin, pelmin = min(values.items(), key=lambda x: x[1])
        yield diamax, pelmax
        yield diamin, pelmin


class UsuarioVistaRating(MRJob):
    def mapper(self, key, line):
        usuario, movie, rating, genre, date = line.split(",")
        if line.startswith("Usuario"):  # skip the header line
            pass
        else:
            yield movie, [usuario, rating]

    def reducer(self, movie, data):
        data = list(data)
        yield movie, [len(data), sum([int(x[1]) for x in data])/len(data)]


class DiaRating(MRJob):
    def mapper(self, key, line):
        usuario, movie, rating, genre, date = line.split(",")
        if line.startswith("Usuario"):  # skip the header line
            pass
        else:
            yield None, [date, rating]

    def reducer(self, _, data):
        data = list(data)
        values = {}
        for key, val in data:
            if key not in values:
                values[key] = []
            values[key].append(float(val))
        diamax, pelmax = max(values.items(), key=lambda x: sum(x[1])/len(x[1]))
        diamin, pelmin = min(values.items(), key=lambda x: sum(x[1])/len(x[1]))
        yield diamax, sum(pelmax)/len(pelmax)
        yield diamin, sum(pelmin)/len(pelmin)


class GeneroRating(MRJob):
    def mapper(self, key, line):
        usuario, movie, rating, genre, date = line.split(",")
        if line.startswith("Usuario"):  # skip the header line
            pass
        else:
            yield genre, [movie, rating]

    def reducer(self, genre, data):
        data = list(data)
        values = {}
        for key, val in data:
            if key not in values:
                values[key] = []
            values[key].append(float(val))
        diamax, _ = max(values.items(), key=lambda x: sum(x[1])/len(x[1]))
        diamin, _ = min(values.items(), key=lambda x: sum(x[1])/len(x[1]))
        yield genre, diamax
        yield genre, diamin


if __name__ == "__main__":
    print(">>>>>>>>>> Peliculas vistas y rating promedio por usuario")
    PeliculaVistaRating.run()

    print(">>>>>>>>>> Dia con mas y menos peliculas vistas")
    DiaVistas.run()

    print(">>>>>>>>>> Vistas por pelicula y rating promedio de ella")
    UsuarioVistaRating.run()

    print(">>>>>>>>>> Dia con mayor y menor rating")
    DiaRating.run()

    print(">>>>>>>>>> Peliicula con mayor y menor rating por genero")
    GeneroRating.run()
