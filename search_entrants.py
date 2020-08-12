import argparse
from entrant_applications import EntrantApplications
from analytics import Analytics


def collection_and_analysis(f_name, is_analytic):
    with open(f_name, 'rt', encoding='utf-8') as f:
        data = list(map(lambda s: s.replace('\n', ''), f.readlines()))
    entrants = []
    for fio in data:
        entrant = EntrantApplications(fio)
        entrants.append(entrant)
    result = []
    for entrant in entrants:
        result.append(entrant.fname)
        result.append('Согласие о зачислении подано на направление: ' + entrant.priority[1])
        for direction in entrant.apps:
            result.append(direction[1])
        result.append('')
    if is_analytic:
        analysis = Analytics(entrants)
        result.extend(analysis.get_analytics())
    with open('result.txt', 'wt', encoding='utf-8') as f:
        f.write('\n'.join(s for s in result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search for applicants on the site admlist.ru and analysis of information about them')
    parser.add_argument('file', type=str, help='Input file for FIO applicants')
    parser.add_argument('--analytics', action='store_true', help='Is do analysis')
    args = parser.parse_args()
    collection_and_analysis(args.file, args.analytics)
