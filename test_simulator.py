from simulator import *
import policies

"""
Tests for our Simulator class.
Feel free to add tests for any helper methods you create as you see fit.
"""

def test_year():
    s = Simulator()
    assert s.time == 2010
    s.advance_year()
    assert s.time == 2011

def test_advance_year():
    # Fill me in!
    sim = Simulator()
    sim.advance_year()
    #testing whether or not it will stay at 2300 or decrease by 6
    assert sim.cumulative_co2_emissions == 2300
    sim.add_country('United States', policies.Baseline(106), 10)
    sim.advance_year()
    assert sim.time == 2012
    assert sim.prior_emissions['United States'] == 106
    assert sim.cumulative_co2_emissions == 2400
    assert sim.global_surface_temp_inc == 2400 * .0005
    assert sim.country_temperatures['United States'] == 10 + (2 * 2400 * .0005)
    sim2 = Simulator()
    #test to see if the cap works on global temp increase
    sim2.add_country('United States', policies.Baseline(4000), 10)
    sim2.advance_year()
    assert sim2.global_surface_temp_inc == 3
    #test to see if things other than US and Baseline work as well as more than one country
    sim3 = Simulator()
    sim3.add_country('China', policies.TaxEmissions(10, 0.05), 8)
    sim3.add_country('United States', policies.Baseline(6.5), 10)
    sim3.advance_year()
    assert sim3.prior_emissions['United States'] == 6.5
    assert sim3.prior_emissions["China"] == 9.5
    assert sim3.cumulative_co2_emissions == 2300 + 16 - 6
    assert sim3.global_surface_temp_inc == .0005 * 2310
    assert sim3.country_temperatures['China'] == (.0005 * 2310) + 8
    assert sim3.country_temperatures['United States'] == (2 * .0005 * 2310) + 10




def test_report():
    sim = Simulator()
    sim.add_country('United States', policies.Baseline(6.5), 10)
    assert sim.report()[0]['name'] == "United States"
    assert sim.report()[0]["temperature"] == 10
    sim.add_country('China', policies.TaxEmissions(14, 0.05), 8)
    assert sim.report()[1]['name'] == "China"
    assert sim.report()[1]["temperature"] == 8
    sim.add_country('Colombia', policies.Deforestation(0.07, 50, 0.03), 24)
    assert sim.report()[2]['name'] == 'Colombia'
    assert sim.report()[2]["temperature"] == 24
    sim.add_country('Libya', policies.MatchLowest(0.06), 23)
    assert sim.report()[3]['name'] == 'Libya'
    assert sim.report()[3]["temperature"] == 23
    sim.add_country('United Kingdom', policies.Reducing(4.5, 0.5), 9)
    assert sim.report()[4]['name'] == 'United Kingdom'
    assert sim.report()[4]["temperature"] == 9
