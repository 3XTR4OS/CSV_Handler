import csv


def get_return(client_list):
    top_clients = top_gems(client_list)
    total_top_cliens = find_top_5_cliens(client_list)
    get_result = []

    for client in top_clients:

        for client_2 in total_top_cliens:
            if client['name'] in client_2['name']:
                client_2_total = client_2['total']
        get_result.append({'name': client['name'], 'spend_money': client_2_total, 'gems': client['gems']})

    return get_result


def total_calculate(client_list):
    """Функция, рассчитывающая общее кол-во потраченых средств"""
    for client in client_list:
        client['total'] = sum(map(int, client['total']))


def find_top_5_cliens(client_list, client_count=5):
    """Функция, сортирующая клиентов по их прибыльности; возвращает топ ... лучших"""
    top_clients = sorted(client_list, key=lambda x: x['total'])[::-1]
    return top_clients[0:client_count]


def top_gems(client_list):
    """Функция, возвращающая камни, которые купили минимум 2 клиента"""
    top_clients = find_top_5_cliens(client_list)
    top_client_and_gems = []
    gems_list = []
    popular_gems = set()

    for i in find_top_5_cliens(client_list):
        gems_list.append(set(i['gems']))

    for gems in gems_list:
        for gems_check in gems_list:

            if id(gems) == id(gems_check):
                continue

            else:

                if gems & gems_check:
                    popular_gems.add(*gems & gems_check)

                else:
                    continue

    for client in top_clients:
        if set(client['gems']) & popular_gems:
            top_client_and_gems.append({'name': client['name'], 'gems': (set(client['gems']) & popular_gems)})

    return top_client_and_gems


try:
    with open('deals.csv', 'r', encoding='UTF8') as csvfile:
        status = 'OK'
        reader = csv.reader(csvfile)
        customer_names = set()  # Имена, совершавших сделки
        customers_list = []

        for row in reader:

            """Нужно, чтобы проигнорировать строку с колонками"""
            if row[0] == 'customer':
                continue

            if row[0] in customer_names:  # Являлся ли этот человек к нам раньше
                for customer in customers_list:
                    if row[0] in customer.values():  # Если да, то...
                        customer['gems'].append(row[1])  # Добавить камень в его "покупки"
                        customer['total'].append(row[2])  # Добавить стоимость за камень

            else:
                customers_list.append({'name': row[0], 'gems': [row[1]], 'total': [row[2]]})
                customer_names.add(row[0])
    total_calculate(customers_list)  # Заменяет список затрат на сумму потраченного

except:
    status = 'except'
    print('Возникла ошибка.', status)

# USING

# """ Вывод всех клиентов (всех их сделок и общей суммой в одном словаре)"""
# for i in customers_list[:]:
#     print(i)

# """Вывод клиентов, заплативших больше всего за товар"""
# for i in find_top_5_cliens(customers_list)[:]:
#     print(i)

# """Вывод 3.5 условия из тз"""
# for i in top_gems(customers_list)[:]:
#     print(i)

# """Вывод ответа на POST Django запрос"""
# for i in get_return(customers_list)[:]:
#     print(i)
