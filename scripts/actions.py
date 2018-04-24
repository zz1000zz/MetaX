####################################################
def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} taps {}.'.format(me, card))
    else:
        notify('{} untaps {}.'.format(me, card))	

def untapAll(group, x = 0, y = 0): #Modified it to account for Energy which will be played upside down
	mute()
	for card in group:
		if not card.owner == me:
			continue
		if card.orientation == Rot90:
			card.orientation = Rot0
		if card.orientation == Rot270:
			card.orientation = Rot180
	notify("{} untaps all their cards.".format(me))			
			
			
def clearAll(group, x = 0, y= 0):
    notify("{} clears all targets and combat.".format(me))
    for card in group:
		if card.controller == me:
			card.target(False)
			card.highlight = None

def roll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))
		  
def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))

def discard(card, x = 0, y = 0): #Renamed
	card.moveTo(me.piles['Discard Pile'])
	notify("{} discards {}".format(me, card))

def addCounter(card, x = 0, y = 0):
	mute()
	notify("{} adds 1 counter to {}.".format(me, card))
	card.markers[CounterMarker] += 1

def removeCounter(card, x = 0 , y = 0):
	mute()
	notify("{} removes 1 counter to {}.".format(me, card))
	card.markers[CounterMarker] -= 1
	  
def setCounter(card, x = 0, y = 0):
	mute()
	quantity = askInteger("How many counters", 0)
	notify("{} sets {} counters on {}.".format(me, quantity, card))
	card.markers[CounterMarker] = quantity	
		
def play(card, x = 0, y = 0): #Extra Cards will go to Drop after being played
	mute()
	src = card.group
	if card.Type=="Extra": card.moveTo(card.owner.piles['Drop Zone'])
	elif me.id == 1:
                global xBattle
		xBattle += 75
		card.moveToTable(xBattle, 0)
	else:
                global XBattle2
                xBattle -= 75
                card.moveToTable(xBattle2, -90)
	notify("{} plays {} from their {}.".format(me, card, src.name))

def toVP(card, y = 90):
		mute()
		src = card.group
                card.moveTo(card.owner.piles['VP'])
		notify("{} gives up a Victory Point.".format(me))
		
def topCardVP(group, count = 1, x = 0, y = 0):
	mute()
	for i in range(0,count):
		if len(group) == 0: return
		card = group[0]
		toVP(card)

def randomDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	notify("{} randomly discards {}.".format(me,card.name))
	card.moveTo(me.piles['Discard Pile'])

def randomDraw(group):
	mute()
	card = group.random()
	if card == None: return
	notify("{} takes a random VP.".format(me))
        card.moveTo(card.owner.hand)

def draw(group, conditional = False, count = 1, x = 0, y = 0): #Added draw function to include choice
    mute()
    for i in range(0,count):
        if len(group) == 0:
            return
        if conditional == True:
            choiceList = ['Yes', 'No']
            colorsList = ['#FF0000', '#FF0000']
            choice = askChoice("Draw a card?", choiceList, colorsList)
            if choice == 0 or choice == 2:
                return 
        card = group[0]
        card.moveTo(card.owner.hand)
        notify("{} draws a card.".format(me))

def drawMany(group, count = None):
	if len(group) == 0: return
	mute()
	if count == None: count = askInteger("Draw how many cards?", 0)
	for card in group.top(count): card.moveTo(me.hand)
	notify("{} draws {} cards.".format(me, count))

def drawBottom(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group.bottom().moveTo(me.hand)
	notify("{} draws a card from the bottom.".format(me))

def shuffle(group):
	group.shuffle()
  
def lookAtTopCards(num, targetZone='hand'): #Added function for looking at top X cards and take a card
    mute()
    notify("{} looks at the top {} cards of their deck".format(me,num))
    cardList = [card for card in me.Deck.top(num)]
    choice = askCard(cardList, 'Choose a card to take')
    toHand(choice, show = True)
    me.Deck.shuffle() 
	
def lookAtDeck(): #For Automation
    mute()
    notify("{} looks at their Deck.".format(me))
    me.Deck.lookAt(-1)
	
#---------------------------------------------------------------------------
# Phases
#---------------------------------------------------------------------------

def showCurrentPhase(phaseNR = None): # Just say a nice notification about which phase you're on.
   if phaseNR: notify(phases[phaseNR])
   else: notify(phases[num(me.getGlobalVariable('phase'))])

def endMyTurn(opponent = None):
   if not opponent: opponent = findOpponent()
   me.setGlobalVariable('phase','0') # In case we're on the last phase (Force), we end our turn.
   notify("=== {} has ended their turn ===.".format(me))
   opponent.setActivePlayer() 
      
def nextPhase(group = table, x = 0, y = 0, setTo = None):  
# Function to take you to the next phase. 
   mute()
   phase = num(me.getGlobalVariable('phase'))
   if phase == 3: 
      endMyTurn()
      return  
   else:
      if not me.isActivePlayer and confirm("Your opponent does not seem to have ended their turn yet. Switch to your turn?"):
         remoteCall(findOpponent(),'endMyTurn',[me])
         rnd(1,1000) # Pause to wait until they change their turn
      phase += 1
      if phase == 1: goToDraw()
      elif phase == 2: goToPlanning()
      elif phase == 3: goToDeclare()

def goToDraw(group = table, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('phase','1')
   showCurrentPhase(1)
         
def goToPlanning(group = table, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('phase','2')
   showCurrentPhase(2)
         
def goToDeclare(group = table, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('phase','3')
   showCurrentPhase(3)

#---------------------------------------------------------------------------
# Meta Functions
#---------------------------------------------------------------------------
def findOpponent(position = '0', multiText = "Choose which opponent you're targeting with this effect."):
   opponentList = fetchAllOpponents()
   if len(opponentList) == 1: opponentPL = opponentList[0]
   else:
      if position == 'Ask':
         choice = SingleChoice(multiText, [pl.name for pl in opponentList])
         opponentPL = opponentList[choice]         
      else: opponentPL = opponentList[num(position)]
   return opponentPL

def fetchAllOpponents(targetPL = me):
   opponentList = []
   if len(getPlayers()) > 1:
      for player in getPlayers():
         if player != targetPL: opponentList.append(player) # Opponent needs to be not us, and of a different type. 
   else: opponentList = [me] # For debug purposes
   return opponentList   

def playerside():
   if me.hasInvertedTable(): side = -1
   else: side = 1   
   return side
   
 
#------------------------------------------------------------------------------
# Button and Announcement functions
#------------------------------------------------------------------------------

def BUTTON_OK(group = None,x=0,y=0):
   notify("--- {} has no further reactions.".format(me))

def BUTTON_Wait(group = None,x=0,y=0):  
   notify("--- Wait! {} wants to react.".format(me))

def BUTTON_Actions(group = None,x=0,y=0):  
   notify("--- {} is waiting for opposing actions.".format(me))

def declarePass(group, x=0, y=0):
   notify("--- {} Passes".format(me))    

