
# Daniel Puratich
# Fall 2023
# General Optimizing Resistor Divider for buck converter or LDO IC error amplifier feedback Calculator

# TODO: Increase efficiency by using something better than a brute force approach
# TODO: implement automatic price tradeoffs into evaluation or data output ? https://developer.digikey.com/products/product-information/partsearch/keywordsearch 
# TODO: fancier styling on the final printout 

from resistors import get_resistors # function to generate E-series resistors 

# Reference voltage of the error amplifier (generally inside an IC), from datasheet generally
VREFNOM = 0.75 
VREFMIN = VREFNOM*0.99 # should be provided in a table as either a fixed value or a tolerance percentage
VREFMAX = VREFNOM*1.01

# what you want the high side of the divider to be when the low side is at the vref (i.e. desired vout of the buck converter or LDO)
VOUTTARGET = 12.0

# limits the two resistors summed value
RSUMMIN = 50*(10**3) # lower limit on sum of rbot and rtop
RSUMMAX = 500*(10**3) # upper limit on sum of rbot and rtop
ROUNDONE = True # if you set this to true it will guarentee rtop or rbot is a multiple of 10 value

# Options when searching for solutions (remove excess options to avoid extra irrelevant solutions)
E_SERIES = [12, 24, 48, 96, 192] # E series: https://en.wikipedia.org/wiki/E_series_of_preferred_numbers 
DECADE_LIMIT = 6 # (1 to 100k) resistor decades to be considerred
TOLERANCE_PERCENTAGES = [0.01, 0.005, 0.001] # considering 1%, 0.5%, and 0.1% (if it's within your limits consider using 1% as most common)

for tolerance_series in E_SERIES: 
    resistors = get_resistors([tolerance_series], DECADE_LIMIT)
    for tolerance in TOLERANCE_PERCENTAGES : 
        best_voutnom = 0
        best_voutmax = 0
        best_voutmin = 0
        best_rtop = 0
        best_rbot = 0
        best_tol = 0
        for rbot in resistors :
            for rtop in resistors :
                rsum = rtop+rbot
                if rsum<RSUMMAX and rsum>RSUMMIN : 
                    rbot_tolmax = rbot*(tolerance+1.0)
                    rbot_tolmin = rbot*(1.0-tolerance)
                    rtop_tolmax = rtop*(tolerance+1.0)
                    rtop_tolmin = rtop*(1.0-tolerance)
                    voutnom = (VREFNOM*(rtop+rbot))/rbot # basic resistor divider formula
                    voutmax = (VREFMAX*(rtop_tolmax+rbot_tolmin))/rbot_tolmin  # choice of rbot min or max is chosen on solution to optimization problem bc a/x where a is pos const and x is pos is always decreasing as x increases 
                    voutmin = (VREFMIN*(rtop_tolmin+rbot_tolmax))/rbot_tolmax
                    if (
                        ((abs(voutnom-VOUTTARGET) < abs(best_voutnom-VOUTTARGET))) and ( # it is closer to the nominal target
                            (not ROUNDONE) or ( 
                                (rtop == 10**(len(str(int(rtop)))-1)) or 
                                (rbot == 10**(len(str(int(rbot)))-1)) # check resistors is a very common value (to save BOM line items if desired) (I know this is inefficient :d )
                            )
                        ) 
                        ) : # if closer solution to vouttarget  
                        best_voutnom = voutnom
                        best_voutmax = voutmax
                        best_voutmin = voutmin
                        best_rtop = rtop
                        best_rbot = rbot
                        best_tol = tolerance
        print(f"Soln: max {round(best_voutmax,4)}v with nom {round(best_voutnom,4)}v and min {round(best_voutmin,4)}v with rtop {int(best_rtop)} & rbot {int(best_rbot)} so total {int(best_rbot+best_rtop)} at tolerance {best_tol*100}% with E{tolerance_series}")
