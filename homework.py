import datetime as dt
from typing import Optional


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        if date is not None:
            date = dt.datetime.strptime(date, self.date_format).date()
            self.date = date
        else:
            date = dt.date.today()
            self.date = date

        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record_instance):
        if record_instance.amount is not int:
            amount = int(record_instance.amount)
            record_instance.amount = amount

        self.records.append(record_instance)
        return record_instance

    def get_today_stats(self):
        today = dt.date.today()
        sum = 0
        for record in self.records:
            if record.date == today:
                sum += record.amount
        return sum

    def get_week_stats(self):
        today = dt.date.today()
        max_date = today - dt.timedelta(weeks=1)
        sum = 0
        for record in self.records:
            if max_date <= record.date <= today:
                sum += record.amount
        return sum


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        sum = self.get_today_stats()
        remainder = self.limit - sum

        if currency == 'rub':
            result = f'{remainder} руб'
        elif currency == 'usd':
            exchange = round(remainder / self.USD_RATE, 2)
            result = f'{exchange} USD'
        elif currency == 'eur':
            exchange = round(remainder / self.EURO_RATE, 2)
            result = f'{exchange} Euro'

        if remainder > 0:
            return f'На сегодня осталось {result}'
        elif remainder < 0:
            result = result.replace('-', '')
            return f'Денег нет, держись: твой долг - {result}'
        else:
            return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        sum = self.get_today_stats()
        remainder = self.limit - sum
        if remainder > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remainder} кКал')
        else:
            return 'Хватит есть!'
