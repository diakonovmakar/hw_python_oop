import datetime as dt
from typing import Optional

DATE_FORMAT = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date: Optional[str] = None):
        if amount is not int:
            amount = int(amount)
        self.amount = amount

        if date is not None:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
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
        return sum(r.amount for r in self.records if r.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        mx_date = today - dt.timedelta(weeks=1)
        return sum(r.amount for r in self.records if mx_date < r.date <= today)

    def get_remains(self):
        sum = self.get_today_stats()
        return self.limit - sum


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0
    currencies = {
        'rub': [RUB_RATE, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']
    }

    def get_today_cash_remained(self, currency):
        remainder = self.get_remains()
        if remainder == 0:
            return 'Денег нет, держись'

        if currency not in self.currencies.keys():
            raise ValueError('Ошибка: выбранная вами валюта не поддерживается')
        else:
            if remainder < 0:
                exchange = abs(remainder / self.currencies[currency][0])
            else:
                exchange = remainder / self.currencies[currency][0]

            currency_abbreviation = self.currencies[currency][1]
            result = f'{exchange:.2f} {currency_abbreviation}'

        if remainder > 0:
            return f'На сегодня осталось {result}'
        return f'Денег нет, держись: твой долг - {result}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remainder = self.get_remains()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remainder} кКал')
        return 'Хватит есть!'
