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

    # example from slides in Moodle
    def test_case1(self) -> None:
        """Test Case 1."""
        automaton_str = """
        Automaton:
            Symbols: 01

            A
            B
            C final
            D
            E
            F
            G
            H

            --> A
            A -0-> B
            A -1-> F
            B -0-> G
            B -1-> C
            C -0-> A
            C -1-> C
            D -0-> C
            D -1-> G
            E -0-> H
            E -1-> F
            F -0-> C
            F -1-> G
            G -0-> G
            G -1-> E
            H -0-> G
            H -1-> C
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            AE
            BH
            C final
            F
            G

            --> AE
            AE -0-> BH
            AE -1-> F
            BH -0-> G
            BH -1-> C
            C -0-> AE
            C -1-> C
            F -0-> C
            F -1-> G
            G -0-> G
            G -1-> AE

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
