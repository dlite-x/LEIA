
   
"""
Description:
    This script is a first order model of the energy chain required to 
    produce oxygen from lunar regolith via carbothermal reduction. 
"""

##if theres a problem with WX change your local region on windows to US /English
#Resolved problem with spyder requires python v3.6 max !!!

from Parcel import *
#import wx for GUI
import wx
from matplotlib.figure import Figure
from numpy import arange, sin, pi

import matplotlib

import matplotlib.pyplot as plt
import numpy as np
import math
from decimal import Decimal

import os
clear = lambda: os.system('cls')
import wx.lib.agw.floatspin as FS



matplotlib.use('WX')
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas

plt.rcParams["figure.figsize"] = (10,5)

show_metrics = False

#Extract_EnerCost_kWh_kg = 0.0006
#Extract_EnerCost_kWh_kg = 0.00065
Extract_EnerCost_kJ_kg = 2.34
#TransCostkWh_kg_m = 6.25/1000000
TransCostkWh_kg_m = 0.000008
Benef_EnerCost_kWh_kg = 0.001
Carbo_EnerCost_kWh_kg = 0.25
#Sabat_HeatProduced_kWh_per_molCO2 = 0.069
Sabat_HeatProduced_kWh_per_molCO2 = 0.071
#Value for EnergyCost_HeatDissipation percentate: 
#cost kWh/kWh dissipated (based on ISS calculation in excel)
EnergyCost_HeatDissipation = 0.013
#below based on efficiency parapmeter 70%
#Electro_EnerCost_kWh_per_InputH2O_mol = 770/3600
Electro_eff = 70
#Liquefy_EnerCost_kWh_per_InputO2_mol = 0.12 
Liquefy_carnot_eff = 10

