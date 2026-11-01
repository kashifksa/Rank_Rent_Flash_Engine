import sys

filename = sys.argv[1]
content = open(filename, encoding='utf-8').read()
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if '\u2014' in line:
        print(f'Line {i}: {repr(line)}')
