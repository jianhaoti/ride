#TODO

What to add:

# Rideshare Demand Prediction Features

Here's a structured list of suggested features for rideshare demand prediction, with nesting for organization:

- [ ] **Weather Data (Location-Specific & Granular)**
  - [ ] **Temperature:**
    - [ ] `Air_Temperature` (e.g., in Celsius or Fahrenheit)
    - [ ] `Feels_Like_Temperature` (Apparent Temperature, Heat Index, Wind Chill)
    - [ ] `Temperature_Extremes_Flag` (e.g., `is_abysmally_hot`, `is_extremely_cold`, `is_freezing_temp`)
    - [ ] `Temperature_Change` (e.g., `temp_change_last_hour`, `temp_change_last_3_hours`)
  - [ ] **Precipitation:**
    - [ ] `Precipitation_Occurrence` (Binary: `is_raining`, `is_snowing`, `is_hailing`, `is_freezing_rain`)
    - [L] `Precipitation_Intensity` (e.g., `rain_rate_mm_per_hr`, `snow_rate_cm_per_hr`)
    - [ ] `Precipitation_Accumulation` (e.g., `total_rain_last_hour`, `total_snow_on_ground`)
    - [ ] `Precipitation_Duration` (e.g., `hours_since_rain_started`)
  - [ ] **Wind:**
    - [ ] `Wind_Speed` (e.g., m/s or mph)
    - [ ] `Wind_Gusts` (maximum gust speed)
  - [ ] **Visibility:**
    - [ ] `Visibility_in_meters` (low visibility indicates fog, heavy precipitation, etc.)
  - [ ] **Cloud Cover:**
    - [ ] `Cloud_Cover_Percentage`
  - [ ] **Atmospheric Pressure:**
    - [ ] `Sea_Level_Pressure` (hPa or mbar)
- [ ] **Temporal Features**
  - [x] `Hour_of_Day` (e.g., 0-23)
  - [ ] `Day_of_Week` (e.g., Monday=0, Sunday=6)
  - [ ] `Month_of_Year`
  - [ ] `Day_of_Year`
  - [ ] `Is_Weekend` (Binary)
  - [ ] `Is_Holiday` (Binary, referring to official public holidays)
  - [ ] `Day_Before_Holiday` (Binary)
  - [ ] `Day_After_Holiday` (Binary)
  - [ ] `Hour_Before_Peak_Time` (Binary, e.g., hour before morning rush)
  - [ ] `Season` (e.g., Winter, Spring, Summer, Autumn)
- [ ] **Event Data**
  - [ ] `Major_Sports_Event` (Binary, e.g., Yankee/Mets game, NBA game)
  - [ ] `Major_Concert_Event` (Binary, at specific venues)
  - [ ] `Parade_Event` (Binary, e.g., Thanksgiving Day Parade, St. Patrick's Day Parade)
  - [ ] `Large_Convention_Event` (Binary, at Javits Center, etc.)
  - [ ] `School_Vacation` (Binary, particularly for NYC public school calendar)
- [ ] **Public Transit Disruptions**
  - [ ] `Subway_Delay_Flag` (Binary, for specific lines/areas or city-wide)
  - [ ] `Bus_Reroute_Flag` (Binary, for specific routes/areas)
  - [ ] `Commuter_Rail_Delay_Flag` (Binary, e.g., LIRR, Metro-North)
  - [ ] `Bridge_Tunnel_Closures_Flag` (Binary, due to weather or events)
- [ ] **Geospatial Features (for Pickup/Dropoff Zones)**
  - [ ] `Pickup_Zone_ID` (e.g., NYC Taxi Zone ID, or custom grid cell ID)
  - [ ] `Dropoff_Zone_ID`
  - [ ] `Population_Density_in_Zone`
  - [ ] `Commercial_POI_Density_in_Zone` (e.g., restaurants, bars, shops)
  - [ ] `Tourist_POI_Density_in_Zone`
  - [ ] `Proximity_to_Major_Transit_Hub` (e.g., distance to nearest subway station, major train station)
  - [ ] `Median_Income_of_Zone` (proxy for purchasing power/discretionary spending)
- [ ] **Traffic Data**
  - [ ] `Average_Traffic_Speed_in_Zone` (e.g., mph or km/h)
  - [ ] `Traffic_Congestion_Level_Index` (e.g., low, medium, high)
  - [ ] `Road_Closure_Flag` (Binary, for specific zones)
- [ ] **Lagged Features**
  - [ ] `Previous_Hour_Demand` (Demand count in the immediate previous hour for the same zone)
        [ ] `Same_Hour_Last_Day_Demand`
  - [ ] `Same_Hour_Last_Week_Demand`
  - [ ] `Moving_Average_Demand_Last_3_Hours`
  - [ ] `Previous_Hour_Weather_Conditions` (e.g., `previous_hour_is_raining`)
- [ ] **Supply-Side Features (if available)**
  - [ ] `Number_of_Active_Drivers_in_Zone`
  - [ ] `Average_Driver_Wait_Time_in_Zone`
  - [ ] `Surge_Pricing_Multiplier`
