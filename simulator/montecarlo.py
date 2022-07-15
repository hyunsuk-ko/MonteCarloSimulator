import pandas as pd
import numpy as np

class Die:
    """
    General Definition
     :A die has N sides, or “faces”, and W weights, and can be rolled to select a face. 

- W defaults to 1.0 for each face but can be changed after the object is created.
- Note that the weights are just numbers, not a normalized probability distribution.
- The die has one behavior, which is to be rolled one or more times.
- Note that what we are calling a “die” here can be any discrete random variable associated with a stochastic process, such as using a deck of cards or flipping a coin or speaking a language. Our probability model for such variable is, however, very simple – since our weights apply to only to single events, we are assuming that the events are independent. This makes sense for coin tosses but not for language use.
    """
    def __init__(self, faces):
        """
        - Takes an array of faces as an argument. The array's data type (dtype) may be strings or numbers.
        - Internally iInitializes the weights to 1.0 for each face.
        """
        if type(faces) != list:
            raise ValueError("Type should be list.")
        self.faces = faces
        self.weights = [1.0] * len(faces)
        self.df = pd.DataFrame({'faces': self.faces, 'weights': self.weights})
        
    def change_weight(self, new_face, new_weight):
        """
        A method to change the weight of a single side.
        - Takes two arguments: the face value to be changed and the new weight.
        """
        if (new_face not in self.faces) or (type(new_weight) != float):
            return False
        
        idx = self.df[self.df['faces'] == new_face].index.values[0] # finding an index of face 
        self.weights[idx] = new_weight # setting weight of the index with new weight.
        self.df = pd.DataFrame({'faces': self.faces, 'weights': self.weights})
        return True
    
    def roll_die(self, roll_times = 1):
        """
        A method to roll the die one or more times
        """
        if type(roll_times) != int:
            return False
        
        self.roll_times = roll_times
        self.probabilities = [round(p / sum(self.weights),10) for p in self.weights] # Convert weights such that sums up to 1.
        self.outcome = np.random.choice(self.faces, self.roll_times, p = self.probabilities)
        return self.outcome
    
    def show_curr(self):
        """
        - A method to show the user the die’s current set of faces and weights (since the latter can be changed).
        """
        #print()
        #print("---------------DEFAULT VERSION----------------") 
        #print(self.df)
        return self.df
    
    
class Game:
    """
    General Definition
     : A game consists of rolling of one or more dice of the same kind one or more times. 

    - Each game is initialized with one or more of similarly defined dice (Die objects).
    - By “same kind” and “similarly defined” we mean that each die in a given game has the same number of sides and associated faces, but each die object may have its own weights.
    - The class has a behavior to play a game, i.e. to rolls all of the dice a given number of times.
    - The class keeps the results of its most recent play. 
    """
    result_df = pd.DataFrame({'roll_number': [], 'die_number': [], 'result': []})
    
    def __init__(self, die_objs):
        """
        Takes a single parameter, a list of already instantiated similar Die objects.
        """
        if type(die_objs) != list:
            raise ValueError("Type should be list.")
        self.die_objs = die_objs 
               
    def play_game(self, game_times):
        """
        Takes a parameter to specify how many times the dice should be rolled.
        """
        if type(game_times) != int:
            raise ValueError("Type should be int.")
        self.__result__ = pd.DataFrame({'roll_number': [], 'die_number': [], 'result': []}) #Game.result_df.copy()
        self.game_times = game_times
        count = 0
        
        finals = []
        for game_time in range(game_times):
            results = []
            for obj in self.die_objs:
                #faces = obj.roll_die(obj.roll_times)
                faces = obj.roll_die(len(self.die_objs[0].faces))
                for face in faces:
                    results.append(face)
            finals.append(results)
        
        for roll_number in range(game_times):
            for die_number in range(len(self.die_objs[0].faces)):
                #print(game_times)
                #print(len(self.die_objs[0].faces))
                
                new_df = pd.DataFrame({'roll_number' : [roll_number], 'die_number' : [die_number], 'result' : finals[roll_number][die_number]})
                self.__result__ = pd.concat([self.__result__, new_df], axis = 0)
        self.__result__.index = np.arange(len(self.__result__))
        #print()
        #print("--------------PLAY GAME-----------------")
        #print(self.__result__)

    def show(self, form = "wide"): # A method to show the user the results of the most recent play.
        """
        Show the user the results of the most recent play.
        
        - The narrow form of the dataframe will have a two-column index with the roll number and the die number,
         and a column for the face rolled.
         
        - The wide form of the dataframe will a single column index with the roll number, and each die number as a column.
        """
        if form not in ["wide", "narrow"]:
            raise ValueError("Enter wide or narrow.")
                  
        if form == "narrow": # have a two-column index with the roll number and the die number, and a column for the face rolled.  
            narrow_df = self.__result__.copy() 
            # Create a multi-index, using `roll number`, 'die number' as part of the key.
            narrow_df = narrow_df.set_index(['roll_number'])
            narrow_df = narrow_df.reset_index().set_index(['roll_number', 'die_number']) 
            #print()
            #print("---------------NARROW VERSION----------------") 
            #print(narrow_df)
            return narrow_df
        
        elif form == "wide": # a single column index with the roll number, and each die number as a column.
            wide_df = self.__result__.copy().pivot(index = 'roll_number', columns = 'die_number', values = 'result')
            #print()
            #print("---------------WIDE VERSION----------------") 
            #print(wide_df)            
            return wide_df
        
