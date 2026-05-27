import subprocess
from pathlib import Path
p = Path(__file__).parent
input_file = p / 'test_input_data.txt'
modern_out = p / 'modern_out.txt'
legacy_out = p / 'legacy_out.txt'

with open(input_file, 'r', encoding='utf-8') as fin:
    inp = fin.read()

# run modern
proc = subprocess.run(['python', 'modern_library.py'], input=inp, text=True, capture_output=True)
modern_out.write_text(proc.stdout + '\n' + proc.stderr, encoding='utf-8')
print('--- modern output ---')
print(modern_out.read_text(encoding='utf-8'))

# run legacy
proc2 = subprocess.run(['python', 'legacy_lib.py'], input=inp, text=True, capture_output=True)
legacy_out.write_text(proc2.stdout + '\n' + proc2.stderr, encoding='utf-8')
print('--- legacy output ---')
print(legacy_out.read_text(encoding='utf-8'))
