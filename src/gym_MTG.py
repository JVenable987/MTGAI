import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



import gym
from gym import spaces #this adds space.Tuple, and presumably other things as well
import random

# 19, 13, 3, 0, 0, 0, 25 for 3 turns
# 14, 14, 8, 0, 0, 0, 24 for 4 turns
# 8, 14, 10, 3, 0, 0, 25 for 5 turns
# 4, 13, 10, 6, 1, 0, 27 for 6 turns
# 0, 12, 10, 7, 4, 0, 27 for 7 turns
# 0, 10, 10, 7, 5, 1, 27 for 8 turns
DECK_CONTENTS = (8, 14, 10, 3, 0, 0, 25)
FINAL_TURN = 5


class MTGEnv(gym.Env):

    def __init__(self):
        #check out spaces.MultiDiscrete(), and see if it fits the situation better
        #self.observation_space = gym.spaces.Tuple(6)  # Number of state information numbers that need to be provided
        ##should provide... (as explaination, '\' is line countinuation character I believe, and ## are commented out comments so you can remove # from each line)
        
        ##game state values, Five total, maybe add if a land was played, but currently looks like land automatically played once per turn.
        ##limits are FINAL_TURN+1 for turn, FINAL_TURN for ManaLeft, Assume (FINAL_TURN+2)*(FINAL_TURN+2)is limit for CreatureDamage,
        ##and that previous number is squared for total damage
        #[Turn, ManaLeft, LandsInPlay, CreatureDamage, TotalDamage, \
        
        ##This is the hand values which is in order of, 1s, 2s,3s,4s,5s,6s, and lands I believe, and has 7 total values, can probably limit to 7 of each type
        ##but will have to have a lose if they can't play anything due to only having one type of non-land in hand, and exceeds the value limit I would guess
        #self.hand[0], self.hand[1], self.hand[2], self.hand[3], self.hand[4], self.hand[5], self.hand[6], \
        
        ##We also add in the deck states, which also has Seven total values, which can each be from 0 to 53 in general
        #self.deck.NumberOf1Cost, \
        #self.deck.NumberOf2Cost, \
        #self.deck.NumberOf3Cost, \
        #self.deck.NumberOf4Cost, \
        #self.deck.NumberOf5Cost, \
        #self.deck.NumberOf6Cost, \
        #self.deck.NumberOfLands) #and this is ending the things we are putting in.  As such, there are 5+7+7 variables for the states.
        self.action_space = gym.spaces.Discrete(7)  # Number of possible actions
        self.deck = Deck()
        self.deck.SetDeck(DECK_CONTENTS[0], DECK_CONTENTS[1], DECK_CONTENTS[2], DECK_CONTENTS[3],
                          DECK_CONTENTS[4], DECK_CONTENTS[5], DECK_CONTENTS[6])
        hand = self.deck.DrawHand()
        self.hand = Hand()
        self.hand.SetHand(hand_arr[0], hand_arr[1], hand_arr[2], hand_arr[3],
                          hand_arr[4], hand_arr[5], hand_arr[6])
        self.FinalTurn = FINAL_TURN
        self.Turn = 1
        if (self.hand.PlayCard(7)):
            self.LandsInPlay = 1
            self.ManaLeft = 1
        else:
            self.LandsInPlay = 0
            self.ManaLeft = 1
        #self.ManaLeft = LandsInPlay
        
        self.CreatureDamage = 0
        self.TotalDamage = 0
        self.CreaturesPlayedThisTurn = [0, 0, 0, 0, 0, 0]
        
        handInfo = self.hand.GetHand()
        
        state = [self.Turn, self.ManaLeft, self.LandsInPlay, self.CreatureDamage, self.TotalDamage, \
        handInfo[0], handInfo[1], handInfo[2], handInfo[3], handInfo[4], handInfo[5], handInfo[6], \
        self.deck.NumberOf1Cost, \
        self.deck.NumberOf2Cost, \
        self.deck.NumberOf3Cost, \
        self.deck.NumberOf4Cost, \
        self.deck.NumberOf5Cost, \
        self.deck.NumberOf6Cost, \
        self.deck.NumberOfLands]
        self.done = False
        self.reward = 0
        info = state
        return state, self.reward, done, info

    def step(self, action):
        # Take in the AI's action for one turn, process the results,
        # and return the game state information,
        # a reward number,
        # a value that is True if the game is over and False otherwise,
        # and some debugging information.

        # Action 0: Pass turn (then play a land if applicable).
        # Action 1-6: Play a 1-6 drop creature, do not pass turn

        done = False
        reward = 0

        #commented out before first turn code, and replaced this code in the openai gym init() and reset(), to prevent doing it multiple times in a turn
        # Done before the first turn
        #if (self.Turn == 1) and (self.hand.NumberOfLands > 0):
        #    # Play a land first thing
        #    self.hand.PlayCard(7)
        #    self.LandsInPlay += 1
        #    # Tap all lands, add mana accordingly
        #    self.ManaLeft = self.LandsInPlay

        # Actions 1-6 are done during the First Main Phase part 2
        #Maybe have no punishment, but set done = True, and the reward will return either 0 for not done, or TotalDamage if done.
        if action == 1:
            if (self.ManaLeft < 1) or (self.hand.NumberOf1Cost < 1):
                # Invalid move, punish AI, end game
                reward = -100
                done = True
            else:
                self.hand.PlayCard(1)
                self.CreaturesPlayedThisTurn[0] += 1
                self.ManaLeft -= 1
        elif action == 2:
            if (self.ManaLeft < 2) or (self.hand.NumberOf2Cost < 1):
                # Invalid move, punish AI, end game
                reward = -100
                done = True
            else:
                self.hand.PlayCard(2)
                self.CreaturesPlayedThisTurn[1] += 1
                self.ManaLeft -= 2
        elif action == 3:
            if (self.ManaLeft < 3) or (self.hand.NumberOf3Cost < 1):
                # Invalid move, punish AI, end game
                reward = -100
                done = True
            else:
                self.hand.PlayCard(3)
                self.CreaturesPlayedThisTurn[2] += 1
                self.ManaLeft -= 3
        elif action == 4:
            if (self.ManaLeft < 4) or (self.hand.NumberOf4Cost < 1):
                # Invalid move, punish AI, end game
                reward = -100
                done = True
            else:
                self.hand.PlayCard(4)
                self.CreaturesPlayedThisTurn[3] += 1
                self.ManaLeft -= 4
        elif action == 5:
            if (self.ManaLeft < 5) or (self.hand.NumberOf5Cost < 1):
                # Invalid move, punish AI, end game
                reward = -100
                done = True
            else:
                self.hand.PlayCard(5)
                self.CreaturesPlayedThisTurn[4] += 1
                self.ManaLeft -= 5
        elif action == 6:
            if (self.ManaLeft < 6) or (self.hand.NumberOf6Cost < 1):
                # Invalid move, punish AI, end game
                reward = -100
                done = True
            else:
                self.hand.PlayCard(6)
                self.CreaturesPlayedThisTurn[5] += 1
                self.ManaLeft -= 6
        else:  # action == 7
            # Begin post-Main Phase actions because AI wants to pass turn
            # Combat Phase
            self.TotalDamage += self.CreatureDamage

            # Ending Phase
            # TODO discard down to 7 cards in hand if above 7 cards in hand
            if self.Turn == self.FinalTurn:
                done = True
                reward = self.CreatureDamage
            self.Turn += 1

            # Main Phase part 1
            self.hand.PlayCard(7)
            self.LandsInPlay += 1
            # Tap all lands, add mana accordingly
            self.ManaLeft = self.LandsInPlay

            # Update total creature damage based on creatures played last turn
            for creature_type, played_creature_amt in enumerate(self.CreaturesPlayedThisTurn):
                self.CreatureDamage += played_creature_amt * (creature_type + 2)
                self.CreaturesPlayedThisTurn[creature_type] = 0

        # TODO check what state values the AI should know
        #refer to around line 22 for values for state
        
        handInfo = self.hand.GetHand()
        
        state = [self.Turn, self.ManaLeft, self.LandsInPlay, self.CreatureDamage, self.TotalDamage, \
        handInfo[0], handInfo[1], handInfo[2], handInfo[3], handInfo[4], handInfo[5], handInfo[6], \
        self.deck.NumberOf1Cost, \
        self.deck.NumberOf2Cost, \
        self.deck.NumberOf3Cost, \
        self.deck.NumberOf4Cost, \
        self.deck.NumberOf5Cost, \
        self.deck.NumberOf6Cost, \
        self.deck.NumberOfLands]
        #state = (self.CreatureDamage, self.Turn, self.hand, self.ManaLeft, self.CreaturesPlayedThisTurn, DECK_CONTENTS)
        if not done:
            reward = self.CreatureDamage
        info = state
        return state, reward, done, info

    def reset(self):
        # Reset the game for the next iteration.
        # Returns the game state information.
        self.deck.SetDeck(DECK_CONTENTS[0], DECK_CONTENTS[1], DECK_CONTENTS[2], DECK_CONTENTS[3],
                          DECK_CONTENTS[4], DECK_CONTENTS[5], DECK_CONTENTS[6])
        hand_arr = self.deck.DrawHand()
        self.hand.SetHand(hand_arr[0], hand_arr[1], hand_arr[2], hand_arr[3],
                          hand_arr[4], hand_arr[5], hand_arr[6])
        self.Turn = 1
        #attempt to play the card
        if (self.hand.PlayCard(7)):
            self.LandsInPlay = 1
        else:
            self.LandsInPlay = 0
        self.ManaLeft = self.LandsInPlay
        self.CreatureDamage = 0
        self.TotalDamage = 0
        self.CreaturesPlayedThisTurn = [0, 0, 0, 0, 0, 0]
        # TODO check what state values the AI should know, and remember to do in order
        
        handInfo = self.hand.GetHand()
        
        state = [self.Turn, self.ManaLeft, self.LandsInPlay, self.CreatureDamage, self.TotalDamage, \
        handInfo[0], handInfo[1], handInfo[2], handInfo[3], handInfo[4], handInfo[5], handInfo[6], \
        self.deck.NumberOf1Cost, \
        self.deck.NumberOf2Cost, \
        self.deck.NumberOf3Cost, \
        self.deck.NumberOf4Cost, \
        self.deck.NumberOf5Cost, \
        self.deck.NumberOf6Cost, \
        self.deck.NumberOfLands]
        reward = 0
        done = False
        info = state
        #state = (self.CreatureDamage, self.Turn, self.hand, self.ManaLeft, self.CreaturesPlayedThisTurn, DECK_CONTENTS)
        return state, reward, done, info

    def render(self, mode='human'):
        pass


