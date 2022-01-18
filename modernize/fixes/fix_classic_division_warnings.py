from __future__ import generator_stop

from fissix import fixer_base, pytree
from fissix.pgen2 import token
from fissix.fixer_util import Name, Call, Comma, Node

from fissix import fixer_util
from fissix.pygram import python_symbols as syms

add_lib = "modernize.old_division_utils"
wrap_div = "warn_div"
wrap_div_assign = "warn_div_assign"

class FixClassicDivisionWarnings(fixer_base.BaseFix):

    PATTERN = """
    term<
        factor=any
        (('*'|'@'|'/'|'%'|'//') any)+
    >
    |
    expr_stmt<
        target=any
        '/='
        value=any
    >
    """

    def start_tree(self, tree, name):
        super().start_tree(tree, name)
        self.skip = "division" in tree.future_features

    def term_to_calls(self, node):
        '''
        Returns the equivalent term node where wrap_div is used for division instead of `/`
        '''

        # terms associate to the left with the operation a/b/c => (a/b)/c
        #   a/b*c => call(a,b)*c
        #   a/b*c/d => call(call(a,b)*c, d)
        # https://docs.python.org/3/reference/expressions.html#operator-precedence

        first_child = node.children[0].clone()
        first_child.prefix = ''
        current_children = [first_child]
        for op, r_expr in zip(node.children[1::2], node.children[2::2]):
            if op.value == '/':
                current_children = [Call(Name(wrap_div), [Node(syms.term, current_children), Comma(), r_expr.clone()])]
            else:
                current_children.extend([op.clone(), r_expr.clone()])

        new_node = Node(syms.term, current_children)
        new_node.prefix = node.prefix
        return new_node

    def transform(self, node, results):
        if self.skip:
            return

        if 'factor' in results:
            if any(child.value == '/' for child in node.children if hasattr(child, 'value')):
                # expr1 "/" expr2 ... => wrap_div(expr1, expr2) ...
                fixer_util.touch_import(add_lib, wrap_div, node)
                return self.term_to_calls(node)
            else:
                return

        elif 'target' in results:
            if wrap_div_assign not in str(results['value']):
                # target /= expr => target /= wrap_div_assign(target, expr)
                fixer_util.touch_import(add_lib, wrap_div_assign, node)
                args = [results['target'].clone(), Comma(), results['value'].clone()]
                node.set_child(2,Call(Name(wrap_div_assign), args, results['value'].prefix))
                return node
            else:
                return

        else:
            raise Exception("No transformation was applied to file when it should have.")
