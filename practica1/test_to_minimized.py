"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_minimized()
        equiv_map = deterministic_automata_isomorphism( 
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)

    # example from https://www.javatpoint.com/minimization-of-dfa
    def test_case1(self) -> None:
        """Test Case 1."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3 final
            q4
            q5 final

            --> q0
            q0 -0-> q1
            q0 -1-> q3
            q1 -0-> q0
            q1 -1-> q3
            q2 -0-> q1
            q2 -1-> q4
            q3 -0-> q5
            q3 -1-> q5
            q4 -0-> q3
            q4 -1-> q3
            q5 -0-> q5
            q5 -1-> q5
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q3 final

            --> q0
            q0 -0-> q1
            q0 -1-> q3
            q1 -0-> q0
            q1 -1-> q3
            q3 -0-> q3
            q3 -1-> q3

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
