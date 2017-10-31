import random, math

class Spin:

  def __init__(self, x, y):
    self.spin = 1
    self.x = x
    self.y = y
    # top, right, bottom, left
    self.neighborSpins = [None, None, None, None]

  def __get_spin(self):
    return self.spin

  def __set_spin(self, spin):
    self.spin = spin

  spin = property(__get_spin, __set_spin, doc="""Gets or sets the spin variable (+1 or -1).""")

  def flip(self):
    self.spin *= -1

  def setNeighborSpins(self, topSpin, rightSpin, bottomSpin, leftSpin):
    self.neighborSpins[0] = topSpin
    self.neighborSpins[1] = rightSpin
    self.neighborSpins[2] = bottomSpin
    self.neighborSpins[3] = leftSpin

  def calcDiffFlipEnergy(self):
    result = 0
    for s in self.neighborSpins :
      result += s.spin * self.spin * -1
    return result * 2

  def getLocalEnergy(self):
    result = 0
    for s in self.neighborSpins :
      result += s.spin * self.spin
    return result


class TwoDimIsingConf:

  def __init__(self, beta, L):

    self.beta = beta
    self.L = L
    self.E = 0
    self.conf = [[Spin(x, y) for y in range(self.L)] for x in range(self.L)]

    self.setSpinReferences()
    self.setTotalEnergy()

  def __get_beta(self):
    return self.beta

  def __set_beta(self, beta):
    self.beta = beta

  beta = property(__get_beta, __set_beta, doc="""Gets or sets the inverse temperature.""")

  def __get_L(self):
    return self.L

  def __set_L(self, L):
    self.L = L

  L = property(__get_L, __set_L, doc="""Gets or sets the length of one side of configuration""")

  def __get_E(self):
    return self.E

  def __set_E(self, E):
    self.E = E

  E = property(__get_E, __set_E, doc="""Gets or sets total energy of configuration""")

  def setSpinReferences(self):
    round = lambda l : l if l<self.L else 0
    for x in range(0, self.L):
      for y in range(0, self.L):
        # top -> right -> bottom -> left
        dx = [x, round(x+1), x, x-1]
        dy = [round(y+1), y, y-1, y]
        self.conf[x][y].setNeighborSpins(
            self.conf[dx[0]][dy[0]],
            self.conf[dx[1]][dy[1]],
            self.conf[dx[2]][dy[2]],
            self.conf[dx[3]][dy[3]]
        )

  def setTotalEnergy(self):
    result = 0.0
    for x in range(0, self.L):
      for y in range(0, self.L):
        result += self.conf[x][y].getLocalEnergy()
    self.E = result/2.0

  def setNewConf(self):
    x = random.randint(0, self.L-1)
    y = random.randint(0, self.L-1)

    dene = self.conf[x][y].calcDiffFlipEnergy()
    if dene <= 0 or math.exp(-dene*self.beta) > random.uniform(0, 1) :
      self.conf[x][y].flip()
      self.E = self.E + dene

  def dumpSpinsAsArray(self):
    result = [0] * (self.L*self.L)
    for x in range(0, self.L):
      for y in range(0, self.L):
        result[y+x*self.L] = self.conf[x][y].spin
    return result


  def dispSpinConf(self):
    for x in range(0, self.L):
      for y in range(0, self.L):
        if self.conf[x][y].spin is 1 :
          print "x",
        else :
          print "o",
      print


if __name__ == '__main__':

  L = 10

  conf = TwoDimIsingConf(1, L)
  for c in  conf.conf[0][0].neighborSpins :
    print c, conf.conf[c.x][c.y]

  print " initial configuration "
  conf.dispSpinConf()
  print

  for beta in [x / 100.0 for x in range(10, 110)]:
    conf.beta = beta

    # equilibrate
    for i in range(0, L*L*100):
      conf.setNewConf()

    ave_E = 0.0
    var_E = 0.0
    # sample
    for i in range(0, L*L*100):
      conf.setNewConf()
      ave_E += conf.E
      var_E += conf.E ** 2.0

    var_E /= float(L*L*100) * float(L*L) ** 2.0
    ave_E /= float(L*L*100) * float(L*L)
    var_E -= ave_E**2.0
    print beta, ave_E, var_E

  print
  print " final configuration after 10000 steps"
  conf.dispSpinConf()
  print
