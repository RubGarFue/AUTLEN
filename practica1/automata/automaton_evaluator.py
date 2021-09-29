"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        new_states = Set[State]

        for state in super().current_states:
            for transition in super().automaton.transitions:
                if state == transition.initial_state and symbol == transition.symbol:
                    new_states.add(transition.final_state)
        
        #self._complete_lambdas(new_states)

        super().current_states = new_states

    
    def _complete_lambda(self, state: State, set_to_complete: Set[State]) -> None:

        lambda_set = Set[State]
        
        for transition in super().automaton.transitions:
            if state == transition.initial_state and "" == transition.symbol:
                self._complete_lambda(transition.final_state, set_to_complete)
                lambda_set.add(transition.final_state)


    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        raise NotImplementedError("This method must be implemented.")
        new_states = Set[State]
        
        for state in set_to_complete:
            lambda_states = Set[State]
            self._complete_lambda(state, lambda_states)
            new_states.update(lambda_states)
            for transition in super().automaton.transitions:
                if state == transition.initial_state and "" == transition.symbol:
                    self._complete_lambdas(set_to_complete.add(state))
        
        super().current_states = new_states


    def is_accepting(self) -> bool:
        
        for state in super().current_states:
            if state.is_final:
                return True
        
        return False
