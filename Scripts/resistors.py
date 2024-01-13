
#===============================================================================================================================

# Daniel Puratich
# Fall 2023
# Generating Common Resistor Values (with the proper exceptions)

# Script is designed to be useful, efficiency is not a priority ... 

#===============================================================================================================================

# Constants that affect function behavior
# Remove excess options to avoid receiving resistor values you do not want to consider

E_SERIES = [3, 6, 12, 24, 48, 96, 192] # E-series to be evaluated (note exceptions will be applied accordingly)
DECADE_LIMIT = 6 # Maximum resistor value returned will be 10**DECADE_LIMIT+1
# Minimum resistor returned is 1 ohm, all resistors below 1 ohm tend to differ from E-series specification

#===============================================================================================================================

# Constants for series values for reference
# https://en.wikipedia.org/wiki/E_series_of_preferred_numbers 

E3 = [1.0, 2.2, 4.7]
E6 = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
E48 = [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53]
E96 = [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76]
E192 = [1.00, 1.01, 1.02, 1.04, 1.05, 1.06, 1.07, 1.09, 1.10, 1.11, 1.13, 1.14, 1.15, 1.17, 1.18, 1.20, 1.21, 1.23, 1.24, 1.26, 1.27, 1.29, 1.30, 1.32, 1.33, 1.35, 1.37, 1.38, 1.40, 1.42, 1.43, 1.45, 1.47, 1.49, 1.50, 1.52, 1.54, 1.56, 1.58, 1.60, 1.62, 1.64, 1.65, 1.67, 1.69, 1.72, 1.74, 1.76, 1.78, 1.80, 1.82, 1.84, 1.87, 1.89, 1.91, 1.93, 1.96, 1.98, 2.00, 2.03, 2.05, 2.08, 2.10, 2.13, 2.15, 2.18, 2.21, 2.23, 2.26, 2.29, 2.32, 2.34, 2.37, 2.40, 2.43, 2.46, 2.49, 2.52, 2.55, 2.58, 2.61, 2.64, 2.67, 2.71, 2.74, 2.77, 2.80, 2.84, 2.87, 2.91, 2.94, 2.98, 3.01, 3.05, 3.09, 3.12, 3.16, 3.20, 3.24, 3.28, 3.32, 3.36, 3.40, 3.44, 3.48, 3.52, 3.57, 3.61, 3.65, 3.70, 3.74, 3.79, 3.83, 3.88, 3.92, 3.97, 4.02, 4.07, 4.12, 4.17, 4.22, 4.27, 4.32, 4.37, 4.42, 4.48, 4.53, 4.59, 4.64, 4.70, 4.75, 4.81, 4.87, 4.93, 4.99, 5.05, 5.11, 5.17, 5.23, 5.30, 5.36, 5.42, 5.49, 5.56, 5.62, 5.69, 5.76, 5.83, 5.90, 5.97, 6.04, 6.12, 6.19, 6.26, 6.34, 6.42, 6.49, 6.57, 6.65, 6.73, 6.81, 6.90, 6.98, 7.06, 7.15, 7.23, 7.32, 7.41, 7.50, 7.59, 7.68, 7.77, 7.87, 7.96, 8.06, 8.16, 8.25, 8.35, 8.45, 8.56, 8.66, 8.76, 8.87, 8.98, 9.09, 9.20, 9.31, 9.42, 9.53, 9.65, 9.76, 9.88]
E_VALUES = [E3, E6, E12, E24, E48, E96, E192]

#===============================================================================================================================

def get_resistors(e_series=E_SERIES, decade_limit=DECADE_LIMIT) :
    for series in e_series :
        assert series in E_SERIES 
    assert decade_limit <= DECADE_LIMIT
    assert decade_limit >= 0
    resistors = []
    for tolerance_series in e_series :
        for decade_exponent in range(decade_limit+1) :
            multiplier_component = (10**decade_exponent)
            for i in range(0,tolerance_series) :
                series_component = 10**(i/tolerance_series)
                if tolerance_series < 36 : # set the rounding different based on series threshold
                    series_component = round(series_component, 1)
                else :
                    series_component = round(series_component, 2)
                if tolerance_series in [3, 6, 12, 24] : # manual exceptions to the E-series are required as per the spec for better alignment between each series
                    if series_component in [2.6, 2.9, 3.2, 3.5, 3.8, 4.2, 4.6] :
                        series_component += 0.1
                    elif series_component == 8.3 :
                        series_component -= 0.1
                elif tolerance_series == 192 :
                    if series_component == 9.19 :
                        series_component += 0.01
                resistor = round(multiplier_component*series_component,3) # round here because python has oddities with floating point
                if resistor not in resistors : # no duplicates (duplicates occur because of series overlap)
                    resistors.append(resistor)
    return resistors

def validate() :
    # compare what my non-hardcoded calculation spits out versus what I copy pasted from wikipedia to ensure correctness
    for i, series in enumerate(E_SERIES) :
        resistors = get_resistors([series], 0)
        try :
            assert resistors == E_VALUES[i] # must generate the correct values for zero decade limit
        except AssertionError :
            print(f"resistors.py illegal output for E{series}") # help give some diagonstics as to what failed
            for j in range(0,len(resistors)) :
                if resistors[j] != E_VALUES[i][j] :
                    print(f"resistors.py illegal output for E{series} at index {j}, correct is {E_VALUES[i][j]}, given is {resistors[j]}") # this may error due to array's potentially (ideally if code is corr) being different cases, but it's just here to help me debug
            raise AssertionError # still raise the error to stop testing
        assert len(resistors) == series # must generate the correct amount of resistors
        for j in range(DECADE_LIMIT) :
            assert len(get_resistors([series], j)) == len(E_VALUES[i])*(j+1) # must generate correct quantities for each decade limit
        print(f"resistors.py legal output for {series}")
    print("resistors.py passed testing")

if __name__ == "__main__" :
    validate() # Unit test the code! 
    # pass 

#===============================================================================================================================
