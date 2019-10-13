import csv
import glob
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_files(path):
    x_y, x = dict(), list()
    for file in glob.glob('%s/*.txt' % path):
        with open(file) as f:
            f_name = os.path.basename(file)
            f_lines = f.readlines()
            raw_data = [c.split() for c in f_lines]
            x_y[f_name] = [{'x': int(float(a)), 'y': b.replace('.', ',')} for a, b in raw_data]
            x.extend(sorted(set([i['x'] for i in x_y[f_name]])))
            logger.log(20, ' → Parsed file "%s"' % f.name)
    return x, x_y


x, x_y = parse_files('resources')
result_dict = {i: [None] * len(x_y) for i in x}
files = list()
for n, k in enumerate(x_y):
    files.append(k)
    for coords in x_y[k]:
        result_dict[coords['x']][n] = coords['y']

redult_set = [(k,) + tuple(v) for k, v in result_dict.items()]

with open('[result].csv', 'w', encoding='utf-8') as fp:
    writer = csv.writer(fp, dialect='excel', lineterminator='\n')
    writer.writerow(['x'] + ['y_(%s)' % f for f in files])
    writer.writerows(sorted(redult_set, key=lambda s: s[0]))
    logger.log(20, ' → Finished writing to file "%s"' % fp.name)