class Analyzer:
    """
    General Definition
    : An analyzer takes the results of a single game and computes various descriptive statistical properties about it. These properties results are available as attributes of an Analyzer object. Attributes (and associated methods) include:
    """
    def __init__(self, game_obj):
        """
        Takes a game object as its input parameter. 
        """ 
        self.game_obj = game_obj
        self.die_objs = game_obj.die_objs  # sample_die, sample_die_2
        # has an index of the roll number and face values as columns (i.e. it is in wide format).
        self.face_counts_per_roll = pd.DataFrame({'roll_number': [], 'face_count': []}) 
        self.jackpot_count = 0 # how many times a roll resulted in all faces being the same, e.g. all one for a six-sided die.
        self.combo_count = pd.DataFrame({'Combination' : [], 'Occurrence' : []})
        self.all_jackpot_results = pd.DataFrame({'Jackpot': [], 'Combination' : []})
            
    def jackpot(self):
        # roll_times = 3 | play_game
        """
        Compute how many times the game resulted in all faces being identical.
        """
        obj_jackpot_result = pd.DataFrame({'Jackpot': [], 'Combination' : []})
        game_iteration = self.game_obj.game_times
        #print("game iteration: ", game_iteration)
        for i in range(game_iteration): # 3
            result_face = []
            for die_obj in self.die_objs: # 2
                curr_outcome = die_obj.roll_die()[0]
                #print(curr_outcome)
                result_face.append(curr_outcome)
            #print(result_face)
            #print()
            if (len(set(result_face)) == 1): # JACKPOT
                self.jackpot_count += 1
                curr_df = pd.DataFrame({'Combination' : [sorted(result_face)], 'Jackpot': [1]})
            else:
                curr_df = pd.DataFrame({'Combination' : [sorted(result_face)], 'Jackpot': [0]})
            obj_jackpot_result =  pd.concat([obj_jackpot_result, curr_df])
        obj_jackpot_result.index = np.arange(len(obj_jackpot_result))
        self.all_jackpot_results = pd.concat([self.all_jackpot_results, obj_jackpot_result])
        #print()
        #print("---------------JACKPOT----------------")   
        #print(self.all_jackpot_results)
        #print("Total Jackpot count:", self.jackpot_count)
        return self.jackpot_count            

  
    def combo(self):
        """
        Compute the distinct combinations of faces rolled, along with their counts.
        """
        count = self.all_jackpot_results['Combination'].value_counts()
        
        # Stores the results as a dataframe in a public attribute.
        count_df = pd.DataFrame({'Combination': count.index, 'Occurrence': count.values})
        
        # Combinations should be sorted and saved as a multi-columned index.
        self.combo_count = pd.concat([self.combo_count, count_df])
        
        #print()
        #print("---------------COMBO----------------") 
        #print(self.combo_count)
        return self.combo_count
    
    def face_count(self):
        """
        Compute how many times a given face is rolled in each event.
        """
        faces = self.die_objs[0].faces.copy()
        all_counts = []
        
        for combo in self.all_jackpot_results['Combination']:
            face_dict = dict()
            for face in faces:
                face_dict[face] = 0
            for head in combo:        
                face_dict[head] += 1
            all_counts.append(list(face_dict.values()))
        
        face_df = pd.DataFrame()       
        for face in list(face_dict.keys()):   
            face_df[face] = []
        
        for i in range(len(all_counts)):
            face_df.loc[len(face_df)] = all_counts[i] # appending every roll result to df
            
        face_df.index.name = 'roll_number'
        #print()
        #print("---------------FACE COUNT----------------") 
        #print(face_df)
        return face_df

         
if __name__ == '__main__':
    sample_die = Die(['a','b','c'])
    sample_die.change_weight('a', 2.0)
    sample_die.roll_die() # SHOULD BE IDENTCIAL TO NUMBER OF DIE INSTANCES.
    #sample_die.show_curr()
    
    sample_die_2 = Die(['a','b','c'])
    sample_die_2.change_weight('c', 5.0)
    sample_die_2.roll_die()
    #sample_die_2.show_curr()    
    
    sample_die_3 = Die(['a','b','c'])
    sample_die_3.change_weight('b', 15.0)
    sample_die_3.roll_die()
    
    game = Game([sample_die, sample_die_2, sample_die_3])
    game.play_game(5)
    game.show('narrow')
    game.show('wide')
    
    analyzer = Analyzer(game)
    analyzer.jackpot()
    analyzer.combo()
    analyzer.face_count()

    


       