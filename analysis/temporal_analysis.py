import pandas as pd 
from config import analysis_config as anal
from typing import Dict, Tuple
from data import data_pipeline
from pathlib import Path

# Get days of week from config
days_of_week = anal.days_of_week

def generate_ride_density_per_hour(df: pd.DataFrame) -> pd.Series:
    df['Hour'] = df['Date/Time'].dt.hour
    df_unique_days = df['Date/Time'].dt.date.nunique()
    df_aggregate_rides = df.groupby('Hour').size().reindex(range(24), fill_value=0)
    density = pd.Series(df_aggregate_rides) / df_unique_days

    return density

def generate_ride_density_per_day(df: pd.DataFrame) -> pd.Series:
    unique_day_series = pd.Series(
        (df[df['Day Name'] == day]['Date/Time'].dt.date.nunique() for day in days_of_week), #type:ignore
        index=anal.days_of_week
    )    
    df_aggregate_rides = df.groupby('Day Name').size().reindex(anal.days_of_week, fill_value=0)
    density = df_aggregate_rides / unique_day_series

    return density

def get_per_hour_dict(df: pd.DataFrame) -> Dict[str, Tuple[pd.Series, str]]:
    ret = {}
    for day in anal.days_of_week:
        df_filtered_by_day = df[df['Day Name'] == day].copy()
        ret[day] = (generate_ride_density_per_hour(df_filtered_by_day), anal.colors[day]) #type:ignore
    
    return ret

def get_per_day_dict(df: pd.DataFrame) -> Dict[str, Tuple[pd.Series, str]]:
    df['Day Name'] = df['Date/Time'].dt.day_name()
    day_density_series = generate_ride_density_per_day(df)

    ret = {}
    for day in anal.days_of_week:
        ret[day] = (day_density_series[day], anal.colors[day])
    return ret

def get_weekday_weekend_per_hour_dict(df: pd.DataFrame) -> Dict[str, Tuple[pd.Series, str]]:
    # generate density plot of rush hour distribution
    weekday_df = df[~df['Is Weekend']].copy()
    weekend_df = df[df['Is Weekend']].copy()

    weekday_density_series = generate_ride_density_per_hour(weekday_df) # type: ignore
    weekend_density_series = generate_ride_density_per_hour(weekend_df) # type: ignore

    return {
        "Weekday" : (weekday_density_series, "blue"), 
        "Weekend": (weekend_density_series, "red")
        }

