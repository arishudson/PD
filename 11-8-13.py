import random

class SimpleGame(object):
    
    payoffMatrix = [ [(3,3), (0,5)] , [(5,0), (1,1)] ]
    
    history = []
    
    def __init__(self, playerList):
        
        self.players = playerList
        
    def payoff(self, moves):
        
        return self.payoffMatrix[moves[0]][moves[1]]
        
    def run(self):
        
        outcome = [self.players[0].move(),self.players[1].move()]
        
        scores = self.payoff(outcome)
        
        self.players[0].record(outcome,scores)
        
        self.players[1].record(outcome,scores)
        
        self.history.append([outcome,scores])
        
        return [outcome, scores]

class RandomPlayer(object):
    
    p_defect = 0.5
    
    game = []
    
    def __init__(self,pd):
        
        self.p_defect = pd
        
    def move(self):
        
        r = random.random()
        
        if r < self.p_defect:
            
            return 0
            
        else:
            
            return 1
    
    def record(self, outcome, score):
        
        pass
    


player1 = RandomPlayer(0.5)
player2 = RandomPlayer(0.25)
SG = SimpleGame([player1,player2])

result = SG.run()

print result

SG2 = SimpleGame([player1,player2])

for t in range(100):
    SG2.run()
print SG2.history