class Hand:
    def __init__(self):
        self.NumberOf1Cost = 0
        self.NumberOf2Cost = 0
        self.NumberOf3Cost = 0
        self.NumberOf4Cost = 0
        self.NumberOf5Cost = 0
        self.NumberOf6Cost = 0
        self.NumberOfLands = 0

    def GetHand(self):
        return [self.NumberOf1Cost, self.NumberOf2Cost, self.NumberOf3Cost, self.NumberOf4Cost, \
                self.NumberOf5Cost, self.NumberOf6Cost, self.NumberOfLands]
        
    #    void ResetHand(){
    def ResetHand(self):
        self.NumberOf1Cost = 0
        self.NumberOf2Cost = 0
        self.NumberOf3Cost = 0
        self.NumberOf4Cost = 0
        self.NumberOf5Cost = 0
        self.NumberOf6Cost = 0
        self.NumberOfLands = 0

    def SetHand(self, Nr1Cost, Nr2Cost, Nr3Cost, Nr4Cost, Nr5Cost, Nr6Cost, NrLands):
        self.NumberOf1Cost = Nr1Cost
        self.NumberOf2Cost = Nr2Cost
        self.NumberOf3Cost = Nr3Cost
        self.NumberOf4Cost = Nr4Cost
        self.NumberOf5Cost = Nr5Cost
        self.NumberOf6Cost = Nr6Cost
        self.NumberOfLands = NrLands

    def PlayCard(self, card_type):
        if (card_type == 1):
            if (self.NumberOf1Cost > 0):
                self.NumberOf1Cost -= 1
                return True
        elif (card_type == 2):
            if (self.NumberOf2Cost > 0):
                self.NumberOf2Cost -= 1
                return True
        elif (card_type == 3):
            if (self.NumberOf3Cost > 0):
                self.NumberOf3Cost -= 1
                return True
        elif (card_type == 4):
            if (self.NumberOf4Cost > 0):
                self.NumberOf4Cost -= 1
                return True
        elif (card_type == 5):
            if (self.NumberOf5Cost > 0):
                self.NumberOf5Cost -= 1
                return True
        elif (card_type == 6):
            if (self.NumberOf6Cost > 0):
                self.NumberOf6Cost -= 1
                return True
        elif (card_type == 7):
            if (self.NumberOfLands > 0):
                self.NumberOfLands -= 1
                return True
        else:
            return False

    def AddDrawnCard(self, card_type):
        if card_type == 1:
            self.NumberOf1Cost += 1
        elif card_type == 2:
            self.NumberOf2Cost += 1
        elif card_type == 3:
            self.NumberOf3Cost += 1
        elif card_type == 4:
            self.NumberOf4Cost += 1
        elif card_type == 5:
            self.NumberOf5Cost += 1
        elif card_type == 6:
            self.NumberOf6Cost += 1
        elif card_type == 7:
            self.NumberOfLands += 1


