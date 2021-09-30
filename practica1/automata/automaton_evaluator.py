"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        new_states = set()

        if symbol is not None and symbol not in self.automaton.symbols:
                raise ValueError(
                    f"Symbol {symbol}"
                    f"is not in the set of symbols",
                )

        for state in self.current_states:
            for transition in self.automaton.transitions:
                if state == transition.initial_state and symbol == transition.symbol:
                    new_states.add(transition.final_state)
        
        self._complete_lambdas(new_states)

        self.current_states = new_states


    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        #raise NotImplementedError("This method must be implemented.")
        initial_len = len(set_to_complete)
        new_states = set()
        
        for state in set_to_complete:
            for transition in self.automaton.transitions:
                if state == transition.initial_state and not transition.symbol:
                    new_states.add(transition.final_state)
        
        set_to_complete.update(new_states)
        if len(set_to_complete) != initial_len:
            self._complete_lambdas(set_to_complete)


    def is_accepting(self) -> bool:
        
        for state in self.current_states:
            if state.is_final:
                return True
        
        return False
