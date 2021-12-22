# -*- coding: utf-8 -*-
"""
Description:
    This script applies the adapted Balovnev model by Dickson et al. (2016) 
    to the RASSOR excavator to analyse the scaling of energy cost with 
    the excavation of lunar regolith.

@author: Michael Wilson and DL
"""
import numpy as np
import math
from scipy.optimize import curve_fit

#define constants
eb = 0.001588                   #thickness of blunt edge (m)
w = 0.1008                      #width of bucket drum (m)
phi = math.radians(45)          #internal friction angle of BP-1 (rad)
beta = math.radians(5)          #bucket rake angle (rad)
alpha_b = math.radians(90)      #blunt edge angle (rad)
g = 1.622                       #lunar gravity (m/s^2)
c = 2000                       #max BP-1 cohesion coefficient (Pa)
s = 0.0032                      #thickness of scoop side walls (m)
delta = math.radians(5)         #external friction angle of GRC-3 (rad)
R = 0.14                        #radius of the bucket drum (m)
d = 0.01                        #depth of the bucket drum (m)

#calculate distance of blade edge from the drum centre (m)
r = ((R*(3.125*(1-np.cos(math.radians(62)))))+5.3125)/5.3125

r_scoop = (3.125*R)/5.3125      #scoop curvature radius (m)
#straight-line scoop length (m)
l_scoop = r_scoop*np.sin(math.radians(62))  

#arc of bucket drum below regolith surface (rad)
#NOT USED IN CALCULATIONS
theta_bucket = np.arccos((R-d)/R) 

#volume of regolith displaced by drum (m^3)
#NOT USED IN CALCULATIONS
V_drum = ((np.pi*w*(R**2)*theta_bucket)/(2*np.pi)) - (0.5*w*(R**2)
                        *np.sin(theta_bucket)*np.cos(theta_bucket))

#volume of scoop (m^3)
V_scoop = ((62*np.pi*w*(r_scoop**2))/(360))-(0.5*w*(r_scoop**2)
                *np.sin(math.radians(62))*np.cos(math.radians(62)))

#arc excavated by scoop (rad)
#NOT USED IN CALCULATIONS
theta_exc = np.arccos((r-d)/r)

#volume of regolith displaced by excavation (m^3)
#NOT USED IN CALCULATIONS
V_exc = ((np.pi*w*(r**2)*theta_exc)/(2*np.pi)) - (0.5*w*(r**2)
                        *np.sin(theta_exc)*np.cos(theta_exc))

#volume of regolith prism above surface (m^3)
#NOT USED IN CALCULATIONS
V_prism = V_exc - V_scoop - V_drum

#surcharge mass (kg/m^2) - set to 0 for use of bucket drum scoop
q = 0
#q=gamma*V_prism


def line(x,m,c):
    """
    Equation of a line.
    """
    return (m*x)+c

def Cos(a):
    return np.cos(a)
def Sin(a):
    return np.sin(a)
def Tan(a):
    return np.tan(a)
def ArcTan(a):
    return np.arctan(a)
def ArcSin(a):
    return np.arcsin(a)
def ArcCos(a):
    return np.arccos(a)

def csc(x):
    """
    Cosecant function.
    """
    return 1/Sin(x)

def cot(x):
    """
    Cotangent function.
    """
    return 1/Tan(x)


def density_calc(depth):
    """
    This function calculates the density of lunar regolith based off the 
    depth given using the relationship given by McKay et al. (1991). 
    Previous relationship from Hayne et al. (2017) commented out but present.
    """
    #rho_d = 1800
    #rho_s = 1100 
    #H = 0.06
    
    #convert depth to units of cm for calculation, and convert back to m
    depth = depth*100
    #gammas.append(rho_d-((rho_d-rho_s)*np.exp(-depth/H)))
    gamma = ((1.92*((depth+12.2)/(depth+18)))*1000)
    
    return gamma


