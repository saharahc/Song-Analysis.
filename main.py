from display import Display
from simulator import Simulator
import policies

if __name__ == '__main__':
    sim = Simulator()
    sim.add_country('United States', policies.Baseline(6.5), 10)
    sim.add_country('China', policies.TaxEmissions(14, 0.05), 8)
    sim.add_country('Colombia', policies.Deforestation(0.07, 50, 0.03), 24)
    sim.add_country('Libya', policies.MatchLowest(0.06), 23)
    sim.add_country('United Kingdom', policies.Reducing(4.5, 0.5), 9)    

    display = Display(sim)
    display.run()
