from typing import Collection, Set


def to_minimized(self):# -> "FiniteAutomaton":
    self._remove_unaccesible_states()



def _remove_unaccesible_states(self) -> None:
    # find accessible states
    accessible = set()
    prev_accessible = set(self.initial_state)
    new_accessible = set()

    for i in range(1, len(self.states)):
        for state in prev_accessible:
            new_accessible.update(_process_all_symbols(state))
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
            if states[s1].is_final or states[s2].is_final:
                table[(s1,s2)] = 1
            else:
                table[(s1,s2)] = 0
            
    # fill in table
    flag = True
    while flag:
        flag = False
        for s1 in range(len_states):
            for s2 in range(len_states):
                if table[(s1,s2)]:
                    continue
                for symbol in self.symbols:
                    next1 = _process_symbol(set(states[s1]), symbol).pop()
                    next2 = _process_symbol(set(states[s2]), symbol).pop()
                    if (next1.is_final and not next2.is_final) or (not next1.is_final and next2.is_final):
                        table[(s1,s2)] = 1
                        flag = True
                        break

    # combine equivalent states
    new_states = set()
    for s1 in range(len_states):
        equiv_states = set()
        for s2 in range(len_states):
            if not table[(s1,s2)]:
                equiv_states.add(s2)
        if equiv_states:
            new_state = self._combine_states(equiv_states.add(s1))
            new_states.add(new_state)
        else:
            new_states.add(s1)