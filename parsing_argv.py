from cuper.core import Parser, Type, stringify
from sys import argv
from cuper.util import lit_with_arg

p = Parser(argv[1:])
expr = lit_with_arg('print', Type.TEXT)
result = p.match(expr)
if result:
    print(result[1])
else:
    print("error: expected argv format: %s" % stringify(expr))
