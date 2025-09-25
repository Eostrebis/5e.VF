import json
import os
from pathlib import Path

working_dir = "/home/runner/work/5e.VF/5e.VF/docs/"
working_dir = "C:\\Users\\User\\Documents\\Gautier\\5e.VF\\5e\\docs"
directory = Path(working_dir)


def get_status(file) -> str:
    if file.endswith('.md'):
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('status'):
                    return line[7:].strip()


def update(d1: dict, d2: dict):
    for k in d1:
        d1[k] += d2.setdefault(k, 0)
    for k in d2:
        if k not in d1:
            d1[k] = d2.setdefault(k, 0)
    return d1


if __name__ == '__main__':
    start_index = working_dir.index('docs') + 5
    status_d = {}
    for subdir, dirs, files in os.walk(working_dir):
        p = subdir[start_index:]
        status_d[p] = {}
        status_d[p]['finished'] = 0
        status_d[p]['empty'] = 0
        status_d[p]['completed'] = 0
        status_d[p]['wip'] = 0
        for file in files:
            status = get_status(os.path.join(subdir, file))
            if status:
                status_d[p][status] += 1
    key_d: dict[str, list] = {}
    for key in status_d:
        key_d[key] = []
        if '\\' in key:
            key_d[key[:key.rindex('\\')]].append(key)
    keys = list(key_d.keys())
    for key in keys:
        if not key_d[key]:
            del key_d[key]

    global_d = {}
    for key in list(key_d.keys())[::-1]:
        status_k_d = status_d[key]
        for key2 in key_d[key]:
            update(status_k_d, status_d[key2])
        if sum(status_k_d.values()):
            print(f"Status de {key}")
            print(f"\tTerminé : {status_k_d['finished']}")
            print(f"\tComplété : {status_k_d['completed']}")
            print(f"\tEn Cours : {status_k_d['wip']}")
            print(f"\tVide : {status_k_d['empty']}")
            print(f"Progression globale : {100*round((status_k_d['finished']+status_k_d['completed']*0.75+status_k_d['wip']*0.5)/(sum(status_k_d.values())), ndigits=2)}%")
            print('---')
        update(global_d, status_k_d)
    print(f"Progression globale")
    print(f"\tTerminé : {global_d['finished']}")
    print(f"\tComplété : {global_d['completed']}")
    print(f"\tEn Cours : {global_d['wip']}")
    print(f"\tVide : {global_d['empty']}")
    print(
        f"Progression totale : {100 * round((global_d['finished'] + global_d['completed'] * 0.75 + global_d['wip'] * 0.5) / (sum(global_d.values())), ndigits=2)}%")
    print('---')
