# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 23:43:17 2021

@author: dleger
"""


import matplotlib.pyplot as plt
import numpy as np

#matplotlib qt

plt.rcParams["figure.figsize"] = (10,5)

show_metrics = False

   
class ChemicalParcel:    
   
    #global variables
    EnergyCost_HeatDissipation = 0.013   #percentate: cost kWh/kWh dissipated (based on ISS calculation in excel)
    TransCostkWh_per_m = 6.25/1000000  #placeholder value
    beneficiation_pass =0
     
    def __init__(self, regolith_mass, ilmenite_concentration, regolith_distance, regolith_depth):
       
        self.stage = "Pre-extracted"
        self.step = 0
        self.regolith_mass = regolith_mass
        self.ilmenite_concentration = ilmenite_concentration
        self.regolith_distance = regolith_distance
        self.regolith_depth = regolith_depth
        self.ilmenite_mass = self.ilmenite_concentration * self.regolith_mass
        self.otherminerals_mass = self.regolith_mass *(1-self.ilmenite_concentration)
        self.energyConsumed = 0
        self.CO2_mols = 0
        self.H2O_mols = 0
        self.O2_mols = 0
       
        self.Extract_EnerCost_total= 0
        self.Transport_EnerCost_total = 0
        self.Benef_EnerCost_total = 0
        self.Carbo_EnerCost_total = 0
        self.Sabat_EnerCost_total = 0
        self.Electro_EnerCost_total= 0
        self.Liquefy_EnerCost_total = 0
       
       
        self.beneficiation_pass = 0
       
    def pristine(self):
        self.stage = ("in the ground regolith")
        self.step = 0
       
       
    def extraction(self):
        self.stage = "extracted"  
        self.step = 1
        #kWh/kg regolith extracted
        Extract_EnerCost_kWh_per_InputRegol_kg = 0.0006
        self.Extract_EnerCost_total = Extract_EnerCost_kWh_per_InputRegol_kg*self.regolith_mass
        self.energyConsumed = self.energyConsumed + self.Extract_EnerCost_total
       
               
    def transportation(self):
        self.stage = "transported to station"  
        self.step = 2
        #kWh/kg regolith transported
        Transport_EnerCost_kWh_per_InputRegol_kg = self.regolith_distance * self.TransCostkWh_per_m
        self.Transport_EnerCost_total = Transport_EnerCost_kWh_per_InputRegol_kg*self.regolith_mass
        self.energyConsumed = self.energyConsumed + self.Transport_EnerCost_total
       
    def beneficiation(self):
       
        self.beneficiation_pass =  self.beneficiation_pass+1
        self.stage = "beneficiated pass: "+ str(self.beneficiation_pass)
       
        self.step = 3
        #kWh/kg regolith extracted
        Benef_EnerCost_kWh_per_InputRegol_kg = 0.0000    #no energy value added yet
        Benef_EnerCost_total = Benef_EnerCost_kWh_per_InputRegol_kg*self.regolith_mass
        self.energyConsumed = self.energyConsumed + Benef_EnerCost_total
       
        #initial masses
        self.otherminerals_mass= regolith_mass*(1-self.ilmenite_concentration)
        self.ilmenite_mass =  self.regolith_mass * self.ilmenite_concentration
       
        #after beneficiation pass        +
        self.otherminerals_mass = self.otherminerals_mass * 0.44   #amount of gangue in target bins
        self.ilmenite_mass = self.ilmenite_mass * 0.75   #amount of gangue in target bins
         
       
        self.regolith_mass = self.ilmenite_mass + self.otherminerals_mass
           
        self.ilmenite_concentration = self.ilmenite_mass /self.regolith_mass
       
       
    def carbothermalreactor(self):
        self.stage = "CarboReacted"
        self.step = 4        
        #kWh/kg regolith extracted
        Carbo_EnerCost_kWh_per_InputRegol_kg = 0.25    #hardcoded based on excel calculations
        self.Carbo_EnerCost_total = Carbo_EnerCost_kWh_per_InputRegol_kg*self.regolith_mass
        self.energyConsumed = self.energyConsumed + self.Carbo_EnerCost_total  
       
        #eventually should use this to pull integral value from a file
        start_temp_kelvin = 280  #0 ceclius
        end_temp_kelvin = 1180   #900 ceclius        
           
        self.ilmenite_mass = self.ilmenite_concentration * self.regolith_mass #in kg
        self.ilmenite_mols= self.ilmenite_mass /0.157   #mols = mass (kg) / mass 0.157 kg /mols
       
        self.CO2_mols = 0.5*self.ilmenite_mols
        self.ilmenite_mols = 0
        self.regolith_mass = 0
        self.ilmenite_concentration = 0
        self.ilmenite_mass = 0
               
       
    def sabatierreactor(self):
        self.stage = "SabartierReacted"
        self.step = 5
        #kWh/kg regolith extracted
        Sabat_HeatProduced_kWh_per_molCO2 = 0.069
        Sabat_Cooling_Cost_per_molCO2 = Sabat_HeatProduced_kWh_per_molCO2 * self.EnergyCost_HeatDissipation
        Sabat_EnerCost_kWh_per_InputCO2_mol = Sabat_Cooling_Cost_per_molCO2   #pumping coolant cost based on ISS calculations
        self.Sabat_EnerCost_total = Sabat_EnerCost_kWh_per_InputCO2_mol*self.CO2_mols
        self.energyConsumed = self.energyConsumed + self.Sabat_EnerCost_total    
        self.H2O_mols = 2*self.CO2_mols
        self.CO2_mols = 0        
       
       
    def electrolyzer(self):
        self.stage = "Electrolyzed"
        self.step = 6
        #kWh/kg regolith extracted
        Electro_EnerCost_kWh_per_InputH2O_mol = 770/3600    #based on efficiency parapmeter 70%
        self.Electro_EnerCost_total = Electro_EnerCost_kWh_per_InputH2O_mol*self.H2O_mols
        self.energyConsumed = self.energyConsumed + self.Electro_EnerCost_total    
        self.O2_mols = 0.5*self.H2O_mols
        self.H2O_mols = 0
       
       
    def liquefaction(self):
        self.stage = "Liquefied_Oxygen"
        self.step = 7
        #kWh/kg regolith extracted
        Liquefy_EnerCost_kWh_per_InputO2_mol = 0.12    #TBD  placeholder value
        self.Liquefy_EnerCost_total = Liquefy_EnerCost_kWh_per_InputO2_mol*self.O2_mols
        self.energyConsumed = self.energyConsumed + self.Liquefy_EnerCost_total    
                           
       
    def printmetrics(self):
       
        if (show_metrics == True):
            print("Stage: ======",parcel1.stage,"==========")
           
            if(parcel1.step < 2):
                print("Regolith distance (m): ", parcel1.regolith_distance)
                print("Regolith depth (m): ", parcel1.regolith_depth)
           
            print("Regolith mass (kg): ",parcel1.regolith_mass)
            print("ilmenite concentration (wt.kg/kg): ",round(parcel1.ilmenite_concentration,4))
            print("ilmenite mass (kg): ",round(parcel1.ilmenite_mass,2))
            print("CO2_mols: ",round(parcel1.CO2_mols,3))
            print("H2O_mols: ",round(parcel1.H2O_mols,3))
            print("O2_mols: ",round(parcel1.O2_mols,3))
            print("Cummulative Energy Consumed (kWh): ", round(parcel1.energyConsumed,4),"\n")
     
   
   
 

#=====================================================loop
i=0
ilmenite_array =[]
Energycost_array =[]
 
 
for ilmenite_iterations in np.arange (0.01,0.50,0.01):
   
    ilmenite_array.append(ilmenite_iterations)
   
   
    # USER define parcel 1 <====================================
    ilmenite_concentration = ilmenite_iterations   #kg/kg regolith
    regolith_mass = 1   #kg of regolith
    regolith_distance = 10  #distance in meters of center of regoltih voxel from reactor hopper
    regolith_depth = 0.01  #max depth of this regolith voxel
   
    parcel1 = ChemicalParcel(regolith_mass, ilmenite_concentration, regolith_distance, regolith_depth)
   
    show_metrics = False
   
    parcel1.pristine()
    parcel1.printmetrics()
           
    parcel1.extraction()
    parcel1.printmetrics()
           
    parcel1.transportation()
    parcel1.printmetrics()        
           
    parcel1.beneficiation()
    parcel1.printmetrics()  
   
    parcel1.carbothermalreactor()
    parcel1.printmetrics()          
           
    parcel1.sabatierreactor()
    parcel1.printmetrics()        
           
    parcel1.electrolyzer()
    parcel1.printmetrics()        
           
    parcel1.liquefaction()
    parcel1.printmetrics()
       
    Energycost = round(parcel1.energyConsumed/parcel1.O2_mols,2)
    Energycost_kWh_per_kg_O2 =  Energycost /32*1000
   
    #print("ilmenite is ", round(ilmenite_concentration*100,4), "%, the OVERALL kWh / O2 mol: ", Energycost)
    Energycost_array.append(Energycost_kWh_per_kg_O2)
   
#print(ilmenite_array)
#print(Energycost_array)

fig2, ax2 = plt.subplots()
xpoints = ilmenite_array
ypoints = Energycost_array


plt.plot(xpoints, ypoints)
plt.xlabel("Ilmenite wt%")
plt.ylabel("Energy Cost O2 produced kWh/kg ")
plt.title("Energy Cost of O2 production as a function of ilmenite concentration")

plt.show()

