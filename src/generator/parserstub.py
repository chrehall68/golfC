from generator.types import *
from generator.lexer import Token
from typing import List, Tuple, Union, Any, Literal, Dict, Callable, Optional


class Parser:
    def __init__(
        self,
        grammar: Grammar,
        callbacks: Optional[Dict[str, Callable[[List[Any]], Any]]] = None,
    ):
        self.callbacks = callbacks
        self.rule_map = {rule.name: rule for rule in grammar.rules}
        self.cache = {}

    def __take_leaf(
        self, l: Leaf, tokens: List[Token], pos: int
    ) -> Union[Tuple[Any, int], Literal[False]]:
        if pos >= len(tokens):
            return False
        if l.type == "LITERAL":
            # in the case of literals, l.value
            # contains the exact literal to match
            if tokens[pos].value != l.value:
                return False
            return tokens[pos], pos + 1
        elif l.type == "TERMINAL":
            # in the case of terminals, l.value
            # contains the type of the nonterminal
            if tokens[pos].type != l.value:
                return False
            return tokens[pos], pos + 1
        else:
            # in the case of nonterminals, l.value
            # contains the name of the nonterminal
            result = self.__check_rule(l.value, tokens, pos)
            if not result:
                return False
            return result

    def __take_leaves(
        self, l: List[Leaf], tokens: List[Token], pos: int
    ) -> Union[Tuple[List[Any], int], Literal[False]]:
        if pos >= len(tokens):
            return False
        result = []
        for leaf in l:
            r = self.__take_leaf(leaf, tokens, pos)
            if not r:
                return False
            res, pos = r
            result.append(res)
        return result, pos

    def __check_production(self, prod: Production, tokens: List[Token], pos: int):
        result = []
        for part in prod.items:
            if part.optional:
                # try taking, but it's ok if it fails
                r = self.__take_leaves(part.items, tokens, pos)
                if r:
                    # it actually succeeded, go with this
                    res, pos = r
                    result.append(res)
            elif part.star:
                # try taking any amount of this
                r = self.__take_leaves(part.items, tokens, pos)
                while r:
                    res, pos = r
                    result.append(res)
                    r = self.__take_leaves(part.items, tokens, pos)
            else:
                # must take this item
                r = self.__take_leaves(part.items, tokens, pos)
                if not r:
                    return False
                res, pos = r
                result.append(res)
        return result, pos

    def __check_rule(self, rule: str, tokens: List[Token], pos: int):
        # takes the rule that succeeds that takes the most tokens
        if (rule, pos) in self.cache:
            return self.cache[(rule, pos)]

        actual_rule = self.rule_map[rule]
        best = None
        for prod in actual_rule.productions:
            r = self.__check_production(prod, tokens, pos)
            if r and (best is None or best[1] < r[1]):
                best = r

        result = best if best is not None else False
        self.cache[(rule, pos)] = result
        return result

    def parse(
        self, start_symbol: str, tokens: List[Token]
    ) -> Union[list, Literal[False]]:
        self.cache = {}
        result = self.__check_rule(start_symbol, tokens, 0)
        if result:
            return result[0]
        return False
