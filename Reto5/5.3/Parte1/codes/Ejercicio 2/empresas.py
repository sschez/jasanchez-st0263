from mrjob.job import MRJob, MRStep


class DiaMinMax(MRJob):
    def mapper_get_fields(self, _, line):
        company, price, date = line.split(",")
        if not line.startswith("Company"):
            yield company, (date, float(price))

    def reducer_find_min_max_date(self, company, data):
        data_list = list(data)
        lowest_date = min(data_list, key=lambda x: x[1])[0]
        highest_date = max(data_list, key=lambda x: x[1])[0]
        yield company, [lowest_date, highest_date]


class AccionCreciente(MRJob):
    def mapper_get_fields(self, _, line):
        company, price, date = line.split(",")
        if not line.startswith("Company"):
            yield company, (date, float(price))

    def reducer_check_increasing_stocks(self, company, data):
        data_list = list(data)
        dates_sorted = sorted(data_list, key=lambda x: x[0])
        first_price = dates_sorted[0][1]
        increasing_dates = [x[0] for x in dates_sorted[1:] if x[1] >= first_price]
        if len(increasing_dates) > 0:
            yield company, "Acciones crecientes o estables"


class BlackFriday(MRJob):
    def mapper_get_fields(self, _, line):
        company, price, date = line.split(",")
        if not line.startswith("Company"):
            yield None, (float(price), date)

    def reducer_find_lowest_price_day(self, _, data):
        sums = {}
        for price, date in data:
            if date not in sums:
                sums[date] = 0
            sums[date] += price
        min_price_date = min(sums.items(), key=lambda x: x[1])[0]
        yield min_price_date, sums[min_price_date]


if __name__ == "__main__":
    print(">>>>>>>>>> Dia con valor minimo y maximo para cada empresa")
    DiaMinMax.run()

    print(">>>>>>>>>> Empresas con acciones iguales o mayores")
    AccionCreciente.run()

    print(">>>>>>>>>> Dia con precios mas bajos")
    BlackFriday.run()
