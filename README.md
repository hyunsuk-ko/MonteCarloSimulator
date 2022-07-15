# MonteCarloSimulator

## MetaData 
- Name: Hyun Ko
- Project: Monte Carlo Simulator
- Release Date: 07/14/2022
    
    
## Synopsis
### installing:
- Clone this repo to your computer.
- Type below to your shell:
```
pip install -e .
```

### Importing
```
from montecarlo import Die, Game, Analyzer
```

### Creating dice
```
sample_die = Die(['a','b','c']) # Can be any faces in string
```

### Playing games
```
game = Game([sample_die])
game.play_game(5) # Any integer 
```

### Analyzing games
```
analyzer = Analyzer(game)
analyzer.jackpot()
analyzer.combo()
analyzer.face_count()
```

## API Description

### Die Class
: A die has N sides, or “faces”, and W weights, and can be rolled to select a face. 

#### Attributes
- self.faces = faces
- self.weights = [1.0] * len(faces)
- self.df = pd.DataFrame({'faces': self.faces, 'weights': self.weights})

#### Methods
- init(self, faces)
: Takes an array of faces as an argument. The array's data type (dtype) may be strings or numbers. Internally iInitializes the weights to 1.0 for each face.
    
- change_weight(self, new_face, new_weight)
: A method to change the weight of a single side. Takes two arguments: the face value to be changed and the new weight (float). Returns boolean value whether weight change is successful.
    
- roll_die(self, roll_times = 1): A method to roll the die one or more times (default roll_times = 1). Returns False with invalid given parameter or list of rollled die outcomes.
    
- show_curr(self): A method to show the user the die’s current set of faces and weights (since the latter can be changed). Returns dataframe.
    
    

### Game Class
: A game consists of rolling of one or more dice of the same kind one or more times. 

#### Attributes
- self.die_objs = die_objs
    
#### Methods
- __init__(self, die_objs)
: Takes a single parameter, a list of already instantiated similar Die objects.
    
- play_game(self, game_times)
: Takes a parameter to specify how many times the dice should be rolled. Stores game results in a dataframe.
    
- show(self, form = "wide")
: A method to show the user the results of the most recent play. Show the user the results of the most recent play. The narrow form of the dataframe will have a two-column index with the roll number and the die number, and a column for the face rolled. The wide form of the dataframe will a single column index with the roll number, and each die number as a column.
    

    
### Analyzer Class
: An analyzer takes the results of a single game and computes various descriptive statistical properties about it. These properties results are available as attributes of an Analyzer object. Attributes (and associated methods) include
    
#### Attributes
- self.game_obj = game_obj
- self.die_objs = game_obj.die_objs
- self.face_counts_per_roll = pd.DataFrame({'roll_number': [], 'face_count': []}) 
- self.jackpot_count = 0 
- self.combo_count = pd.DataFrame({'Combination' : [], 'Occurrence' : []})
- self.all_jackpot_results = pd.DataFrame({'Jackpot': [], 'Combination' : []})
    
    
#### Methods
- __init__(self, game_obj)
: Takes a game object as its input parameter. 
    
- jackpot(self)
: Compute how many times the game resulted in all faces being identical.
    
- combo(self)
: Compute the distinct combinations of faces rolled, along with their counts.
    
- face_count(self)
: Compute how many times a given face is rolled in each event.
    
    
    
    
## Manifest
Type below to your shell to checkout file listings.
```
!ls -lR    
```

    