class Frame(wx.Frame):
    #class Frame defines the GUI object to be created
    def __init__(self, parent, title):
        #define frame for GUI with default constructor
        wx.Frame.__init__(self, parent, title=title, size=(1600,1350))
        #define panels to be included in GUI
        self.panel1 = wx.Panel(self, size =(400,700), pos=(450,10))
        self.panel2 = wx.Panel(self, size =(600,550), pos=(890,10))
        self.panel3 = wx.Panel(self, size =(400,700), pos=(10,10))
        self.panel4 = wx.Panel(self, size =(1350,550), pos=(10,735))
       
       
        #self.AddSlider()
        self.AddButton()
        
        #create titles for panels
        wx.StaticText(self.panel1, label="Regolith attributes", pos=(80,50))
        wx.StaticText(self.panel3, label="Process Parameters", pos=(80,50))
        
        #define slider titles for the parcel attributes
        attribute_title_1 = wx.StaticText(self.panel1, label="Ilmenite (wt%)", 
                                       pos=(100,120))
        attribute_title_2 = wx.StaticText(self.panel1, label="Distance (m)", 
                                       pos=(100,220))
        attribute_title_3 = wx.StaticText(self.panel1, label="Depth (m)", 
                                       pos=(100,330))
        attribute_title_4 = wx.StaticText(self.panel1, label="Regolith mass", 
                                       pos=(100,430))
        
        
        
        ycoord = 85
        yofftset = 70
        xcoord = 150
        
        
        #define slider titles for the system parameters
        floatspin_title_C1 = wx.StaticText(self.panel3, 
                                label="Excavation (kJ/kg) ",
                                pos=(xcoord,ycoord+ yofftset *0))
        floatspin_title_C2 = wx.StaticText(self.panel3, 
                                label="Transport (kWh/kg/m)", 
                                pos=(xcoord, ycoord+ yofftset *1))
        floatspin_title_C3 = wx.StaticText(self.panel3, 
                                label="Beneficiation (kWh/kg)", 
                                pos=(xcoord,ycoord+ yofftset *2))
        floatspin_title_C4 = wx.StaticText(self.panel3, 
                                label="Carbothermal(kWh/kg) ", 
                                pos=(xcoord,ycoord+ yofftset *3))
        floatspin_title_C5 = wx.StaticText(self.panel3, 
                                label="Sabatier heat produced (kWh/mol CO2)", 
                                pos=(xcoord,ycoord+ yofftset *4))
        floatspin_title_C6 = wx.StaticText(self.panel3, 
                                label="Heat dissipation (kW/kW)", 
                                pos=(xcoord,ycoord+ yofftset *5))
        floatspin_title_C7 = wx.StaticText(self.panel3, 
                                label="Electrolyser efficiency (%)", 
                                pos=(xcoord,ycoord+ yofftset *6))
        floatspin_title_C8 = wx.StaticText(self.panel3, 
                                label="Liquefaction carnot efficiency (%)", 
                                pos=(xcoord,ycoord+ yofftset *7))
        
        #for parameters  
        xcoord = 150
        ycoord = 105
        yofftset = 70
        
        self.floatspin_c1 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *0), min_val=0, max_val=10, 
            increment=0.01, value=Extract_EnerCost_kJ_kg, 
            agwStyle=FS.FS_LEFT)
        self.floatspin_c1.SetFormat("%f")
        self.floatspin_c1.SetDigits(2)
        
        self.floatspin_c2 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *1), min_val=0, max_val=1, 
            increment=0.0000001, value=TransCostkWh_kg_m, agwStyle=FS.FS_LEFT)
        self.floatspin_c2.SetFormat("%f")
        self.floatspin_c2.SetDigits(7)
        
        self.floatspin_c3 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *2), min_val=0, max_val=1, 
            increment=0.001, value=Benef_EnerCost_kWh_kg, agwStyle=FS.FS_LEFT)
        self.floatspin_c3.SetFormat("%f")
        self.floatspin_c3.SetDigits(3)
        
        self.floatspin_c4 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *3), min_val=0, max_val=1, 
            increment=0.001, value=Carbo_EnerCost_kWh_kg, agwStyle=FS.FS_LEFT)
        self.floatspin_c4.SetFormat("%f")
        self.floatspin_c4.SetDigits(3)
        
        self.floatspin_c5 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *4), min_val=0, max_val=1, 
            increment=0.0001, value=Sabat_HeatProduced_kWh_per_molCO2, 
            agwStyle=FS.FS_LEFT)
        self.floatspin_c5.SetFormat("%f")
        self.floatspin_c5.SetDigits(4)
        
        self.floatspin_c6 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *5), min_val=0, max_val=1, 
            increment=0.0001, value=EnergyCost_HeatDissipation, 
            agwStyle=FS.FS_LEFT)
        self.floatspin_c6.SetFormat("%f")
        self.floatspin_c6.SetDigits(4)
        
        self.floatspin_c7 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *6), min_val=0, max_val=100, 
            increment=1, value=Electro_eff, 
            agwStyle=FS.FS_LEFT)
        self.floatspin_c7.SetFormat("%f")
        self.floatspin_c7.SetDigits(0)
        
        self.floatspin_c8 = FS.FloatSpin(self.panel3, -1, 
            pos=(xcoord,ycoord+ yofftset *7), min_val=0, max_val=100, 
            increment=1, value=Liquefy_carnot_eff, 
            agwStyle=FS.FS_LEFT)
        self.floatspin_c8.SetFormat("%f")
        self.floatspin_c8.SetDigits(0)
        
        
        #create floatspins for attributes
        self.attribute_c1 = FS.FloatSpin(self.panel1, -1, 
            pos=(100,150), min_val=1, max_val=100, 
            increment=1, value=1, 
            agwStyle=FS.FS_LEFT)
        self.attribute_c1.SetFormat("%f")
        self.attribute_c1.SetDigits(0)
        
        self.attribute_c2 = FS.FloatSpin(self.panel1, -1, 
            pos=(100,250), min_val=1, max_val=2000, 
            increment=1, value=1, 
            agwStyle=FS.FS_LEFT)
        self.attribute_c2.SetFormat("%f")
        self.attribute_c2.SetDigits(0)
        
        self.attribute_c3 = FS.FloatSpin(self.panel1, -1, 
            pos=(100,350), min_val=0, max_val=2, 
            increment=0.05, value=0, 
            agwStyle=FS.FS_LEFT)
        self.attribute_c3.SetFormat("%f")
        self.attribute_c3.SetDigits(2)
        
        self.attribute_c4 = FS.FloatSpin(self.panel1, -1, 
            pos=(100,450), min_val=1, max_val=10, 
            increment=1, value=1, 
            agwStyle=FS.FS_LEFT)
        self.attribute_c4.SetFormat("%f")
        self.attribute_c4.SetDigits(0)
       

    def AddButton(self):
        """
        Method defines and creates the button used to run the model
        """
        self.button = wx.Button(self.panel1, wx.ID_ANY, 'Run Model',(150, 550))
        self.button.Bind(wx.EVT_BUTTON, self.onButton)  

    def onButton(self, event):
        """
        Method defines what occurs when the button to run the model is pressed
        """
        print ("Button pressed.")
        user_ilmenite_perc=mf.attribute_c1.GetValue()
        user_distance=mf.attribute_c2.GetValue()
        user_depth = mf.attribute_c3.GetValue()
        user_regolith = mf.attribute_c4.GetValue()
        
        user_extract = mf.floatspin_c1.GetValue()
        user_transport = mf.floatspin_c2.GetValue()
        user_benef = mf.floatspin_c3.GetValue()
        user_carbo = mf.floatspin_c4.GetValue()
        user_sabat = mf.floatspin_c5.GetValue()
        user_heatdiss = mf.floatspin_c6.GetValue()
        user_electro = mf.floatspin_c7.GetValue()
        user_liquef = mf.floatspin_c8.GetValue()
        
        print(user_extract, user_transport, user_benef, user_carbo,
              user_sabat, user_heatdiss, user_electro, user_liquef)
        
        
        self.runModel(user_ilmenite_perc, user_distance, user_depth,
                      user_regolith, user_extract, user_transport, user_benef,
                      user_carbo, user_sabat, user_heatdiss, user_electro, 
                      user_liquef)

            
    def runModel(self, user_ilmenite_perc, user_distance, user_depth,
                 user_regolith, user_extract, user_transport, user_benef, 
                 user_carbo, user_sabat, user_heatdiss, user_electro, 
                 user_liquef):
        
        # USER define parcel 1 <====================================
        #ilmenite_concentration = 0.02   #kg/kg regolith
        regolith_mass = user_regolith   #kg of regolith
        #define distance (m) of center of regoltih voxel from reactor hopper
        regolith_distance = user_distance  
        regolith_depth = user_depth
        ilmenite_concentration = user_ilmenite_perc / 100

        
        parcel1 = ChemicalParcel(regolith_mass, ilmenite_concentration, 
                                 regolith_distance, regolith_depth, 
                                 user_extract, user_transport, user_benef, 
                                 user_carbo, user_sabat,
                                 user_heatdiss, user_electro, user_liquef)
       
        def printmetrics(parcel1):
       
            if (show_metrics == True):
                print("Stage: ======",parcel1.stage,"==========")
               
                if(parcel1.step < 2):
                    print("Regolith distance (m): ", 
                          parcel1.regolith_distance)
                    print("Regolith depth (m): ", parcel1.regolith_depth)
               
                print("Regolith mass (kg): ",parcel1.regolith_mass)
                print("ilmenite concentration (wt.kg/kg): ",
                      round(parcel1.ilmenite_concentration,4))
                print("ilmenite mass (kg): ",
                      round(parcel1.ilmenite_mass,2))
                print("CO2_mols: ",round(parcel1.CO2_mols,3))
                print("H2O_mols: ",round(parcel1.H2O_mols,3))
                print("O2_mols: ",round(parcel1.O2_mols,3))
                print("Cummulative Energy Consumed (kWh): ", 
                      round(parcel1.energyConsumed,4),"\n")
        
        
        parcel1.pristine()
        printmetrics(parcel1)
               
        parcel1.extraction()
        printmetrics(parcel1)
               
        parcel1.transportation()
        printmetrics(parcel1)        
            
        
        parcel1.beneficiation()
        printmetrics(parcel1) 
       
        parcel1.carbothermalreactor()
        printmetrics(parcel1)          
               
        parcel1.sabatierreactor()
        printmetrics(parcel1)        
               
        parcel1.electrolyzer()
        printmetrics(parcel1)        
               
        parcel1.liquefaction()
        printmetrics(parcel1)
           
        Energycost_kWhpermol = round(parcel1.energyConsumed/parcel1.O2_mols,2)          
        #print(Energycost_kWhpermol)
        
        Energycost_kWhperkgO2 = round(Energycost_kWhpermol/32*1000,1)
        #print(Energycost_kWhperkgO2)
       
                       
        #print(parcel1.Extract_EnerCost_total, 
        #parcel1.Transport_EnerCost_total,  parcel1.Benef_EnerCost_total,  
        #parcel1.Carbo_EnerCost_total, parcel1.Sabat_EnerCost_total, 
        #parcel1.Electro_EnerCost_total,parcel1.Liquefy_EnerCost_total)
        
       
        sys_energies=[parcel1.Extract_EnerCost_total, 
                      parcel1.Transport_EnerCost_total,  
                      parcel1.Benef_EnerCost_total,  
                      parcel1.Carbo_EnerCost_total, 
                      parcel1.Sabat_EnerCost_total, 
                      parcel1.Electro_EnerCost_total,
                      parcel1.Liquefy_EnerCost_total]
        
        
        
        
        #print('Total energy consumed:',parcel1.energyConsumed)
        #print(sys_energies)
        energy_percents = []
        for energy in sys_energies:
            energy_percents.append((energy/parcel1.energyConsumed)*100)
        
       
        #print("Percent totals:",sum(energy_percents))

        fig1, ax1 = plt.subplots()
        
        fig1.subplots_adjust(bottom=0.5)
        bars = ('Ex', 'T', 'B', 'C', 'S', 'El', 'L')
        x_pos = np.arange(len(bars))
       
        
        ax2 = ax1.twinx()
        # Create bars with different colors
        ax1.bar(x_pos, sys_energies, color=['black', 'red', 'green', 'blue', 
                                      'cyan','purple', 'pink'])
       
        ax2.bar(x_pos, energy_percents, color=['black', 'red', 'green', 'blue', 
                                      'cyan','purple', 'pink'])
        # Create names on the x-axiss
        plt.xticks(x_pos, bars)
       
        plt.title("Distribution of energy consumption across super-system")
        #plt.ylabel("process energy use %")
        ax1.set_ylabel("Energy consumption (kWh)")
        ax2.set_ylabel("Process Energy Use %")
        plt.xlabel("Process Steps")
        plt.grid(True)
        #plt.xticks(fontsize=20)
        #plt.yticks(fontsize=20)
        ax1.set_yscale('log')
        ax2.set_yscale('log')
        
        #plt.rcParams["figure.figsize"] = (30,30)
        # Show graph
        #round some energies to 4 decimal places
        
        fig1.text(0.1,0.34,'INPUT:')
        fig1.text(0.1,0.30,'Regolith Mass: '+
                   "{:.2f}".format(regolith_mass)+' kg')
        fig1.text(0.1,0.26,'Ilmenite Concentration: '+
                  str(user_ilmenite_perc)+' %')
        fig1.text(0.1,0.22,'Distance: '+
                  "{:.0f}".format(user_distance)+' m')
        fig1.text(0.1,0.18,'Depth: '+
                  "{:.2f}".format(user_depth)+' m')
        fig1.text(0.1,0.14,'OUTPUT:')
        fig1.text(0.1,0.10,'Mass of O2 produced: '+ 
                  "{:.4E}".format(parcel1.O2_mols*(32))+ 'g')
        
        fig1.text(0.3,0.34,'|')
        fig1.text(0.3,0.30,'|')
        fig1.text(0.3,0.26,'|')
        fig1.text(0.3,0.22,'|')
        fig1.text(0.3,0.18,'|')
        fig1.text(0.3,0.14,'|')
        fig1.text(0.3,0.10,'|')
        fig1.text(0.3,0.06,'|')
        fig1.text(0.3,0.02,'|')
        
        print(parcel1.O2_mols/32000)
        
        fig1.text(0.35,0.34,'Total energy cost: '+
                  "{:.4f}".format(parcel1.energyConsumed)+' kWh')
        fig1.text(0.35,0.30,'Energy cost per kg of O2: '+
                  "{:.2f}".format(Energycost_kWhperkgO2)+' kWh')
        
        fig1.text(0.65,0.34,'|')
        fig1.text(0.65,0.30,'|')
        fig1.text(0.65,0.26,'|')
        fig1.text(0.65,0.22,'|')
        fig1.text(0.65,0.18,'|')
        fig1.text(0.65,0.14,'|')
        fig1.text(0.65,0.10,'|')
        fig1.text(0.65,0.06,'|')
        fig1.text(0.65,0.02,'|')
        
        fig1.text(0.7,0.34,'Extraction energy cost: '+
                  str(parcel1.Extract_EnerCost_total)+' kWh')
        fig1.text(0.7,0.30,'Transport energy cost: '+
                   "{:.2E}".format(parcel1.Transport_EnerCost_total)+' kWh')
        fig1.text(0.7,0.26,'Beneficiation energy cost: '+
                  str(parcel1.Benef_EnerCost_total)+' kWh')
        fig1.text(0.7,0.22,'Carbothermal reactor energy cost: '+
                  "{:.4f}".format(parcel1.Carbo_EnerCost_total)+' kWh')
        fig1.text(0.7,0.18,'Sabatier reactor energy cost: '+
                  "{:.2E}".format(parcel1.Sabat_EnerCost_total)+' kWh')
        fig1.text(0.7,0.14,'Electrolyser energy cost: '+
                  "{:.4f}".format(parcel1.Electro_EnerCost_total)+' kWh')
        fig1.text(0.7,0.10,'Liquefaction energy cost: '+
                  "{:.4f}".format(parcel1.Liquefy_EnerCost_total)+' kWh')

        
        plt.show()
        
   
   
app = wx.App()

mf = Frame(None, title='Silder Test')
mf.Show()


mf.Show()
app.MainLoop()