class Deck:
    def __init__(self):
        self.NumberOf1Cost = 0
        self.NumberOf2Cost = 0
        self.NumberOf3Cost = 0
        self.NumberOf4Cost = 0
        self.NumberOf5Cost = 0
        self.NumberOf6Cost = 0
        self.NumberOfLands = 0

    def SetDeck(self, number_1_cost, number_2_cost, number_3_cost,
                number_4_cost, number_5_cost, number_6_cost,
                number_of_lands):
        self.NumberOf1Cost = number_1_cost
        self.NumberOf2Cost = number_2_cost
        self.NumberOf3Cost = number_3_cost
        self.NumberOf4Cost = number_4_cost
        self.NumberOf5Cost = number_5_cost
        self.NumberOf6Cost = number_6_cost
        self.NumberOfLands = number_of_lands

    def NrOfCards(self):
        value = self.NumberOf1Cost + \
                self.NumberOf2Cost + \
                self.NumberOf3Cost + \
                self.NumberOf4Cost + \
                self.NumberOf5Cost + \
                self.NumberOf6Cost + \
                self.NumberOfLands
        return value

    def DrawCard(self):
        RandomIntegerBetweenOneAndDeckSize = random.randint(1, self.NrOfCards())
        CardType = 0
        OneCostCutoff = self.NumberOf1Cost
        TwoCostCutoff = OneCostCutoff + self.NumberOf2Cost
        ThreeCostCutoff = TwoCostCutoff + self.NumberOf3Cost
        FourCostCutoff = ThreeCostCutoff + self.NumberOf4Cost
        FiveCostCutoff = FourCostCutoff + self.NumberOf5Cost
        SixCostCutoff = FiveCostCutoff + self.NumberOf6Cost
        LandCutoff = SixCostCutoff + self.NumberOfLands

        if (RandomIntegerBetweenOneAndDeckSize <= OneCostCutoff):
            CardType = 1
            self.NumberOf1Cost -= 1
        if (OneCostCutoff < RandomIntegerBetweenOneAndDeckSize <= TwoCostCutoff):
            CardType = 2
            self.NumberOf2Cost -= 1
        if (TwoCostCutoff < RandomIntegerBetweenOneAndDeckSize <= ThreeCostCutoff):
            CardType = 3
            self.NumberOf3Cost -= 1
        if (ThreeCostCutoff < RandomIntegerBetweenOneAndDeckSize <= FourCostCutoff):
            CardType = 4
            self.NumberOf4Cost -= 1
        if (FourCostCutoff < RandomIntegerBetweenOneAndDeckSize <= FiveCostCutoff):
            CardType = 5
            self.NumberOf5Cost -= 1
        if (FiveCostCutoff < RandomIntegerBetweenOneAndDeckSize <= SixCostCutoff):
            CardType = 6
            self.NumberOf6Cost -= 1
        if (SixCostCutoff < RandomIntegerBetweenOneAndDeckSize <= LandCutoff):
            CardType = 7  # this has been changed to 7 so that other methods work with it
            self.NumberOfLands -= 1
        return CardType

    def DrawHand(self):
        card_arr = [0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 8):
            card_arr[self.DrawCard() - 1] += 1
        return card_arr
        
