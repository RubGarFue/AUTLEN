import ast
from logging import NullHandler
import numbers

from typing import List, Optional, Union

class ASTMagicNumberDetector(ast.NodeVisitor):

    def __init__(self):
        self.magic_numbers = 0

    def _check_magic_number(self, number: complex) -> None:
        if isinstance(number, numbers.Number):
            if number == 1 or number == 0 or number == 1j:
                self.magic_numbers += 1


    def visit_Num(self, node: ast.Num) -> None:
        self._check_magic_number(node.n)


    # Para Python >= 3.8
    def visit_Constant(self, node: ast.Constant) -> None:
        self._check_magic_number(node.value)


class ASTDotVisitor(ast.NodeVisitor):
    
    def __init__(self) -> None:
        self.level = 0
        self.n_node = 0
        self.last_parent: Optional[int] = None
        self.last_field_name = ""

    def prim_values_str(self, prim_list) -> str:
        return ', '.join(['='.join([str(el) for el in prim_list[ind]]) for ind in range(len(prim_list))])

    def generic_visit(self, node: ast.AST) -> None:
        # usar un esquema similar al generic_visit de la clase padre para recorrer los hijos del nodo actual
        # obtener los nodos hijos (nodos AST y listas de nodos AST) del nodo actual
        # obtener los campos hijos (el resto) del nodo actual
        # procesar todos los campos hijos obtenidos del nodo actual (imprimir sus valores)
        # procesar todos los nodos hijos obtenidos del nodo actual (llamada a visit
        
        if self.level == 0:
            print('digraph {')
            
        if self.last_parent is not None:
            print('s{} -> s{}[label="{}"]'.format(self.last_parent, self.n_node, self.last_field_name))
        
        prim_values = [] 
        for field, value in ast.iter_fields(node):
            if not isinstance(value, list) and not isinstance(value, ast.AST):
                prim_values.append((field,value))
        print('s{}[label="{}({})"]'.format(self.n_node, type(node).__name__, self.prim_values_str(prim_values)))

        n_node = self.n_node
        self.level += 1
        self.n_node += 1
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.last_parent = n_node
                        self.last_field_name = field
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.last_parent = n_node
                self.last_field_name = field
                self.visit(value)
                
        self.level -= 1
        if self.level == 0:
            print('}')


class ASTReplaceNum(ast.NodeTransformer):
    
    def __init__(self , number: complex):
        self.number = number
        
    def visit_Num(self, node: ast.Num) -> ast.AST:
        # devolver un nuevo nodo AST con self.number
        return ast.Num(self.number)
    
    # Para Python >= 3.8
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        # devolver un nuevo nodo AST con self.number si la constante es un número
        return ast.Constant(self.number)


class ASTRemoveConstantIf(ast.NodeTransformer):

    def visit_If(self, node: ast.If) -> Union[ast.AST, List[ast.stmt]]:
        # usar node.test, node.test.value, node.body y node.orelse
        if node.test.value:
            return node.body
        return node.orelse