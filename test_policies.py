
from policies import *

# 'approx' is a pytest helper for working with floats. Because of
# the intricacies of float-point arithmetic in most languages,
# error can quickly become an issue, especially when multiplying.
#   (Recall why we use significant digits in science.)
# Per the docs, the default relative tolerance is 1e-6.
# Refer to this doc for details on how it works:
# https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest-approx
from pytest import approx


# ANALAND = Simulator.add_country("ANALAND", Baseline.emit, 3000)
test_dict = {}

def test_Baseline():
    b = Baseline(300)
    assert b.emit(test_dict) == 300
    b = Baseline(0)
    assert b.emit(test_dict) == 0
    b = Baseline(0.1)
    assert b.emit(test_dict) == 0.1
    
#__________________________________________________________________________________________________________________

def test_Reducing(): 
    c = Reducing(300, 100)
    assert c.emit(test_dict) ==  200
    c = Reducing(300, 200)
    assert c.emit(test_dict) ==  100
    c = Reducing(300, 400)
    assert c.emit(test_dict) ==  0

#__________________________________________________________________________________________________________________


def test_TaxEmissions():
    d = TaxEmissions(300, 1)
    assert d.emit(test_dict) == 0
    d = TaxEmissions(300, 0.03)
    assert d.emit(test_dict) == 291


#__________________________________________________________________________________________________________________

def test_Deforestation():
    e = Deforestation(300, 3, 0.03)
    assert e.emit(test_dict) == 309
    assert e.emit(test_dict) == 318.27
    assert e.emit(test_dict) == 327.8181
    assert e.emit(test_dict) == 327.8181

    
#__________________________________________________________________________________________________________________

def test_MatchLowest():
    match_lowest_dict = {'prior_emissions' : {"USA" : 300, "China" : 200, "Russia" : 100}}
    m = MatchLowest(300)
    assert m.emit(match_lowest_dict) == 100
    match1_lowest_dict = {'prior_emissions' : {}}
    m2 = MatchLowest(300)
    assert m2.emit(match1_lowest_dict) == 300