#Main function
#Create the ai layers
#apparently softmax is a good option for multiple inputs
#to get the actual output from the AI
#output = np.argmax(A2.T[index])
#which outputs the highest probability number.
#Q learning is different though
#examples are directly from website at https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/
#We should implement the keras one, but I have included others, in order to understand what's going on.

#With keras model it is

model = keras.Sequential()
model.add(layers.Input(shape=(1, 19))) #input shape should be changed to 1, 19
model.add(layers.Dense(100, activation='sigmoid'))
model.add(layers.Dense(50, activation='sigmoid'))
model.add(layers.Dense(20, activation='sigmoid'))
model.add(layers.Dense(5, activation='linear'))           #output shape should be changed to 7
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

env = MTGEnv()
num_episodes = 10000

# now execute the q learning
y = 0.95
eps = 0.5
decay_factor = 0.999
r_avg_list = []
for i in range(num_episodes):
    s = env.reset()
    eps *= decay_factor
    if i % 100 == 0:
        print("Episode {} of {}".format(i + 1, num_episodes))
    done = False
    r_sum = 0
    while not done:
        if np.random.random() < eps:
            a = np.random.randint(0, 7)
        else:
            a = np.argmax(model.predict([s:s + 1]))
        new_s, r, done, _ = env.step(a)
        target = r + y * np.max([new_s:new_s + 1]))
        target_vec = model.predict([s:s + 1])[0]
        target_vec[a] = target
        model.fit(np.identity(5)[s:s + 1], target_vec.reshape(-1, 7), epochs=1, verbose=0)
        s = new_s
        r_sum += r
    r_avg_list.append(r_sum / 1000)

#Training

#not sure if it is
#env = gym.make(MTGEnv)
#env = gyme.make('MTGEnv')
#or
#env = MTGEnv()
#for _ in range(1000):
    #env.render()
#    observation = env.reset()
#    print(observation)
#    print(output)
#    env.step(env.action_space.sample())#the env.action_space.sample() should be replaced with the np.argmax when predicting I believe
#    env.close()
    
#prediction

#for _ in range(1000):
    #env.render()
#    observation = env.reset()
#    print(observation)
#    print(output)
#    env.step(np.argmax(...))#the env.action_space.sample() should be replaced with the np.argmax when predicting I believe
#    env.close()