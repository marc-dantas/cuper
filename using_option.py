from cuper.core import Parser, Type, stringify, Option
from cuper.util import arguments

expr = [Option('sum', 'plus'), *arguments(Type.NUMBER, Type.NUMBER)]
val = input("input> ").split()
p = Parser(val)
result = p.match(expr)
if result:
    print(result[1] + result[2])
else:
    print("error: expected format: %s" % stringify(expr))
