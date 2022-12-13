from cuper.core import Parser, Type, Argument, Option, count

p = Parser(["p", "the magic of python"])
r = p.match([Option(["print", "p"]), Argument(Type.TEXT)])

if r.success:
    print(r.values[0])
else:
    print("no match. sorry :(")
