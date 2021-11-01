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

    # example from wikipedia
    def test_case1(self) -> None:
        """Test Case 1."""
        automaton_str = """
        Automaton:
            Symbols: 01

            A
            B
            C final
            D final
            E final
            F

            --> A
            A -0-> B
            A -1-> C
            B -0-> A
            B -1-> D
            C -0-> E
            C -1-> F
            D -0-> E
            D -1-> F
            E -0-> E
            E -1-> F
            F -0-> F
            F -1-> F
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            AB
            CDE final
            F

            --> AB
            AB -0-> AB
            AB -1-> CDE
            CDE -0-> CDE
            CDE -1-> F
            F -0-> F
            F -1-> F

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
