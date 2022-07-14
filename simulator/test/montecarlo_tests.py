import unittest
from montecarlo import Die, Game, Analyzer
import pandas as pd

class MonteCarloTestSuite(unittest.TestCase):
    def test_0_die_init(self): # Add a book and test if it is in `book_list`
        with self.assertRaises(ValueError) as exception_context:
            Die(('H','T'))
        self.assertEqual(str(exception_context.exception),"Type should be list.")
        
    def test_01_die_change_weight(self): # Add a book and test if it is in `book_list`
        test_1 = Die(['H','T'])
        testValue = test_1.change_weight('H', 10.0)
        message = "Test value is not true."
        self.assertTrue(testValue, message)
        
    def test_02_die_change_weight(self): # Add a book and test if it is in `book_list`
        test_2 = Die(['H','T'])
        testValue = test_2.change_weight('H', 1)
        message = "Test value is not false."
        self.assertFalse(testValue, message)

    def test_03_die_change_weight(self): # Add a book and test if it is in `book_list`
        test_3 = Die(['H','T'])
        testValue = test_3.change_weight('A', 10.0)
        message = "Test value is not false."
        self.assertFalse(testValue, message)
        
    def test_04_die_roll_die(self): 
        test_4 = Die(['H','T'])
        test_4.change_weight('H', 100.0)
        actual = test_4.roll_die(3)[0]
        expected = 'H'
        self.assertEqual(actual, expected)
        
    def test_05_die_roll_die(self): # Add a book and test if it is in `book_list`
        test_5 = Die(['H','T'])
        testValue = test_5.roll_die("A")
        message = "Test value is not false."
        self.assertFalse(testValue, message)
        
    def test_06_game_init(self): # Add a book and test if it is in `book_list`
        with self.assertRaises(ValueError) as exception_context:
            Game(('H','T'))
        self.assertEqual(str(exception_context.exception),"Type should be list.")
        
    def test_07_game_play_game(self): # Add a book and test if it is in `book_list`
        sample_die = Die(['H','T'])
        sample_die.roll_die()
        sample_die_2 = Die(['H','T'])
        sample_die_2.roll_die()
        game = Game([sample_die, sample_die_2])
        with self.assertRaises(ValueError) as exception_context:
            game.play_game(5.48)
        self.assertEqual(str(exception_context.exception),"Type should be int.")
        
    def test_08_game_play_game(self): # Add a book and test if it is in `book_list`
        sample_die = Die(['H','T'])
        sample_die.roll_die()
        sample_die_2 = Die(['H','T'])
        sample_die_2.roll_die()
        game = Game([sample_die, sample_die_2])
        game.play_game(5)
        with self.assertRaises(ValueError) as exception_context:
            game.show("ab")
        self.assertEqual(str(exception_context.exception),"Enter wide or narrow.")

    def test_10_analyzer_jackpot(self):
        sample_die = Die(['H','T'])
        sample_die.roll_die()
        sample_die.change_weight('H', 100.0)
        game = Game([sample_die])
        game.play_game(5)
        analyzer = Analyzer(game)
        actual = analyzer.jackpot()
        expected = 5
        self.assertEqual(actual, expected)
        
    def test_11_analyzer_combo(self):
        sample_die = Die(['H','T'])
        sample_die.roll_die()
        sample_die_2 = Die(['H','T'])
        sample_die_2.roll_die()
        game = Game([sample_die, sample_die_2])
        game.play_game(5)
        analyzer = Analyzer(game)
        analyzer.jackpot()
        actual = analyzer.combo().iloc[0]['Occurrence']
        expected = 2
        self.assertEqual(actual, expected)
        
    def test_12_analyzer_face_count(self):
        sample_die = Die(['H','T'])
        sample_die.roll_die()
        sample_die.change_weight('T', 100.0)
        game = Game([sample_die])
        game.play_game(5)
        analyzer = Analyzer(game)
        analyzer.jackpot()
        analyzer.combo()
        actual = analyzer.face_count().iloc[0]['H']
        expected = 0
        self.assertEqual(actual, expected)

        
if __name__ == '__main__':
    unittest.main(verbosity=3)