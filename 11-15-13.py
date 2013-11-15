import numpy

class ThreeDimLattice(object):
    
    IsLooped = True
    
    payoffMatrix = [ [(3,3), (0,5)] , [(5,0), (1,1)] ]
    
    def __init__(self, playertype, playerarg, lengths):
        
        self.lengths = lengths
        
        self.PlayerList = numpy.empty(lengths, dtype=object)
        
        for i in range(lengths[0]):
            
            for j in range(lengths[1]):
                
                for k in range(lengths[2]):
                    
                    self.PlayerList[i,j,k] = playertype(playerarg)
                    
                    self.PlayerList[i,j,k].lattice = self
        
    def payoff(self, moves):
        
        return self.payoffMatrix[moves[0]][moves[1]]
    
    
    def selectRandomPlayer(self):
        
        I = numpy.random.random_integers(0,self.lengths[0]-1)
        J = numpy.random.random_integers(0,self.lengths[1]-1)
        K = numpy.random.random_integers(0,self.lengths[2]-1)
        
        return [I,J,K]
    
    def getNeighbors(self,focal_agent_id):
        
        neighbors = []
        
        if focal_agent_id[0] == 1:
            neighbors.append([2,focal_agent_id[1],focal_agent_id[2]])
            neighbors.append([self.lengths[0] - 1,focal_agent_id[1],focal_agent_id[2]])
        elif focal_agent_id[0] == self.lengths[0] - 1:
            neighbors.append([1,focal_agent_id[1],focal_agent_id[2]])
            neighbors.append([self.lengths[0] - 2,focal_agent_id[1],focal_agent_id[2]])
        else:
            neighbors.append([focal_agent_id[0] - 1,focal_agent_id[1],focal_agent_id[2]])
            neighbors.append([focal_agent_id[0] + 1,focal_agent_id[1],focal_agent_id[2]])
        
        if focal_agent_id[1] == 1:
            neighbors.append([focal_agent_id[0], 2, focal_agent_id[2]])
            neighbors.append([focal_agent_id[0], self.lengths[1] - 1, focal_agent_id[2]])
        elif focal_agent_id[1] == self.lengths[1] - 1:
            neighbors.append([focal_agent_id[0], 1, focal_agent_id[2]])
            neighbors.append([focal_agent_id[0], self.lengths[1] - 2, focal_agent_id[2]])
        else:
            neighbors.append([focal_agent_id[0], focal_agent_id[1] - 1, focal_agent_id[2]])
            neighbors.append([focal_agent_id[0], focal_agent_id[1] + 1, focal_agent_id[2]])
            
        if focal_agent_id[2] == 1:
            neighbors.append([focal_agent_id[0],focal_agent_id[1], 2])
            neighbors.append([focal_agent_id[0],focal_agent_id[1], self.lengths[2] - 1])
        elif focal_agent_id[2] == self.lengths[2] - 1:
            neighbors.append([focal_agent_id[0], focal_agent_id[1], 1])
            neighbors.append([focal_agent_id[0],focal_agent_id[1], self.lengths[2] - 2])
        else:
            neighbors.append([focal_agent_id[0],focal_agent_id[1],focal_agent_id[2] - 1])
            neighbors.append([focal_agent_id[0],focal_agent_id[1],focal_agent_id[2] + 1])
            
        return neighbors
        
    
    def playOneRound(self,player,opponent):
        
        outcome = [player.move(),opponent.move()]
        
        scores = self.payoff(outcome)
        
        player.record(scores[0])
        
        opponent.record(scores[1])
    
    def playNeighbors(self,agent,neighbors):
        
        opplist = numpy.random.permutation(neighbors)
        
        for index in opplist:
            
            self.playOneRound(self.PlayerList[agent[0],agent[1],agent[2]], self.PlayerList[index[0],index[1],index[2]])
            
        self.PlayerList[agent[0],agent[1],agent[2]].update(opplist)
        
    def playManyGames(self,numgames):
        
        for n in range(numgames):
            
            currentagent = self.selectRandomPlayer()
            
            neighbors = self.getNeighbors(currentagent)
            
            self.playNeighbors(currentagent,neighbors)
        
        scores = {}
        
        for i in range(self.lengths[0]):
            
            for j in range(self.lengths[1]):
                
                for k in range(self.lengths[2]):
                    
                    scores[str(i) + ',' + str(j) + ',' + str(k)] = self.PlayerList[i,j,k].score
        
        totalscore = 0       
        
        for i in range(self.lengths[0]):
            
            for j in range(self.lengths[1]):
                
                for k in range(self.lengths[2]):
                    
                    totalscore += self.PlayerList[i,j,k].score
        finalstrats = {}
        
        for i in range(self.lengths[0]):
            
            for j in range(self.lengths[1]):
                
                for k in range(self.lengths[2]):
                    
                    finalstrats[str(i) + ',' + str(j) + ',' + str(k)] = self.PlayerList[i,j,k].strategy
                    
        
        print 'The total score was ' + str(totalscore) + '.'
        
        print 'The individual scores were: ' + str(scores)
        
        print 'The final strategy distribution was: ' + str(finalstrats)


class NaiveAdaptivePlayer(object):
    
    score = 0
    
    strategy = 'C'
    
    lattice = []
    
    def __init__(self,pcrazy):
        
        r = numpy.random.random()
        
        if r < pcrazy:
            
            self.IsCrazy = True
            
            self.strategy = 'D'
        
        else:
            
            self.IsCrazy = False
        
    def move(self):
        
        if self.strategy == 'C':
            
            return 0
        
        elif self.strategy == 'D':
            
            return 1
        
        else:
            print 'Help! I\'m making the wrong move!'
    
    def record(self, myscore):
        
        self.score += myscore
        
    def update(self, neighbors):
        
        if self.IsCrazy == True:
            
            pass
            
        else:
            
            nscores = []
            
            for n in neighbors:
                
                nscores.append(self.lattice.PlayerList[n[0],n[1],n[2]].score)
            
            ii = numpy.argmax(nscores)
            
            bestn = neighbors[ii]
            
            if self.score >= self.lattice.PlayerList[bestn[0],bestn[1],bestn[2]].score:
                
                pass
            
            else:
                
                self.strategy = self.lattice.PlayerList[bestn[0],bestn[1],bestn[2]].strategy

    

''' 
         
class FullRandomPlayer(object):
    
    score = 0
    
    lattice = []
    
    def __init__(self):
        
        
'''

mylat = ThreeDimLattice(NaiveAdaptivePlayer,.01,[10,10,10])
mylat.playManyGames(10000)