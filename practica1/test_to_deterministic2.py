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
            Symbols: abc

            q0
            q1
            q2
            q3
            q4
            q5
            q6
            q7
            qf final

            --> q0
            q0 --> q1
            q0 --> qf
            q1 --> q2
            q1 --> q5
            q2 -a-> q3
            q3 -b-> q4
            q4 --> q7
            q5 -c-> q6
            q6 --> q7
            q7 --> q1
            q7 --> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: abc

            q0 final
            q1 final
            q2 final
            q3
            empty

            --> q0
            q0 -a-> q3
            q0 -b-> empty
            q0 -c-> q1
            q1 -a-> q3
            q1 -b-> empty
            q1 -c-> q1
            q2 -a-> q3
            q2 -b-> empty
            q2 -c-> q1
            q3 -a-> empty
            q3 -b-> q2
            q3 -c-> empty
            empty -a-> empty
            empty -b-> empty
            empty -c-> empty

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
