# Holds data for card request
class CardRequest:
  guid = ''
  ref = ''
  amount = ''
  cardNbr = ''
  cardExpMth = ''
  cardExpYear = ''
  zipCode = ''
  firstName = ''
  lastName = ''
  email = ''

  def toString(self):
    return 'ref=' + str(self.ref) + \
      ',amount=' + str(self.amount) + \
      ',firstName=' + str(self.firstName) + \
      ',lastName=' + str(self.lastName) + \
      ',email=' + str(self.email) + \
      ',cardNbr=XXXX' + str(self.cardNbr)[12:]