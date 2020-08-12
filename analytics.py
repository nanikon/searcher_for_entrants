def func_fin(x, finance):
    """Фильтрует заявление на участие в конкурсе по типу финансирования"""
    if finance == 'all':
        return True
    else:
        return x.split(', ')[-4].split()[1][1:-1] == finance


def func_type(x, type_receipt):
    """Фильтрует заявление на учатие в конкурсе по типу зачисления"""
    if type_receipt == 'all':
        return True
    else:
        return x.split(',')[-4].split()[0] == type_receipt


class Analytics:
    def __init__(self, entrants):
        self.entrants = entrants
        self.statements = []
        self.nul = 0
        for entrant in self.entrants:
            for app in entrant.apps:
                if app[0] != '-':
                    self.statements.append(app[1])
                else:
                    self.nul += 1
            if entrant.priority[0] != '-':
                self.statements.append(entrant.priority[1])
        self.universities = self.get_universities_with_abit()
        self.directions = self.get_directions_with_abit()

    def get_all_abit(self):
        """Возвращает колв-во анализируемых абитурентов"""
        return len(self.entrants)

    def get_not_found_abit(self):
        """Возвращает колв-во не найденных абитурентов. Возможно они поступают в ВУЗы, не поддерживаемые агрегатором"""
        return self.nul

    def get_found_abit(self):
        """Возвращает кол-во найденных абитурентов"""
        return len(self.entrants) - self.nul

    def get_all_statements(self):
        """Возвращает общее кол-во поданных заявлений на участие в конкурсе"""
        return len(self.statements)

    def get_filter_statements(self, finance='all', type_receipt='all'):
        """Возвращает кол-во поданных заявлений на участие в конкурсе, отфильтрованные по типу зачисления (type_receipt)
        и типу финансирования (finance). По умолчанию и при указании 'all' никак не фильтрует.
        Возможные значения finance: Б - бюджет, К - коммерция, БК - квазибюджет.
        Возможные значение type_receipt: 'ОК' - общий конкурс, 'БВИ' - без вступительных испытаний,
        'ОП' - особое право, 'Ц' - целевое. При других значениях возвращается 0."""
        return len(list(filter(lambda x: func_fin(x, finance) and func_type(x, type_receipt), self.statements)))

    def get_consent(self):
        """Возвращает кол-во поданных заявлений о согласии на зачисление"""
        return len(list(filter(lambda x: x.priority[0] != '-', self.entrants)))

    def get_name_universities(self):
        """Возвращает список ВУЗов, в которые были поданы документы абитуриенами и которые поддерживаются агрегатором"""
        return self.universities.keys()

    def get_universities_with_abit(self):
        """Возвращает словарь, в котором ключи - названия ВУЗов, а значения - кол-во поданных заявлений
        на участие в конкурсе в них"""
        universities = {}
        for statement in self.statements:
            university = statement.split(', ')[0]
            if university in universities:
                universities[university] += 1
            else:
                universities[university] = 1
        return universities

    def get_most_popular_university(self):
        """Возвращает список самых популяных ВУЗов, то есть ВУЗов, в которые было подано максимальное кол-во
        заявлений на участие в конкурсе"""
        universities = self.universities
        max_abit = max(universities.values())
        result = []
        for university in universities:
            if max_abit == universities[university]:
                result.append(university)
        return result

    def get_directions_with_abit(self):
        """Возвращает словарь, в котором ключи - названия направлений, а значения - кол-во абитуриентов, подавших
        заявление на участие в конкурсе по ним"""
        directions = {}
        for statement in self.statements:
            a = statement.split(', ')
            i = 0
            while ('03' not in a[i]) and ('05' not in a[i]):
                i += 1
            name = a[i]
            if name in directions:
                directions[name] += 1
            else:
                directions[name] = 1
        return directions

    def get_name_directions(self):
        """Возвращает список направлений, на которые были поданы заявления на участие в конкурсе"""
        return self.directions.keys()

    def get_most_popular_direction(self):
        """Возвращает самые популярные направление, тое есть те, на которые были поданы максимальное кол-во заявлений
        на участие в конкурсе по ним"""
        directions = self.directions
        max_abit = max(directions.values())
        result = []
        for direction in directions:
            if max_abit == directions[direction]:
                result.append(direction)
        return result

    def get_analytics(self):
        """Возвращает список строк с красимвым выводом всей аналитики"""
        result = [
            f'Всего абитуриентов проанализировано: {self.get_all_abit()}',
            'Из них:',
            f'\tНе найдено: {self.get_not_found_abit()}',
            f'\tНайдено: {self.get_found_abit()}',
            ' ',
            f'Всего заявлений подано {self.get_all_statements()}',
            'Из них',
            'По типу финансирования:',
            f'\t{self.get_filter_statements(finance="Б")} на бюджет,',
            f'\t{self.get_filter_statements(finance="К")} на коммерцию,',
            f'\t{self.get_filter_statements(finance="БК")} на квазибюджет.',
            'По типу поступления:',
            f'\t{self.get_filter_statements(type_receipt="ОП")} по особому праву,',
            f'\t{self.get_filter_statements(type_receipt="Ц")} по целевой квоте,',
            f'\t{self.get_filter_statements(type_receipt="БВИ")} без вступительных испытаний,',
            f'\t{self.get_filter_statements(type_receipt="ОК")} по общему конкурсу.',
            '',
            f'Заявлений о согласии на зачисление подано: {self.get_consent()}',
            '',
            'ВУЗы, в которые были поданы заявления:',
            '\n'.join(key + ": " + str(value) for key, value in self.universities.items()),
            f'Самый(-е) "популярный(-е)" ВУЗ(-ы): {" ".join(i for i in self.get_most_popular_university())}',
            '',
            'Направления, на которые были поданы заявления:',
            '\n'.join(key + ": " + str(value) for key, value in self.directions.items()),
            f'Самое(-ые) "популярное(-ые)" направление(-я): {" ".join(i for i in self.get_most_popular_direction())}',
        ]
        return result