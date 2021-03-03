from com.company.model.entity import Bet
from com.company.model.service import DBConnector


class BetConnector:

    def __init__(self):
        # Should be dependencyInjected
        dbConnector = DBConnector()

    def placeBet(self, betCreator, betRecipient, amount):
        bet = Bet()
        bet.senderId = betCreator
        bet.receiver = betRecipient
        bet.amount = amount

        self.dbConnector.persist(bet)

    def payOutBet(self, betId):
        foundBet = self.dbConnector.findbet(betId)
        selectedWinner = foundBet.determineWinner()
        if(selectedWinner != None):
            foundBet.closeBet()

    def updateArbiterDecision(self,betId,arbiterId,selectedWinnerId):
        foundBet = self.dbConnector.findbet(betId)
        foundBet.arbiterConfirmWin(arbiterId, selectedWinnerId)
        self.dbConnector.persist(foundBet)
