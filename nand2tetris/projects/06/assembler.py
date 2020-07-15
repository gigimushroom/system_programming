import sys

def split_c_instr(code):
  dest = comp = jump = None

  split_by_jump = code.split(";")
  d_and_c = split_by_jump[0]
  if len(split_by_jump) > 1:
    jump = split_by_jump[1]

  result = d_and_c.split("=")
  
  if len(result) > 1:
    dest = result[0]
    comp = result[1]
  else:
    # Only Comp is set. Usually for jump instruction.
    comp = result[0]

  return dest, comp, jump


def dest_to_binary(code):
  # return 3 bits
  d = {
    None: '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
  }
  return d[code]

def comp_to_binary(code):
  if not code:
    return None

  d = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',

    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
  }
  return d[code]
    

def jump_to_binary(code):
  d = {
    None: '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
  }
  return d[code]


symbol_table = {
  'SP': 0,
  'LCL': 1,
  'ARG': 2,
  'THIS': 3,
  'THAT': 4,
  'R0': 0,
  'R1': 1,
  'R2': 2,
  'R3': 3,
  'R4': 4,
  'R5': 5,
  'R6': 6,
  'R7': 7,
  'R8': 8,
  'R9': 9,
  'R10': 10,
  'R11': 11,
  'R12': 12,
  'R13': 13,
  'R14': 14,
  'R15': 15,
  'SCREEN': 16384,
  'KBD': 24576,
}
avail_mem_pos = 16

contents = []
file_name = sys.argv[1]
with open(file_name) as f:
  for line in f:
    # partition returns a tuple: 
    # everything before the partition string, the partition string,
    # and everything after the partition string. 
    # So, by indexing with [0] we take just the part before 
    # the partition string.
    line = line.partition('//')[0]
    line = line.strip()
    if line:
      contents.append(line)

counter = 0
codes = []
for c in contents:
  if c.startswith('('):
    symbol_table[c[1:-1]] = counter
  else:
    codes.append(c)
    counter += 1

binary = []
# Parsing
for code in codes:
  if code.startswith('@'):
    code = code[1:]
    if not code.isdigit():
      if not code in symbol_table:
        symbol_table[code] = avail_mem_pos
        avail_mem_pos += 1
      
      code = symbol_table[code]

    hack = "{0:b}".format(int(code))
    hack = hack.zfill(16)
    binary.append(hack)
  else:
    dest, comp, jump = split_c_instr(code)
    dest_hex = dest_to_binary(dest)
    comp_hex = comp_to_binary(comp)
    j_hex = jump_to_binary(jump)
    code = '111' + comp_hex + dest_hex + j_hex
    binary.append(code)

# for c in binary:
#   print(c)
#print(symbol_table)


with open(sys.argv[2], 'w') as f:
  for item in binary:
    f.write("%s\n" % item)









