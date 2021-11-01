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
        self._remove_unaccesible_states()
        self._group_equivalent_states()

    def _remove_unaccesible_states(self):
        self.states = set(self.states)
        # find accessible states
        accessible = set()
        prev_accessible = {self.initial_state}
        new_accessible = set()

        for i in range(1, len(self.states)):
            for state in prev_accessible:
                new_accessible.update(self._process_all_symbols(state))
            accessible.update(prev_accessible)
            prev_accessible.clear()
            prev_accessible.update(new_accessible)
            new_accessible.clear()
        
        unaccessible = self.states - accessible

        # remove unaccessible states and transitions
        for state in unaccessible:
            # remove state
            self.states.remove(state)

            # remove its transitios
            trans_to_remove = set()
            for trans in self.transitions:
                if state == trans.initial_state or state == trans.final_state:
                    trans_to_remove.add(trans)

            self.transitions = tuple(set(self.transitions) - set(trans_to_remove))

    def _process_all_symbols(self, current_state: State): # ->
        new_states = set()

        for trans in self.transitions:
            if current_state == trans.initial_state:
                new_states.add(trans.final_state)
            
        return new_states

    def _group_equivalent_states(self):
        states = list(self.states)
        len_states = len(states)

        # create table
        table = dict()
        # table['States'] = states
        # len_states = len(states) - 1
        # for state in states:
        #     table[state] = [0]*len_states
        #     len_states -= 1

        for s1 in range(len_states):
            for s2 in range(s1+1,len_states):
                if (states[s1].is_final and not states[s2].is_final) or (not states[s1].is_final and states[s2].is_final):
                    table[(s1,s2)] = 1
                else:
                    table[(s1,s2)] = 0
                
        # fill in table
        #flag = True
        #while flag:
        #    flag = False
        #    for s1 in range(len_states):
        #        for s2 in range(s1+1, len_states):
        #            if table[(s1,s2)]:
        #                continue
        #            for symbol in self.symbols:
        #                next1 = self._process_symbol({states[s1]}, symbol).pop()
        #                next2 = self._process_symbol({states[s2]}, symbol).pop()
        #                if (next1.is_final and not next2.is_final) or (not next1.is_final and next2.is_final):
        #                    table[(s1,s2)] = 1
        #                    flag = True
        #                    break

        ##### WIKIPEDIA pero no tira #######
        #finals = {state for state in states if state.is_final}
        #not_finals = set(states) - finals
        #quo1 = [finals, not_finals]
        #quo2 = [finals, not_finals]
        #while quo2:
        #    A = quo2.pop()
        #    for symbol in self.symbols:
        #        X = set()
        #        for trans in self.transitions:
        #            if trans.final_state in A:
        #                X.add(trans.initial_state)
        #        new_quo1 = []
        #        new_quo2 = []
        #        for Y in quo1:
        #            if X&Y and Y-X:
        #                new_quo1.append(X&Y)
        #                new_quo1.append(Y-X)
        #                if Y in quo2:
        #                    new_quo2.append(X&Y)
        #                    new_quo2.append(Y-X)
        #                else:
        #                    if len(X&Y) <= len(Y-X):
        #                        new_quo2.append(X&Y)
        #                    else:
        #                        new_quo2.append(Y-X)
        #            else:
        #                new_quo1.append(Y)
        #        quo2 = new_quo2
        #        quo2 = new_quo2

        # con la captura esa que hice
        flag = True
        while flag:
            flag = False
            for s1 in range(len_states):
                for s2 in range(s1+1, len_states):
                    if table[(s1,s2)]:
                        continue
                    for symbol in self.symbols:
                        next1 = states.index(self._process_symbol({states[s1]}, symbol).pop())
                        next2 = states.index(self._process_symbol({states[s2]}, symbol).pop())
                        if (next1, next2) in table.keys():
                            if table[(next1,next2)]:
                                table[(s1,s2)] = 1
                                flag = True
                                break
                        if (next2, next1) in table.keys():
                            if table[(next2,next1)]:
                                table[(s1,s2)] = 1
                                flag = True
                                break

        # combine equivalent states
        pair_of_states = []
        for s1 in range(len_states):
            for s2 in range(s1+1, len_states):
                if not table[(s1,s2)]:
                    pair_of_states.append({s1,s2})

        merged_states = []
        for p1 in range(len(pair_of_states)):
            union = pair_of_states[p1]
            for p2 in range(p1+1, len(pair_of_states)):
                if pair_of_states[p1] & pair_of_states[p2]:
                    union = union.union(pair_of_states[p2])
            skip = False
            for merge_s in merged_states:
                if union <= merge_s:
                    skip = True
                    break
            if not skip:
                merged_states.append(union)
        for s1 in range(len_states): # add nor merged states
            if not any(s1 in subs for subs in merged_states):
                merged_states.append({s1})

        a = 'fifiiin'
        