import xml.etree.cElementTree as ET
import sys
import os
import JackTokenizer

# https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

def pretty_token(tk):
  pp = ' %s ' % tk
  return pp

def tokenize_file(input, writer=None):
  root = ET.Element("tokens")

  tk = JackTokenizer.Tokenizer(input)
  while(tk.hasMoreTokens()):
    tk.advance()
    
    tk_type = tk.tokenType()
    element = None
    if tk_type == JackTokenizer.TYPE_KEYWORD:
      kw = tk.keyword()
      ET.SubElement(root, 'keyword').text = pretty_token(kw)

    elif tk_type == JackTokenizer.TYPE_SYMBOL:
      kw = tk.symbol()
      ET.SubElement(root, 'symbol').text = pretty_token(kw)

    elif tk_type == JackTokenizer.TYPE_IDENTIFIER:
      kw = tk.identifier()
      ET.SubElement(root, 'identifier').text = pretty_token(kw)

    elif tk_type == JackTokenizer.TYPE_INT_CONST:
      kw = tk.intVal()
      ET.SubElement(root, 'integerConstant').text = pretty_token(kw)

    elif tk_type == JackTokenizer.TYPE_STRING_CONT:
      kw = tk.stringVal()
      ET.SubElement(root, 'stringConstant').text = pretty_token(kw)


  tree = ET.ElementTree(root)
  indent(root)

  fn = '%sT.xml' % input
  tree.write(fn)


file_name = sys.argv[1]
if os.path.isfile(file_name):
  tokenize_file(file_name)

# else:
#   dir_name = sys.argv[1]
#   # Get last part of dirtectory name. Example: a/b => b
#   output = '%s.asm' % os.path.basename(dir_name)
#   print(dir_name, output) 
#   # cw = code_writer.CodeWriter(join(dir_name, output))
#   # cw.writeInit()

#   # for f in listdir(dir_name):
#   #   if isfile(join(dir_name, f)) and f.endswith('.vm'):
#   #     parse_a_file(join(dir_name, f), cw)

