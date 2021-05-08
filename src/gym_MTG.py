import gym
import random

DECK_CONTENTS = (2, 2, 2, 2, 2, 3, 4)  # TODO What needs to be in the deck? This needs to be double-checked
FINAL_TURN = 5  # TODO This also needs to be double checked


class MTGEnv(gym.Env):

    def __init__(self):
        self.action_space = gym.spaces.Discrete(7)  # Number of possible actions
        self.observation_space = gym.spaces.Discrete(6)  # Number of state information numbers that need to be provided

        self.deck = Deck()
        self.deck.SetDeck(DECK_CONTENTS[0], DECK_CONTENTS[1], DECK_CONTENTS[2], DECK_CONTENTS[3],
                          DECK_CONTENTS[4], DECK_CONTENTS[5], DECK_CONTENTS[6])
        self.hand = Hand()
        hand_arr = self.deck.DrawHand()
        self.hand.SetHand(hand_arr[0], hand_arr[1], hand_arr[2], hand_arr[3],
                          hand_arr[4], hand_arr[5], hand_arr[6])
        self.FinalTurn = FINAL_TURN
        self.Turn = 1
        self.ManaLeft = 0
        self.LandsInPlay = 0
        self.CreatureDamage = 0
        self.TotalDamage = 0
        self.CreaturesPlayedThisTurn = [0, 0, 0, 0, 0, 0]

    def step(self, action):
        # Take in the AI's action for one turn, process the results,
        # and return the game state information,
        # a reward number,
        # a value that is True if the game is over and False otherwise,
        # and some debugging information.

        # Action 0: Pass turn (then play a land if applicable).
        # Action 1-6: Play a 1-6 drop creature, do not pass turn

        done = False

        # Done before the first turn
        if (self.Turn == 1) and (self.hand.NumberOfLands > 0):
            # Play a land first thing
            self.hand.PlayCard(7)
            self.LandsInPlay += 1
            # Tap all lands, add mana accordingly
            self.ManaLeft = self.LandsInPlay

        # Actions 1-6 are done during the First Main Phase part 2
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
                reward = self.TotalDamage  # TODO verify if this should be self.CreatureDamage instead
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

        state = (self.CreatureDamage, self.Turn, self.hand, self.ManaLeft, self.CreaturesPlayedThisTurn, DECK_CONTENTS)
        if not done:
            reward = self.TotalDamage  # TODO verify if this should be self.CreatureDamage instead
        info = self.deck
        return state, reward, done, info  # TODO reward might be None here if we're not careful, double check everything

    def reset(self):
        # Reset the game for the next iteration.
        # Returns the game state information.
        self.deck.SetDeck(DECK_CONTENTS[0], DECK_CONTENTS[1], DECK_CONTENTS[2], DECK_CONTENTS[3],
                          DECK_CONTENTS[4], DECK_CONTENTS[5], DECK_CONTENTS[6])
        hand_arr = self.deck.DrawHand()
        self.hand.SetHand(hand_arr[0], hand_arr[1], hand_arr[2], hand_arr[3],
                          hand_arr[4], hand_arr[5], hand_arr[6])
        self.Turn = 1
        self.ManaLeft = 0
        self.LandsInPlay = 0
        self.CreatureDamage = 0
        self.TotalDamage = 0
        self.CreaturesPlayedThisTurn = [0, 0, 0, 0, 0, 0]
        state = (self.CreatureDamage, self.Turn, self.hand, self.ManaLeft, self.CreaturesPlayedThisTurn, DECK_CONTENTS)
        return state

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
        if card_type == 1:
            self.NumberOf1Cost -= 1
        elif card_type == 2:
            self.NumberOf2Cost -= 1
        elif card_type == 3:
            self.NumberOf3Cost -= 1
        elif card_type == 4:
            self.NumberOf4Cost -= 1
        elif card_type == 5:
            self.NumberOf5Cost -= 1
        elif card_type == 6:
            self.NumberOf6Cost -= 1
        elif card_type == 7:
            self.NumberOfLands -= 1

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

        if RandomIntegerBetweenOneAndDeckSize <= OneCostCutoff:
            CardType = 1
            self.NumberOf1Cost -= 1
        if OneCostCutoff < RandomIntegerBetweenOneAndDeckSize <= TwoCostCutoff:
            CardType = 2
            self.NumberOf2Cost -= 1
        if TwoCostCutoff < RandomIntegerBetweenOneAndDeckSize <= ThreeCostCutoff:
            CardType = 3
            self.NumberOf3Cost -= 1
        if ThreeCostCutoff < RandomIntegerBetweenOneAndDeckSize <= FourCostCutoff:
            CardType = 4
            self.NumberOf4Cost -= 1
        if FourCostCutoff < RandomIntegerBetweenOneAndDeckSize <= FiveCostCutoff:
            CardType = 5
            self.NumberOf5Cost -= 1
        if FiveCostCutoff < RandomIntegerBetweenOneAndDeckSize <= SixCostCutoff:
            CardType = 6
            self.NumberOf6Cost -= 1
        if SixCostCutoff < RandomIntegerBetweenOneAndDeckSize <= LandCutoff:
            CardType = 7  # this has been changed to 7 so that other methods work with it
            self.NumberOfLands -= 1
        return CardType

    def DrawHand(self):
        card_arr = [0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 8):
            card_arr[self.DrawCard() - 1] += 1
        return card_arr
