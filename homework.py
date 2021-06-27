import datetime as dt
from typing import Optional

date_format = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date: Optional[str] = None):
        if amount is not int:
            amount = int(amount)
            self.amount = amount
        else:
            self.amount = amount

        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.date.today()

        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record_instance):
        self.records.append(record_instance)
        return record_instance

    def get_today_stats(self):
        today = dt.date.today()
        list_of_amounts = []
        for record in self.records:
            if record.date == today:
                list_of_amounts.append(record.amount)
        return sum(list_of_amounts)

    def get_week_stats(self):
        today = dt.date.today()
        max_date = today - dt.timedelta(weeks=1)
        list_of_amounts = []
        for record in self.records:
            if max_date < record.date <= today:
                list_of_amounts.append(record.amount)
        return sum(list_of_amounts)

    def get_remains(self):
        sum = self.get_today_stats()
        return self.limit - sum


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    currencies = {
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']
    }

    def get_today_cash_remained(self, currency):
        remainder = self.get_remains()
        if remainder == 0:
            return 'Денег нет, держись'

        if currency not in self.currencies.keys():
            result = f'{abs(remainder)} руб'
        else:
            exchange = abs(remainder / self.currencies[currency][0])
            result = f'{exchange:.2f} {self.currencies[currency][1]}'

        if remainder > 0:
            return f'На сегодня осталось {result}'
        else:
            return f'Денег нет, держись: твой долг - {result}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remainder = self.get_remains()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remainder} кКал')
        if remainder <= 0:
            return 'Хватит есть!'
