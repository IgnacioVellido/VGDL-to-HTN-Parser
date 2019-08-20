import sys
from antlr4 import *
from VgdlLexer import VgdlLexer
from VgdlParser import VgdlParser

from antlr4.tree.Trees import Trees

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = VgdlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = VgdlParser(stream)
    tree = parser.basicGame()

    print(Trees.toStringTree(tree, None, parser))
 
if __name__ == '__main__':
    main(sys.argv)