def calculate_temporal_statistics(df: pd.DataFrame) -> Dict:
    """Calculate comprehensive temporal statistics"""
    print("\n📊 Calculating Temporal Statistics...")
    
    # Basic dataset info
    total_rides = len(df)
    date_range = df['Date/Time'].dt.date
    unique_days = date_range.nunique()
    total_hours = unique_days * 24
    
    print(f"   📈 Total rides: {total_rides:,}")
    print(f"   📅 Date range: {date_range.min()} to {date_range.max()}")
    print(f"   📅 Unique days: {unique_days}")
    print(f"   ⏰ Total hours: {total_hours:,}")
    
    # Daily statistics
    daily_rides = df.groupby(date_range).size()
    avg_rides_per_day = daily_rides.mean()
    std_rides_per_day = daily_rides.std()
    max_rides_per_day = daily_rides.max()
    min_rides_per_day = daily_rides.min()
    
    print(f"\n   📊 Daily Statistics:")
    print(f"      Average rides per day: {avg_rides_per_day:.1f}")
    print(f"      Standard deviation: {std_rides_per_day:.1f}")
    print(f"      Maximum rides per day: {max_rides_per_day}")
    print(f"      Minimum rides per day: {min_rides_per_day}")
    print(f"      Coefficient of variation: {(std_rides_per_day/avg_rides_per_day)*100:.1f}%")
    
    # Hourly statistics
    df['Hour'] = df['Date/Time'].dt.hour
    hourly_rides = df.groupby('Hour').size()
    avg_rides_per_hour = hourly_rides.mean()
    peak_hour = hourly_rides.idxmax()
    peak_rides = hourly_rides.max()
    quiet_hour = hourly_rides.idxmin()
    quiet_rides = hourly_rides.min()
    
    print(f"\n   ⏰ Hourly Statistics:")
    print(f"      Average rides per hour: {avg_rides_per_hour:.1f}")
    print(f"      Peak hour: {peak_hour}:00 ({peak_rides} rides)")
    print(f"      Quietest hour: {quiet_hour}:00 ({quiet_rides} rides)")
    print(f"      Peak/Quiet ratio: {peak_rides/quiet_rides:.1f}x")
    
    # Day of week statistics
    df['Day Name'] = df['Date/Time'].dt.day_name()
    day_rides = df.groupby('Day Name').size().reindex(days_of_week, fill_value=0)
    busiest_day = day_rides.idxmax()
    busiest_day_rides = day_rides.max()
    quietest_day = day_rides.idxmin()
    quietest_day_rides = day_rides.min()
    
    print(f"\n   📅 Day of Week Statistics:")
    print(f"      Busiest day: {busiest_day} ({busiest_day_rides} rides)")
    print(f"      Quietest day: {quietest_day} ({quietest_day_rides} rides)")
    print(f"      Busiest/Quietest ratio: {busiest_day_rides/quietest_day_rides:.1f}x")
    
    # Weekend vs Weekday
    weekday_df = df[~df['Is Weekend']]
    weekend_df = df[df['Is Weekend']]
    
    weekday_avg = len(weekday_df) / weekday_df['Date/Time'].dt.date.nunique() if len(weekday_df) > 0 else 0  #type:ignore
    weekend_avg = len(weekend_df) / weekend_df['Date/Time'].dt.date.nunique() if len(weekend_df) > 0 else 0  #type:ignore
    weekend_weekday_ratio = weekend_avg / weekday_avg
    
    print(f"\n   🏠 Weekend vs Weekday:")
    print(f"      Average weekday rides: {weekday_avg:.1f}")
    print(f"      Average weekend rides: {weekend_avg:.1f}")
    print(f"      Weekend/Weekday ratio: {weekend_weekday_ratio:.2f}")
    
    # Rush hour analysis
    morning_rush = df[(df['Hour'] >= 7) & (df['Hour'] <= 9)].groupby('Day Name').size()
    evening_rush = df[(df['Hour'] >= 17) & (df['Hour'] <= 19)].groupby('Day Name').size()
    
    print(f"\n   🚗 Rush Hour Analysis:")
    print(f"      Morning rush (7-9 AM) - Busiest: {morning_rush.idxmax()} ({morning_rush.max()} rides)")
    print(f"      Evening rush (5-7 PM) - Busiest: {evening_rush.idxmax()} ({evening_rush.max()} rides)")
    
    # Seasonal patterns (if data spans multiple months)
    df['Month'] = df['Date/Time'].dt.month
    monthly_rides = df.groupby('Month').size()
    if len(monthly_rides) > 1:
        print(f"\n   🌸 Seasonal Patterns:")
        print(f"      Busiest month: {monthly_rides.idxmax()} ({monthly_rides.max()} rides)")
        print(f"      Quietest month: {monthly_rides.idxmin()} ({monthly_rides.min()} rides)")
    
    # Return comprehensive statistics
    stats = {
        'total_rides': total_rides,
        'unique_days': unique_days,
        'avg_rides_per_day': avg_rides_per_day,
        'std_rides_per_day': std_rides_per_day,
        'max_rides_per_day': max_rides_per_day,
        'min_rides_per_day': min_rides_per_day,
        'avg_rides_per_hour': avg_rides_per_hour,
        'peak_hour': peak_hour,
        'peak_rides': peak_rides,
        'quiet_hour': quiet_hour,
        'quiet_rides': quiet_rides,
        'busiest_day': busiest_day,
        'busiest_day_rides': busiest_day_rides,
        'quietest_day': quietest_day,
        'quietest_day_rides': quietest_day_rides,
        'weekday_avg': weekday_avg,
        'weekend_avg': weekend_avg,
        'weekend_weekday_ratio': weekend_weekday_ratio,
        'daily_rides': daily_rides,
        'hourly_rides': hourly_rides,
        'day_rides': day_rides
    }
    
    return stats

def run_temporal_analysis():
    Path(anal.output_path_temporal).mkdir(parents = True, exist_ok = True)

    date_time = data_pipeline.get_temporal_data()
    
    # Calculate comprehensive statistics
    temporal_stats = calculate_temporal_statistics(date_time)  #type:ignore
    
    # Generate visualization data
    weekday_weekend = get_weekday_weekend_per_hour_dict(date_time)  #type:ignore
    every_day = get_per_day_dict(date_time) #type:ignore
    per_hour = get_per_hour_dict(date_time)  #type:ignore

    return {
        'weekday_weekend': weekday_weekend,
        'every_day': every_day,
        'per_hour': per_hour,
        'statistics': temporal_stats
    }