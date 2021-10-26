"""Automaton implementation."""
from typing import Collection, Set

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)

class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )

        # Add here additional initialization code.
        # Do not change the constructor interface.

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":

        initial_states = {self.initial_state}
        initial_states = self._complete_lambdas(initial_states)

        dictstates = {}

        dictstates['States'] = [initial_states]

        # Actualizamos los simbolos del AFD
        symbols = ()
        for symbol in self.symbols:
            if symbol is not None:
                symbols += (symbol,)
                dictstates[symbol] = []

        # Creamos la tabla de estados para el AFD
        for state in dictstates['States']:
            current_states = state
            for symbol in symbols:
                current_states = self._process_symbol(current_states, symbol)
                if not current_states:
                    dictstates[symbol].append(None)
                else:
                    if current_states not in dictstates['States']:
                        dictstates['States'].append(current_states)
                    dictstates[symbol].append(current_states)
                current_states = state

        # Creamos el estado sumidero
        nextstate = len(dictstates['States'])
        sink = State("q"+str(nextstate))
        sink_transitions = ()
        for symbol in symbols:
            trans = Transition(initial_state=sink,
                            symbol=symbol,
                            final_state=sink)
            sink_transitions += (trans,)

        # Cambiamos los conjuntos de estados por nuevos estados
        for state in dictstates['States']:
            combined_state = self._combine_states(state)
            for key in dictstates.keys():
                index = 0
                for value in dictstates[key]:
                    if value == state:
                        dictstates[key][index] = combined_state
                    index += 1

        # Actualizamos la tabla de estados y las transiciones
        # actualizando el estado sumidero en caso necesario
        transitions = ()
        sink_state = False
        for key in list(dictstates.keys())[1:]:
            index = 0
            for value in dictstates[key]:
                initial_state = dictstates['States'][index]
                if value is None:
                    sink_state = True
                    trans = Transition(initial_state=initial_state,
                                       symbol=key,
                                       final_state=sink)
                    sink_transitions += (trans,)
                else:
                    trans = Transition(initial_state=initial_state,
                                       symbol=key,
                                       final_state=value)
                    transitions += (trans,)
                index += 1

        # Actualizamos los estados del AFD
        states = ()
        for state in dictstates['States']:
            states += (state,)

        # Actualizamos estado y transiciones si hay estado sumidero
        if sink_state:
            states += (sink,)
            transitions += sink_transitions

        return FiniteAutomaton(initial_state=dictstates['States'][0],
                               states=states,
                               symbols=symbols,
                               transitions=transitions)


    def _process_symbol(self, current_states: Set[State], symbol: str) -> Set[State]:
        new_states = set()

        for state in current_states:
            for transition in self.transitions:
                if state == transition.initial_state and symbol == transition.symbol:
                    new_states.add(transition.final_state)
        
        new_states = self._complete_lambdas(new_states)

        return new_states


    def _complete_lambdas(self, set_to_complete: Set[State]) -> Set[State]:
        
        initial_len = len(set_to_complete)
        new_states = set()
        
        for state in set_to_complete:
            for transition in self.transitions:
                if state == transition.initial_state and not transition.symbol:
                    new_states.add(transition.final_state)
        
        set_to_complete.update(new_states)
        if len(set_to_complete) != initial_len:
            set_to_complete = self._complete_lambdas(set_to_complete)
        
        return set_to_complete


    def _combine_states(self, states: Set[State]) -> State:
        name = ''
        is_final = False
        for state in states:
            name += state.name
            if state.is_final:
                is_final = True

        new_state = State(name, is_final=is_final)

        return new_state


    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")