def geom_factors(x):
    """
    This function calculates and returns the geometric factors depending
    on the angle of a surface with respect to a reference plane as defined
    in the Balovnev excavation model from Wilkinson and DeGennaro (2007).
    """
    #calculate geometric factor for particular angle
    #initially define as 0
    A = 0
    
    #calculate A
    if x < 0.5*(ArcSin(Sin(delta)/Sin(phi))-delta):
        
        A = (1-(Sin(phi)*Cos(2*x)))/(1-Sin(phi))
        
    else:
        A = ((Cos(delta)*(Cos(delta)+np.sqrt((Sin(phi)**2)-(Sin(delta)**2)))
        )/(1-Sin(phi)))*np.exp(((2*x)-np.pi+delta+ArcSin(
            (Sin(delta)/Sin(phi))))*Tan(phi))
    
    return A


def calc_exc_force(gamma):
    """
    This function calculates the excavation force carried out by RASSOR using
    the adapted Balovnev excavation model described by Dickson et al. (2016).
    """
    
    A1 = geom_factors(beta)
    A2 = geom_factors(alpha_b)
    A3 = geom_factors(np.pi/2)
    
    
    #split equation into three parts then add together at end
    part1 = w*(d+r-R)*A1*(1+(cot(beta)*Tan(delta)))*(
        ((d*g*gamma)/2)+(c*cot(phi))+(g*q)+((d-(l_scoop*Sin(beta)))*
        g*gamma*((1-Sin(phi))/1+Sin(phi))))
    
    part2 = w*eb*A2*(1+(Tan(delta)*cot(alpha_b)))*(
        ((eb*g*gamma)/2)+(c*cot(phi))+(g*q)+(
            ((d*g*gamma*(1-Sin(phi)))/(1+Sin(phi)))))
    
    part3 = A3*(d+r-R)*((2*s)+(4*l_scoop*Tan(delta)))*(
        ((d*g*gamma)/2)+(c*cot(phi))+(g*q)+((d-(l_scoop*Sin(beta)))*
        g*gamma*((1-Sin(phi))/1+Sin(phi))))
    
    exc_force = part1+part2+part3
    return exc_force


def force_density_fitting():
    """
    This function fits a straight line to the data from the relationship 
    between the excavation forces and lunar regolith densities.
    """
    #define depths profile
    depths = np.linspace(0,2,41)  #soil depths (m)
    #calculate change in densities through regolith
    gammas = density_calc(depths)
    
    #calculate force profile for these densities
    exc_forces = calc_exc_force(gammas)
    
    #fit a straight line to the force vs density relationship to obtain
    #the parameters (slope and constant) from this relationship
    popt, pcov = curve_fit(line, gammas, exc_forces)
    return popt, pcov


def energy_analysis(user_depth, rassor_system_energy):
    """
    This function calculates and plots the data related to the density at the
    soil depth on the lunar surface defined by the user. 
    """
    #calculate density through regolith
    user_gamma = density_calc(user_depth)
    
    #calculate the excavation force required at this density
    exc_force = calc_exc_force(user_gamma) #NOT USED
    
    #use V_scoop to calculate mass
    mass = V_scoop*user_gamma
    
    #displacement = l_scoop, assuming scoop only travels through its own length
    displacement = l_scoop
    
    #calculate relationship for force vs density and find slope and constant 
    #from relationship
    popt, pcov = force_density_fitting()
    
    #define separate parameters from force-density relationship
    slope = popt[0]
    constant = popt[1]
    
    #define fixed cutting depth in metres
    cut_depth = 0.05    #NOT USED
    
    #calculate energy per mass excavated for base case
    energy_perkg = (((slope*user_gamma)+constant)*displacement)/mass
    
    #need to scale for RASSOR's system energy cost
    #first, calculate energy cost at 0 m depth
    first_density = density_calc(0)
    first_force = calc_exc_force(first_density) #NOT USED
    first_mass = V_scoop*first_density
    
    first_energy_perkg = (((slope*first_density)+constant)*displacement)/(
                            first_mass)
    
    #apply scaling
    rassor_energyperkg = rassor_system_energy*(energy_perkg/first_energy_perkg)
    
    return rassor_energyperkg
    

