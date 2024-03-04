from json import dump
from re import findall
from string import ascii_letters, digits
from subprocess import run 

PATTERN = "width: ([0-9]+);"

def command_args(size, character):
    return ['./get_metrics.sh', str(size), character]

CHARACTERS = ascii_letters + digits + "-+:/" # TODO: How to pass ImageMagick a space?

widths = {}

for c in CHARACTERS:
    result = run(command_args(160, c), capture_output=True)
    metrics = str(result.stdout or result.stderr)
    matches = findall(PATTERN, metrics)
    width_str = matches[0]
    widths[c] = int(width_str)

output_file = "widths.json"
with open(output_file, 'w') as f:
    dump(widths, f, indent=4, sort_keys=True)
