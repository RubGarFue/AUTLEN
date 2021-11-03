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

            q0q1
            q3q5 final

            --> q0q1
            q0q1 -0-> q0q1
            q0q1 -1-> q3q5
            q3q5 -0-> q3q5
            q3q5 -1-> q3q5

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


    # example from slides in Moodle
    def test_case2(self) -> None:
        """Test Case 2."""
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

    
    # example from wikipedia
    def test_case3(self) -> None:
        """Test Case 3."""
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


    # example from https://www.gatevidyalay.com/minimization-of-dfa-minimize-dfa-example/
    def test_case4(self) -> None:
        """Test Case 4."""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3
            q4 final

            --> q0
            q0 -a-> q1
            q0 -b-> q2
            q1 -a-> q1
            q1 -b-> q3
            q2 -a-> q1
            q2 -b-> q2
            q3 -a-> q1
            q3 -b-> q4
            q4 -a-> q1
            q4 -b-> q2
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0q2
            q1
            q3
            q4 final

            --> q0q2
            q0q2 -a-> q1
            q0q2 -b-> q0q2
            q1 -a-> q1
            q1 -b-> q3
            q3 -a-> q1
            q3 -b-> q4
            q4 -a-> q1
            q4 -b-> q0q2

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


    def test_case5(self) -> None:
        """Test Case 5."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3
            q4 final

            --> q0
            q0 -0-> q1
            q0 -1-> q3
            q1 -0-> q2
            q1 -1-> q4
            q2 -0-> q1
            q2 -1-> q4
            q3 -0-> q2
            q3 -1-> q4
            q4 -0-> q4
            q4 -1-> q4
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q1q2q3
            q4 final

            --> q0
            q0 -0-> q1q2q3
            q0 -1-> q1q2q3
            q1q2q3 -0-> q1q2q3
            q1q2q3 -1-> q4
            q4 -0-> q4
            q4 -1-> q4

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

if __name__ == '__main__':
    unittest.main()
