"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton
from automata.re_parser_interfaces import AbstractREParser
from automata.automaton import State, Transition


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:
    
        state = State("qi", is_final=True)
        return FiniteAutomaton(initial_state=state,
                                states=(state,),
                                symbols=(),
                                transitions=())


    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
    
        qi = State("qi")
        f0 = State("f0", is_final=True)
        trans1 = Transition(initial_state=qi,
                            symbol=(None,),
                            final_state=f0)
        return FiniteAutomaton(initial_sate=qi,
                                states=(qi, f0),
                                symbols=(None,),
                                transitions=(trans1,))


    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        initial_state = State("qi")
        f0 = State("f0", is_final=True)
        trans1 = Transition(initial_state=initial_state,
                            symbol=symbol,
                            final_state=f0)
                            
        return FiniteAutomaton(initial_state=initial_state,
                                states=(initial_state, f0),
                                symbols=(symbol,),
                                transitions=(trans1,))


    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        
        final_state = self._get_final_state(automaton)

        qi = State("qi")
        f0 = State("f0", is_final=True)

        trans1 = Transition(initial_state=qi,
                            symbol=None,
                            final_state=automaton.initial_state)

        trans2 = Transition(initial_state=final_state,
                            symbol=None,
                            final_state=automaton.initial_state)
        
        trans3 = Transition(initial_state=final_state,
                            symbol=None,
                            final_state=f0)

        trans4 = Transition(initial_state=qi,
                            symbol=None,
                            final_state=f0)
        
        automaton.states += (qi, f0)
        automaton.symbols += (None,)
        automaton.transitions += (trans1, trans2, trans3, trans4)

        return automaton


    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        qi = State("qi")
        f0 = State("f0", is_final=True)

        final_state1 = self._get_final_state(automaton1)
        final_state2 = self._get_final_state(automaton2)
        states = (qi, f0) + automaton1.states + automaton2.states

        for state in automaton1.states:
            print(state.name)
        
        print("---")
        for state in automaton2.states:
            print(state.name)

        print("fin")
        
        symbols = (None,) + automaton1.symbols + automaton2.symbols

        t1 = Transition(initial_state=qi,
                        symbol=None,
                        final_state=automaton1.initial_state)
        t2 = Transition(initial_state=qi,
                        symbol=None,
                        final_state=automaton2.initial_state)
        t3 = Transition(initial_state=final_state1,
                        symbol=None,
                        final_state=f0)
        t4 = Transition(initial_state=final_state2,
                        symbol=None,
                        final_state=f0)

        states = (qi, f0) + automaton1.states + automaton2.states
        transitions = (t1,t2,t3,t4) + automaton1.transitions + automaton2.transitions
        
        return FiniteAutomaton(initial_state=qi,
                                states=states,
                                symbols=symbols,
                                transitions=transitions)


    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:

        automaton = FiniteAutomaton(initial_state=automaton1.initial_state,
                                    states=automaton1.states,
                                    symbols=automaton1.symbols + automaton2.symbols + (None,),
                                    transitions=automaton1.transitions + automaton2.transitions)
        
        final_state = self._get_final_state(automaton)

        trans = Transition(initial_state=final_state,
                            symbol=None,
                            final_state=automaton2.initial_state)
        
        automaton.states += automaton2.states
        automaton.transitions += (trans,)

        return automaton


    def _get_final_state(
        self,
        automaton: FiniteAutomaton
    ) -> State:
        for state in automaton.states:
            if state.is_final:
                state.is_final = False
                return state
