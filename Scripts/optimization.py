
# Daniel Puratich
# Fall 2023
# Optimizing resistor divider selection for https://uwarg-docs.atlassian.net/wiki/spaces/EL/pages/2357822038/Houston+Power+Testing 

# Script is designed to be useful, efficiency is not a priority ... 

from resistors import get_resistors # function to generate resistors nicely 

k = 10**3 

vrefnom = 0.75 #from ic datasheet (LMR16030)
vrefmin = 0.735
vrefmax = 0.765

voutabsmax = 5.25 #rpi max input voltage - https://raspberrypi.stackexchange.com/questions/94043/what-is-the-max-voltage-that-the-raspberry-pi-can-handle-over-the-usb-plug#:~:text=The%20voltage%20requirement%20for%20all,which%20is%20the%20USB%20standard.&text=As%20noted%20by%20a%20Raspberry,USB%20devices%20connected%20to%20it. 

rbotmin = 10*k #from ic datasheet
rbotmax = 100*k
rsummax = 500*k # determined for noise immunity
# normally we'd use a common resistor value here, but for this specific case (see confluence), deviation is ~required

for tolerance_series in [96, 192] : # evlaute tolerance series, E96 should be used generally
    resistors = get_resistors([tolerance_series], 6) 
    for tolerance in [0.01, 0.005, 0.001] : # considering 1%, 0.5%, and 0.1% resistors
        best_voutnom = 0
        best_voutmax = 0
        best_voutmin = 0
        best_rtop = 0
        best_rbot = 0
        best_tol = 0
        for rbot in resistors :
            if (rbot >= rbotmin) and (rbot <= rbotmax) : # must be within manufacturer guidelines
                rbot_tolmax = rbot*(tolerance+1.0)
                rbot_tolmin = rbot*(1.0-tolerance)
                for rtop in resistors :
                    rsum = rtop+rbot
                    if (rsum<rsummax) : 
                        rtop_tolmax = rtop*(tolerance+1.0)
                        rtop_tolmin = rtop*(1.0-tolerance)
                        voutnom = (vrefnom*(rtop+rbot))/rbot # basic resistor divider formula
                        # choice of rbot min or max is chosen on solution to optimization problem
                        # this is because a/x where a is const and x is positive is always decreasing as x increases 
                        voutmax = (vrefmax*(rtop_tolmax+rbot_tolmin))/rbot_tolmin 
                        voutmin = (vrefmin*(rtop_tolmin+rbot_tolmax))/rbot_tolmax
                        if voutmax < voutabsmax and voutnom > best_voutnom : 
                            # Must be below absolute maximum chosen because cannot ever exceed RPi's rating no matter what
                            # highest nominal chosen as best criteria because that'll be the common optimization
                            best_voutnom = voutnom
                            best_voutmax = voutmax
                            best_voutmin = voutmin
                            best_rtop = rtop
                            best_rbot = rbot
                            best_tol = tolerance
        print(f"Soln: max {round(best_voutmax,5)}v with nom {round(best_voutnom,3)}v and min {round(best_voutmin,3)}v with rtop {int(best_rtop)} & rbot {int(best_rbot)} so total {int(best_rbot+best_rtop)} at tolerance {best_tol*100}% with E{tolerance_series}")

"""
Script Output: 

Soln: max 5.24997v with nom 5.06v and min 4.875v with rtop 127000 & rbot 22100 so total 149100 at tolerance 1.0% with E96
Soln: max 5.23555v with nom 5.089v and min 4.945v with rtop 162000 & rbot 28000 so total 190000 at tolerance 0.5% with E96
Soln: max 5.19993v with nom 5.089v and min 4.979v with rtop 162000 & rbot 28000 so total 190000 at tolerance 0.1% with E96
Soln: max 5.24997v with nom 5.06v and min 4.875v with rtop 127000 & rbot 22100 so total 149100 at tolerance 1.0% with E192
Soln: max 5.24308v with nom 5.097v and min 4.952v with rtop 102000 & rbot 17600 so total 119600 at tolerance 0.5% with E192
Soln: max 5.24957v with nom 5.138v and min 5.027v with rtop 62600 & rbot 10700 so total 73300 at tolerance 0.1% with E192
"""
