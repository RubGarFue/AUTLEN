"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton
from automata.re_parser_interfaces import AbstractREParser
from automata.automaton import State, Transition


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:
    
        state = State("q0", is_final=True)
        return FiniteAutomaton(initial_state=state,
                                states=(state,),
                                symbols=(),
                                transitions=())


    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
    
        q0 = State("q0")
        q1 = State("q1", is_final=True)
        trans = Transition(initial_state=q0,
                            symbol=(None,),
                            final_state=q1)
        return FiniteAutomaton(initial_sate=q0,
                                states=(q0, q1),
                                symbols=(None,),
                                transitions=(trans,))


    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        initial_state = State("q0")
        final_state = State("q1", is_final=True)
        trans = Transition(initial_state=initial_state,
                            symbol=symbol,
                            final_state=final_state)
                            
        return FiniteAutomaton(initial_state=initial_state,
                                states=(initial_state, final_state),
                                symbols=(symbol,),
                                transitions=(trans,))


    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        
        automaton_final_state = self._get_final_state(automaton)

        nextstate = len(automaton.states)
        initial_state = State("q"+str(nextstate))
        final_state = State("q"+str(nextstate+1), is_final=True)

        trans1 = Transition(initial_state=initial_state,
                            symbol=None,
                            final_state=automaton.initial_state)

        trans2 = Transition(initial_state=initial_state,
                            symbol=None,
                            final_state=final_state)
        
        trans3 = Transition(initial_state=automaton_final_state,
                            symbol=None,
                            final_state=final_state)

        trans4 = Transition(initial_state=automaton_final_state,
                            symbol=None,
                            final_state=automaton.initial_state)
        
        automaton.states += (initial_state, final_state)
        automaton.symbols += (None,)
        automaton.transitions += (trans1, trans2, trans3, trans4)

        automaton.initial_state = initial_state

        return automaton


    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:

        final_state1 = self._get_final_state(automaton1)
        final_state2 = self._get_final_state(automaton2)

        nextstate = len(automaton1.states)

        for state in automaton2.states:
            state.name = "q"+str(nextstate)
            nextstate += 1
        
        initial_state = State("q"+str(nextstate))
        final_state = State("q"+str(nextstate+1), is_final=True)

        symbols = automaton1.symbols

        for symbol in automaton2.symbols:
            if symbol not in symbols:
                symbols += (symbol,)
        
        if None not in symbols:
            symbols += (None,)

        t1 = Transition(initial_state=initial_state,
                        symbol=None,
                        final_state=automaton1.initial_state)
        t2 = Transition(initial_state=initial_state,
                        symbol=None,
                        final_state=automaton2.initial_state)
        t3 = Transition(initial_state=final_state1,
                        symbol=None,
                        final_state=final_state)
        t4 = Transition(initial_state=final_state2,
                        symbol=None,
                        final_state=final_state)
        
        states = (initial_state, final_state) + automaton1.states + automaton2.states
        transitions = (t1,t2,t3,t4) + automaton1.transitions + automaton2.transitions
        
        return FiniteAutomaton(initial_state=initial_state,
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
                                    symbols=automaton1.symbols,
                                    transitions=automaton1.transitions)
        
        final_state = self._get_final_state(automaton)

        trans = Transition(initial_state=final_state,
                            symbol=None,
                            final_state=automaton2.initial_state)
        
        nextstate = len(automaton1.states)

        for state in automaton2.states:
            state.name = "q"+str(nextstate)
            nextstate += 1
        
        symbols = automaton1.symbols

        for symbol in automaton2.symbols:
            if symbol not in symbols:
                symbols += (symbol,)
        
        if None not in symbols:
            symbols += (None,)
        
        states = automaton1.states + automaton2.states
        transitions = automaton1.transitions + automaton2.transitions + (trans,)

        return FiniteAutomaton(initial_state=automaton1.initial_state,
                               states=states,
                               symbols=symbols,
                               transitions=transitions)


    def _get_final_state(
        self,
        automaton: FiniteAutomaton
    ) -> State:
        for state in automaton.states:
            if state.is_final:
                state.is_final = False
                return state
