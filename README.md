# MonteCarloSimulator

## MetaData 
    - Name: Hyun Ko
    - Project: Monte Carlo Simulator
    
    
## Synopsis
### installing:
- Clone this repo to your computer.
- Type below to your shell:
```
pip install -e .
```

### importing:
```
from montecarlo import Die, Game, Analyzer
```

### Creating dice
```
sample_die = Die(['a','b','c'])
```

### Playing games
```
game = Game([sample_die])
game.play_game(5) # Any integer 
```

### Analyzing games.
```
analyzer = Analyzer(game)
analyzer.jackpot()
analyzer.combo()
analyzer.face_count()
```



## API Description
