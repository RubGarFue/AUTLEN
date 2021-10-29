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
        transformed = automaton.to_deterministic()
        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)

    def test_case1(self) -> None:
        """Test Case 1."""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3 final

            --> q0
            q0 -a-> q0
            q0 -b-> q0
            q0 -a-> q1
            q1 -b-> q2
            q2 -a-> q3
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            qf final

            --> q0
            q0 -a-> q1
            q0 -b-> q0
            q1 -a-> q1
            q1 -b-> q2
            q2 -a-> qf
            q2 -b-> q0
            qf -a-> q1
            qf -b-> q2
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
