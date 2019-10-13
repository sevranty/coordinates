import csv
import glob
import logging
import os
import plotly.graph_objects as go

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_files(path):
    x_y, x = dict(), list()
    for file in glob.glob('%s/*.txt' % path):
        with open(file) as f:
            f_name = os.path.basename(file)
            f_lines = f.readlines()
            raw_data = [c.split() for c in f_lines]
            x_y[f_name] = [{'x': int(float(a)), 'y': b.replace('.', '.')} for a, b in raw_data]
            # x_y[f_name] = [{'x': int(float(a)), 'y': b.replace('.', ',')} for a, b in raw_data]
            x.extend(sorted(set([i['x'] for i in x_y[f_name]])))
            logger.log(20, ' → Parsed file "%s"' % f.name)
    return x, x_y


x, x_y = parse_files('resources')

result_dict = {i: [None] * len(x_y) for i in x}

files = list()
file_list = []
numbers_in_file = []

print('========================================================================')
print('x        = ', x)
print('x_y      = ', x_y)
print('x_y.keys = ', x_y.keys())
print('========================================================================')

for file in x_y:
    file_list.append(file)
    numbers_in_file = x_y[file]
    print('FILE=(', file, ') // NUMBERS_IN_FILE(', file, ')=', numbers_in_file)

print('========================================================================')
print('file_list = ', file_list)
print('========================================================================')

for n, k in enumerate(x_y):
    files.append(k)
    for coords in x_y[k]:
        result_dict[coords['x']][n] = coords['y']

result_set = [(k,) + tuple(v) for k, v in result_dict.items()]

with open('[result].csv', 'w', encoding='utf-8') as fp:
    writer = csv.writer(fp, dialect='excel', lineterminator='\n')
    writer.writerow(['x'] + ['y_(%s)' % f for f in files])
    writer.writerows(sorted(result_set, key=lambda s: s[0]))
    logger.log(20, ' → Finished writing to file "%s"' % fp.name)


def matrixtranspose(matrix):
    if not matrix: return []
    coords_raw = [*zip(*matrix)]
    coords = [list(map(lambda s: s.replace(',', '.') if type(s) is str else s, row)) for row in coords_raw]
    return coords


trs = matrixtranspose(sorted(result_set, key=lambda s: s[0]))  # trs == transpose_result_set

# Create traces
fig = go.Figure()

for row in trs[1:]:
    fig.add_trace(go.Scatter(
        y=row,
        x=trs[0],
        mode='lines',
        name='lines'
    ))

# Edit the layout
fig.update_layout(title='Интенсивность спектров испускания',
                  xaxis_title='Интенсивность, отн ед',
                  yaxis_title='Длина волны, нм')

fig.show()
