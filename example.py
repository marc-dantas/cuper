from cuper.core import Parser, Type, Argument, Option

p = Parser("p", "10")
r = p.match(Option(["print", "p"]), Argument(Type.NUMBER))
print(r.success)  # True
