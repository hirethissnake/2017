class Game:
	
	def __init__(self, size):
		"""Initialize the Game class"""
		#TODO
			#Init weight grid
			#Init grid graph
			#Init snakes
			#Init move number (how many since start of game)
		
		
	def update(self, snakeHeadPositions, foodPositions):
		"""Update game with current board from server"""
		#TODO
			#Calculate all game changes and store
	
	
	def getNextMove(self):
		""""Use all algorithms to determine the next best move for our snake"""
		#TODO
			#Run each algorithm to make decisions
			#Find best route to desired square
			#Ensure boundary is not selected (shouldn't be an issue since we would only head towards positively weighted squares anyway and boundary square do not exist according to algorithm)
			#If several candidates, pick one at random
			#Return decision
	
	
	def weightNotHitSelf(self):
		"""Weight grid to avoid snake hitting itself"""
		#TODO
			#Weight self as 0
			#Are we getting food this move? (Do we need to weight our tail 0)
	
	
	def weightNotHitOthers(self):
		"""Weight grid to avoid snake hitting other snakes"""
		#TODO
			#Weight other snakes as 0
			#Are they getting food this move? (Do we need to weigh their tails 0)
			#Are they dying this move?
			#How big are they? Don't block heads of small snakes
		
		
	def weightFood(self):
		"""Weight grid with food necessity"""
		#TODO
			#How desperately do we need food?
			#How long do we have to get there?
			
			
	def weightSmallSnakes(self):
		"""Positively weight smaller snakes for murdering purposes"""
		#TODO
			#Compare size
			#How long will it take to get to the snake?
			#How much food is around for the snake to grow?
			
		
	def weightLargeSnakes(self):
		"""Negativly weight squares where large snake heads could move to next round"""
		#TODO
			#Compare size
			#Can we get food and grow bigger?
			
		
	def weightEnclosedSpaces(self):
		"""Do not kill ourselves by picking a corner where we trap ourselves"""
		#TODO
			#How long are we?
			#Are we giving other people the opportunity to block off our exit?
			#What is the optimal traversal path to maximize future space opportunities
			#Don't limit our moves (against a surface) unless advantageous or necessary
	
	
	def weightTrapSnakes(self):
		"""Positively weight squares that will allow us to block other snakes off"""
		#TODO
			#How long are they?
			#How much traversal room are we leaving them?
			#Do they need food? Do they have it in the trapped location?
			#How long are we? Can we effectively block them for long enough?	