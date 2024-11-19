import math
import pandas as pd
import matplotlib.pyplot as plt

def calculate_radiation(date, latitude, tilt):
    
    # We set up initial parameters based on the date
    if date == "Oct 1":
        n = 274
        declination = math.radians(-3.36106)
    else:  # Nov 1
        n = 305
        declination = math.radians(-14.56895)
    
    latitude_rad = math.radians(latitude)   
    tilt_rad = math.radians(tilt)
    
    G_sc = 1367  # Solar constant in W/m²
    
    results = []
    for hour in range(24):
        hour_angle = math.radians((hour - 12) * 15)
        
        # Calculate extraterrestrial radiation
        G_0 = G_sc * (1 + 0.033 * math.cos(360 * n / 365)) * (
            math.cos(latitude_rad) * math.cos(declination) * math.cos(hour_angle) +
            math.sin(latitude_rad) * math.sin(declination)
        )
        
        # Calculate R_b
        R_b = (math.sin(declination) * math.sin(latitude_rad - tilt_rad) +
               math.cos(declination) * math.cos(latitude_rad - tilt_rad) * math.cos(hour_angle)) / (
            math.sin(declination) * math.sin(latitude_rad) +
            math.cos(declination) * math.cos(latitude_rad) * math.cos(hour_angle)
        )
        
        G_0_tilted = G_0 * R_b
        
        # Calculate clear sky radiation
        G_clear = 0.7 * G_0_tilted
        
        results.append({
            'Hour': hour,
            'G_0': max(0, G_0_tilted),
            'G_clear': max(0, G_clear)
        })
    
    return pd.DataFrame(results)

# Calculate for October 1 and November 1
oct_1 = calculate_radiation("Oct 1", 8.460555, 8.460555)
nov_1 = calculate_radiation("Nov 1", 8.460555, 8.460555)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(oct_1['Hour'], oct_1['G_0'], label='Oct 1 - Extraterrestrial')
plt.plot(oct_1['Hour'], oct_1['G_clear'], label='Oct 1 - Clear Sky')
plt.plot(nov_1['Hour'], nov_1['G_0'], label='Nov 1 - Extraterrestrial')
plt.plot(nov_1['Hour'], nov_1['G_clear'], label='Nov 1 - Clear Sky')
plt.xlabel('Hour of the Day')
plt.ylabel('Radiation (W/m²)')
plt.title('Hourly Radiation for Sierra Leone (Latitude Tilt)')
plt.legend()
plt.grid(True)
plt.show()

# Show effect of changing tilt
oct_1_20tilt = calculate_radiation("Oct 1", 8.460555, 20)
nov_1_20tilt = calculate_radiation("Nov 1", 8.460555, 20)

plt.figure(figsize=(12, 6))
plt.plot(oct_1['Hour'], oct_1['G_clear'], label='Oct 1 - Latitude Tilt')
plt.plot(oct_1_20tilt['Hour'], oct_1_20tilt['G_clear'], label='Oct 1 - 20° Tilt')
plt.plot(nov_1['Hour'], nov_1['G_clear'], label='Nov 1 - Latitude Tilt')
plt.plot(nov_1_20tilt['Hour'], nov_1_20tilt['G_clear'], label='Nov 1 - 20° Tilt')
plt.xlabel('Hour of the Day')
plt.ylabel('Clear Sky Radiation (W/m²)')
plt.title('Effect of Tilt on Clear Sky Radiation')
plt.legend()
plt.grid(True)
plt.show()