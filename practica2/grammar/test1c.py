# Ejemplo
from ast_utils import ASTReplaceNum
import ast, inspect, types

def transform_code(f, transformer):
    f_ast = ast.parse(inspect.getsource(f))

    new_tree = ast.fix_missing_locations(transformer.visit(f_ast))
    
    old_code = f.__code__
    code = compile(new_tree, old_code.co_filename, 'exec')
    new_f = types.FunctionType(code.co_consts[0], f.__globals__)
    
    return new_f

def my_fun(p):
    if p == 1:
        print(p + 1j)
    elif p == 5:
        print(0)
    else:
        print(p - 27.3 * 3j)

num_replacer = ASTReplaceNum(3)
new_fun = transform_code(my_fun, num_replacer)

new_fun(1)
# Debería imprimir -8

new_fun(3)
# Debería imprimir 6