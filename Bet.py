import collections
import time
from enum import Enum


class BetArbitrationType(Enum):
    GROUP = 1  # A selected group votes on who the winner is
    MUTUAL = 2 # The betters both have to agree who won
    ARBITER = 3 # A designated third party determines who won
    ### TODO: Add "APP" method where application looks up who won - requires supported ESPN score lookup



class Bet:
    betId = None
    revisionNumber = None
    receiverId = None
    senderId = None
    winnerId = None
    amount = 0.0
    createTimestamp = None
    closeTimestamp = None
    arbitrationType = BetArbitrationType.MUTUAL
    arbiterList = []
    confirmationList = {}


    def __init__(self, receiver, sender, amount):
        self.betId = IdGenerator.newBet()
        self.revisionNumber = 0
        self.receiverId = receiver
        self.senderId = sender
        self.amount = amount
        self.createTimestamp = time.time()

    def setArbitration(self, arbitrationType, *arbiters):
        self.arbitrationType = BetArbitrationType.arbitrationType
        self.arbiterList = list(arbiters)
        for arbUserId in self.arbiterList:
            self.confirmationList[arbUserId] = None


    def arbiterConfirmWin(self, arbiterId, designatedWinner):
        self.confirmationList[arbiterId] = designatedWinner

    def determineWinner(self):
        winner = self.confirmationList.values()[0]
        if len(winner) == 0:
            print("ERROR: We ")
            return None
        for designatedWinner in self.confirmationList.values():
            if winner != designatedWinner:
                # There is no consensus on the winner!
                print("LOG: We attempted to determine a winner, but the arbiters did not agree!")
                return None
        # If we got this far, we do have an agreed upon winner!
        print("LOG: Winner for bet: " + self.betId + " is user: " + winner)
        self.winnerId = winner
        return winner


    def closeBet(self):
        self.closeTimestamp = time.time()

        if(self.winnerId == self.receiverId): # If bet receiver won
            PaymentController.deduct(self.senderId, self.amount)
            PaymentController.credit(self.receiverId, self.amount)
        elif(self.winnerId == self.senderId): #If bet sender/initiator won
            PaymentController.deduct(self.receiverId, self.amount)
            PaymentController.credit(self.senderId, self.amount)
        else:
            # If we get here, there was an error with the bet and the designated winner was not one of the bet participants
            print("ERROR: Winner Id does not match bet participants!")
