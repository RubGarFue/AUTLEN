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
                return True
        return False


    def visit_Num(self, node: ast.Num) -> None:
        if self._check_magic_number(node.n):
            self.magic_numbers += 1


    # Para Python >= 3.8
    def visit_Constant(self, node: ast.Constant) -> None:
        if self._check_magic_number(node.value):
            self.magic_numbers += 1


class ASTDotVisitor(ast.NodeVisitor):
    
    def __init__(self) -> None:
        self.level = 0
        self.n_node = 0
        self.last_parent: Optional[int] = None
        self.last_field_name = ""


    def generic_visit(self, node: ast.AST) -> None:
        # usar un esquema similar al generic_visit de la clase padre para recorrer los hijos del nodo actual
        # obtener los nodos hijos (nodos AST y listas de nodos AST) del nodo actual
        # obtener los campos hijos (el resto) del nodo actual
        # procesar todos los campos hijos obtenidos del nodo actual (imprimir sus valores)
        # procesar todos los nodos hijos obtenidos del nodo actual (llamada a visit
        if self.level == 0:
            print('digraph {\n')

        for field, value in ast.iter_fields(node):
            self.level += 1
            if isinstance(value, list):
                for item in value:
                    print(value)
                    if isinstance(item, ast.AST):
                        self.last_parent = self.n_node
                        self.n_node += 1
                        print('s' + str(self.last_parent) + ' -> ' + 's' + str(self.n_node) + '[label="' + field + '"]')
                        self.visit(item)
            elif isinstance(value, ast.AST):
                #self.last_parent = self.n_node
                self.n_node += 1
                print('s' + str(self.last_parent) + ' -> ' + 's' + str(self.n_node) + '[label="' + field + '"]')
                self.visit(value)

        #print('}')


class ASTReplaceNum(ast.NodeTransformer):

    def __init__(self , number: complex):
        self.number = number
        
    def visit_Num(self, node: ast.Num) -> ast.AST:
        # devolver un nuevo nodo AST con self.number
        node.value = self.numbe
        return node
    
    # Para Python >= 3.8
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        # devolver un nuevo nodo AST con self.number si la constante es un número
        node.value = self.number
        return node


class ASTRemoveConstantIf(ast.NodeTransformer):

    def visit_If(self, node: ast.If) -> Union[ast.AST, List[ast.stmt]]:
        # usar node.test, node.test.value, node.body y node.orelse
        if node.test.value == True:
            node.test = None
            node.orelse = None
            return node.body