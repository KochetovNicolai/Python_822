import matplotlib.pyplot as plt
from random import shuffle


class Plot:
    """Этот класс ответственный за отрисовку графиков"""

    def __init__(self):
        pass

    def table_to_plot(self, table, company='Undefined', name_='Undefined', ):
        """Из pandas.DataFrame делает график и сохраняет его в data"""

        table['mean'] = (table['high'] + table['low']) / 2.0

        _, ax = plt.subplots()

        fig = plt.figure(
            figsize=(18, 9),
            facecolor='ivory',
            dpi=250
        )

        plt.title('{} stock prices for the recent 36 months'.format(company[0]), fontsize=24)

        plt.xlabel(
            'Date',  # Текст
            fontdict=dict(family='monospace', color='peru', weight='normal', size=25)  # Настройки шрифта
        )
        plt.ylabel(
            'Price $',
            fontdict=dict(family='monospace', color='peru', weight='light', size=25)
        )

        plt.grid(True)

        plt.plot(
            table[:36]['timestamp'].iloc[::-1],
            table[:36]['mean'].iloc[::-1],
            color='teal',
            alpha=0.9,
            linewidth=8
        )  # Рассмотрим данные за последние 36 месяцев

        name = '{}.png'.format(name_)

        plt.savefig('static/{}'.format(name))

        return name

    def twin_table_plot(self, tables, companies, name_):

        colours = ['crimson', 'navy', 'seagreen', 'aqua']

        for i in range(len(tables)):  # Создадим новый столбец в каждой таблице
            tables[i]['mean'] = (tables[i]['high'] + tables[i]['low']) / 2.0

        fig = plt.figure(
            figsize=(18, 9),
            facecolor='ivory',
            dpi=250
        )

        plt.title('Compare {} stock prices for the recent 36 months'.format(', '.join(companies)), fontsize=24)

        plt.xlabel(
            'Date',  # Текст
            fontdict=dict(family='monospace', color='peru', weight='normal', size=25)  # Настройки шрифта
        )
        plt.ylabel(
            'Price $',
            fontdict=dict(family='monospace', color='peru', weight='light', size=25)
        )

        plt.grid(True)

        shuffle(colours)  # Будем перемешивать цвета, чтобы графики были неоднообразными

        for i in range(len(tables)):
            plt.plot(
                tables[i][:36]['timestamp'].iloc[::-1],
                tables[i][:36]['mean'].iloc[::-1],
                color=colours[i],
                alpha=0.9,
                linewidth=5
            )  # Рассмотрим данные за последние 36 месяцев

        plt.legend(
            companies,
            loc='lower left',
            borderaxespad=5
        )

        name = '{}.png'.format(name_)

        plt.savefig('static/{}'.format(name))

        return name
