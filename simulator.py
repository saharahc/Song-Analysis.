
class Simulator:
    def __init__(self):
        # Our simulation starts in year 2010
        self.time = 2010                     
        # Countries added so far (by name)
        self.country_names = []
        # Maps country names to their policy object
        self.country_policies = {}
        # Maps country names to their current temperature
        self.country_temperatures = {}
        # Maps country names to their initial temperature in year 0
        self.initial_country_temps = {}
    
        # Tracks the total global surface temperature increase (in Celcius) since 1850-1900
        # In 2010, the global surface temperature had increased by approx. 1 degree Celcius
        self.global_surface_temp_inc = 1
        
        # The global surface temperature increase should not go above this value
        self.max_temperature_inc = 3 
        # Tracks total CO2 emissions over time
        self.cumulative_co2_emissions = 2300 
        # Amount by which atmospheric CO2 levels decrease per year
        self.annual_co2_decrement = 6 

        ########################################
        # Simulator history, for use by policies
        # (In a real application, we might make this a separate class)
        
        # Prior emissions by country in the past year        
        self.prior_emissions = {} 
                
    def add_country(self, name, policy, average_temp):
        self.country_names.append(name)
        self.country_policies[name] = policy
        self.country_temperatures[name] = average_temp
        self.initial_country_temps[name] = average_temp
        self.prior_emissions[name] = policy.baseline

    def country_emissions(self):
        """helper function for advance year that calculates each country's emissions for the new year"""
        for country in self.country_policies:
            self.prior_emissions[country] = self.country_policies[country].emit(self.prior_emissions)


    def total_emissions(self):
        """helper function for advance year that combines previous emissions with new emsions minus what
        the atmosphere gets rid of naturally"""
        countries_combined = 0 
        for country in self.prior_emissions:
            countries_combined += self.prior_emissions[country]
        if self.cumulative_co2_emissions + countries_combined - self.annual_co2_decrement > 2300:
            self.cumulative_co2_emissions = self.cumulative_co2_emissions + countries_combined - self.annual_co2_decrement
        else: 
            self.cumulative_co2_emissions = 2300

    def new_temp_global(self):
        """helper function for advance year that finds the increase in world temperature from the baseline"""
        if .0005 * self.cumulative_co2_emissions > self.max_temperature_inc:
            self.global_surface_temp_inc = self.max_temperature_inc
        else: 
            self.global_surface_temp_inc = .0005 * self.cumulative_co2_emissions

    def new_temps(self):
        """helper function for advance year that calculates each country's new temps"""
        x = self.global_surface_temp_inc
        for country in self.country_names:
            if country == "United States" or country == "Libya" or country == "United Kingdom":
                self.country_temperatures[country] = self.initial_country_temps[country] + 2 * x
            elif country == "China":
                self.country_temperatures["China"] = self.initial_country_temps["China"] + x
            elif country == "Colombia":
                self.country_temperatures["Colombia"] = self.initial_country_temps + 1 + x

    def advance_year(self):
        """
        Advances the simulator by one year, updating all relevant information
        """
        # TODO: Fill in this method. Consider what helper functions you might use here.
        self.time += 1
        self.country_emissions()
        self.total_emissions()
        self.new_temp_global()
        self.new_temps()

    def report(self):
        # TODO: Modify this function to return a list of dictionaries, where each dictionary 
        # contains a particular country mapped to its current temperature. 
        temps = []
        for country in self.country_temperatures:
            temps.append({'name': country, "temperature": self.country_temperatures[country]})
        return temps
