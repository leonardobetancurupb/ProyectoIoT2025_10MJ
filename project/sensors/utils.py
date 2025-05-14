from datetime import datetime, timedelta
import random
import colorsys
import math

def get_chart_colors(num_colors=1):
    """Generate visually distinct colors for charts"""
    colors = []
    for i in range(num_colors):
        # Use golden ratio conjugate to create well-distributed colors
        h = (i * 0.618033988749895) % 1
        # Make colors more vibrant
        s = 0.7
        v = 0.95
        rgb = colorsys.hsv_to_rgb(h, s, v)
        # Convert to hex
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0]*255), 
            int(rgb[1]*255), 
            int(rgb[2]*255)
        )
        colors.append(hex_color)
    
    return colors[0] if num_colors == 1 else colors

def prepare_time_series_data(sensor_data, time_range='24h'):
    """
    Transform sensor data into chart.js compatible format
    time_range: '24h', '7d', '30d', or 'all'
    """
    # Determine the cutoff time based on the time range
    now = datetime.now()
    
    if time_range == '24h':
        cutoff_time = now - timedelta(hours=24)
        interval = 'hourly'
    elif time_range == '7d':
        cutoff_time = now - timedelta(days=7)
        interval = 'daily'
    elif time_range == '30d':
        cutoff_time = now - timedelta(days=30)
        interval = 'daily'
    else:  # 'all'
        cutoff_time = now - timedelta(days=365)  # Just use a long time ago
        interval = 'weekly'
    
    # Filter data by time range
    filtered_data = [d for d in sensor_data if d.timestamp >= cutoff_time]
    
    # Format data for chart.js
    labels = [d.timestamp.strftime('%Y-%m-%d %H:%M' if interval == 'hourly' else '%Y-%m-%d') 
              for d in filtered_data]
    values = [float(d.value) for d in filtered_data]
    
    # Get a nice color for the chart
    color = get_chart_colors()
    
    # Create the chart data
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': f"Sensor Readings ({filtered_data[0].unit if filtered_data else 'N/A'})",
            'data': values,
            'fill': False,
            'borderColor': color,
            'backgroundColor': color + '20',  # Add transparency
            'tension': 0.1
        }]
    }
    
    return chart_data

def generate_demo_data(sensor, num_points=48):
    """Generate sample demo data for a sensor when no real data exists"""
    # Set the time range to cover the past 48 hours
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=num_points)
    
    # Determine base values based on sensor type
    if sensor.type.name.lower() == 'temperature':
        base_value = 22.0
        unit = '°C'
        variance = 3.0
    elif sensor.type.name.lower() == 'humidity':
        base_value = 45.0
        unit = '%'
        variance = 10.0
    elif sensor.type.name.lower() == 'pressure':
        base_value = 1013.0
        unit = 'hPa'
        variance = 5.0
    elif sensor.type.name.lower() == 'light':
        base_value = 500.0
        unit = 'lux'
        variance = 200.0
    else:
        base_value = 50.0
        unit = 'units'
        variance = 10.0
    
    # Generate the data points
    data_points = []
    current_time = start_time
    
    for i in range(num_points):
        # Create a smooth curve with some randomness
        time_factor = i / num_points
        trend_value = base_value + variance * 0.5 * math.sin(time_factor * 2 * math.pi)
        random_factor = random.uniform(-variance * 0.3, variance * 0.3)
        value = trend_value + random_factor
        
        # Ensure value is reasonable
        value = max(0, value)  # No negative values for these sensor types
        
        data_points.append({
            'timestamp': current_time,
            'value': round(value, 2),
            'unit': unit
        })
        
        current_time += timedelta(hours=1)
    
    return data_points
