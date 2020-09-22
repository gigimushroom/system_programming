import sys
import os
from os import listdir
from os.path import isfile, join
import JackTokenizer
import lib
import CompilationEngine as CE
import xml.etree.cElementTree as ET


def pretty_token(tk):
  pp = ' %s ' % tk
  return pp

def tokenize_file(input, output=None):
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

      #TODO: output symbol table metadata.

      ET.SubElement(root, 'identifier').text = pretty_token(kw)

    elif tk_type == JackTokenizer.TYPE_INT_CONST:
      kw = tk.intVal()
      ET.SubElement(root, 'integerConstant').text = pretty_token(kw)

    elif tk_type == JackTokenizer.TYPE_STRING_CONT:
      kw = tk.stringVal()
      ET.SubElement(root, 'stringConstant').text = pretty_token(kw)

  tree = ET.ElementTree(root)
  lib.indent(root)

  if output:
    fn = output
  else:
    fn = '%sT.xml' % input

  tree.write(fn)

def run_parser(input, output):
  pp = CE.Parser(input, output=output)
  pp.CompileClass()
  pp.WriteAsFile()

def run():
  file_name = sys.argv[1]
  if os.path.isfile(file_name):
    tokenize_file(file_name)

  else:
    dir_name = os.path.basename(sys.argv[1])
    # Create directory if not exists.
    output_dir = '%s/output' % dir_name
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    for f in listdir(dir_name):
      file_with_path = join(dir_name, f)
      if isfile(file_with_path) and file_with_path.endswith('.jack'):
        print('File full path', file_with_path)
        # Trim .jack extension.
        ff = os.path.splitext(f)[0]
        # Generate xxxT.xml output file name under /output directory.
        output = '%sT.xml' % join(output_dir, ff)
        print('Tokenizer output file', output)

        tokenize_file(input=file_with_path, output=output)

        parser_in = output
        parser_out = '%s.xml' % join(output_dir, ff)
        print('Parser output file', parser_out)

        run_parser(parser_in, parser_out)


run()

