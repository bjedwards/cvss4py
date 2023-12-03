import argparse
import json
import csv

from cvss4py import score_vector, vector_to_equivalence_class

# From https://stackoverflow.com/questions/29484443/python-argparse-insert-blank-line-between-help-entries/29485128#29485128
class BlankLinesHelpFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        lines = super()._split_lines(text, width)
        if text.endswith('\n'):
            lines += ['']
        return lines
    
less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=4, width=80)

parser = argparse.ArgumentParser(
    prog="CVSS v4 Calculator", 
    description="Python program to calculate CVSS v4 scores",
    formatter_class=less_indent_formatter
)

parser.add_argument(
    dest="vector",
    type=str,
    nargs='?',
    default=None,
    help="Vector string to evaluate, can be missing if --input_vectors is specififed",
)

parser.add_argument(
    '-iv', '--input_vectors',
    default=None,
    type=str,
    dest="input_vectors",
    help="Newline separated file that has vectors to score",
)

parser.add_argument(
    '-ot', '--output_type',
    default='raw',
    dest='output_type',
    help='''How to output the final scores:
\traw: Each line is the score corresponding to the input vector
\tjsonl: Each line is a new json object with score information
\tcsv: a header is displayed then a csv for each vector scored''',
    choices=['raw', 'jsonl', 'csv']
)

parser.add_argument(
    '-oeq', '--output_equivalence_class',
    dest="output_equivalence_class", 
    action="store_false", 
    help="Output the corresponding equivalence class with the vector in csv and jsonl mode"
)

cmd_args = vars(parser.parse_args())

input_vectors = cmd_args['input_vectors']
if cmd_args['vector'] is None:
    if cmd_args['input_vectors'] is None:
        raise ValueError("Must specify a vector on the command line or a file for --input_vectors (-iv) to score")
    else:
        with open(cmd_args['input_vectors'], 'r') as f:
            vectors = f.readlines()
else:
    vectors = [cmd_args['vector']]

scored_vects = []
for vector in vectors:
    vector = vector.strip()
    if vector == '':
        continue
    try:
        score = score_vector(vector)
        eq_c = vector_to_equivalence_class(vector)
    except:
        score = None
        eq_c = None
    scored_v =  {
        'vector':vector,
        'equivalence_class':eq_c,
        'score':score
    }
    if not cmd_args['output_equivalence_class']:
        del scored_v['equivalence_class']
    scored_vects.append(scored_v)

if cmd_args['output_type'] == 'jsonl':
    for scored_v in scored_vects:
        print(json.dumps(scored_v))

elif cmd_args['output_type'] == 'csv':
    csv_writer = csv.DictWriter(sys.stdout, fieldnames=list(scored_vects[0].keys()))
    csv_writer.writeheader()
    for scored_v in scored_vects:
        csv_writer.writerow(scored_v)
elif cmd_args['output_type'] == 'raw':
    for scored_v in scored_vects:
        print(scored_v['score'])


