import os
import django
import random
import math
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import models after Django setup
from django.contrib.auth.models import User
from accounts.models import UserProfile
from sensors.models import SensorType, Sensor, SensorData
from landing.models import News
from django.utils.text import slugify

def create_users():
    """Create test users"""
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )
        UserProfile.objects.create(user=admin)
        print("Admin user created")
    
    # Create regular users
    test_users = [
        ('john', 'John', 'Doe', 'john@example.com', 'password123'),
        ('jane', 'Jane', 'Smith', 'jane@example.com', 'password123'),
        ('bob', 'Bob', 'Johnson', 'bob@example.com', 'password123'),
    ]
    
    for username, first, last, email, password in test_users:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first,
                last_name=last
            )
            UserProfile.objects.create(user=user)
            print(f"Created user: {username}")

def create_sensor_types():
    """Create sensor types"""
    # Clear existing types first
    SensorType.objects.all().delete()
    
    types = [
        ('Humedad y Temperatura', 'Sensor que mide la humedad relativa y temperatura ambiente'),
        ('Radiacion Solar', 'Sensor que mide la intensidad de radiación solar'),
        ('Humedad de Suelo', 'Sensor que mide el nivel de humedad en el suelo'),
    ]
    
    for name, description in types:
        SensorType.objects.get_or_create(name=name, description=description)
    
    print(f"Created {len(types)} sensor types")

def create_sensors():
    """Create sample sensors for users"""
    # Get all user and sensor types
    users = User.objects.all()
    sensor_types = SensorType.objects.all()
    
    if not users or not sensor_types:
        print("No users or sensor types available")
        return
    
    locations = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garden', 
                'Basement', 'Garage', 'Office', 'Patio', 'Greenhouse']
    
    # For each user create 2-4 sensors
    for user in users:
        # Skip if user already has sensors
        if Sensor.objects.filter(owner=user).exists():
            continue
            
        num_sensors = random.randint(2, 4)
        for i in range(num_sensors):
            sensor_type = random.choice(sensor_types)
            location = random.choice(locations)
            name = f"{location} {sensor_type.name}"
            
            sensor = Sensor.objects.create(
                name=name,
                type=sensor_type,
                location=location,
                is_active=random.choice([True, True, False]),  # 2/3 chance of being active
                owner=user
            )
            print(f"Created sensor: {name} for {user.username}")
            
            # Generate sample sensor data
            create_sensor_data(sensor)

def create_sensor_data(sensor):
    """Create sample data for a sensor"""
    # Generate 48 hourly readings for the past 48 hours
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=48)
      # Set base value and unit based on sensor type
    if sensor.type.name == 'Humedad y Temperatura':
        base_value = 22.0  # room temperature in Celsius
        unit = '°C'
        variance = 3.0
    elif sensor.type.name == 'Radiacion Solar':
        base_value = 500.0  # W/m²
        unit = 'W/m²'
        variance = 200.0
    elif sensor.type.name == 'Humedad de Suelo':
        base_value = 35.0  # percent
        unit = '%'
        variance = 15.0
    else:
        base_value = 50.0
        unit = 'units'
        variance = 20.0
    
    # Generate readings
    current_time = start_time
    data_points = []
    
    while current_time <= end_time:
        # Add some randomness to the value with a slight trend
        time_factor = (current_time - start_time).total_seconds() / (end_time - start_time).total_seconds()
        trend = variance * 0.5 * math.sin(time_factor * 2 * math.pi)  # Sine wave variation
        random_factor = random.uniform(-variance * 0.5, variance * 0.5)  # Random noise
        
        value = base_value + trend + random_factor
        
        # Ensure values are reasonable
        value = max(0, value)  # No negative values for these sensor types
        
        data_points.append(
            SensorData(
                sensor=sensor,
                timestamp=current_time,
                value=round(value, 2),
                unit=unit
            )
        )
        
        current_time += timedelta(hours=1)
    
    # Bulk create the data points
    SensorData.objects.bulk_create(data_points)
    print(f"Created {len(data_points)} data points for sensor {sensor.name}")

def create_news_articles():
    """Create sample news articles"""
    if News.objects.exists():
        print("News articles already exist, skipping...")
        return
    
    articles = [
        {
            'title': 'New IoT Platform Release',
            'summary': 'Our latest platform update brings improved sensor management and real-time analytics.',
            'content': """
            <p>We are excited to announce the release of our new IoT Sensor Dashboard platform version 2.0!</p>
            
            <p>This major update includes:</p>
            <ul>
                <li>Improved real-time data visualization with customizable charts</li>
                <li>Enhanced notification system with SMS and email alerts</li>
                <li>New machine learning algorithms for anomaly detection</li>
                <li>Mobile app integration for on-the-go monitoring</li>
                <li>Expanded API for third-party integrations</li>
            </ul>
            
            <p>The update is available to all users immediately. Simply log in to your dashboard to experience the new features.</p>
            
            <p>We've also improved the security of our platform with enhanced encryption and two-factor authentication options. We recommend all users update their preferences in their account settings.</p>
            
            <p>Thank you for your continued support and feedback which helps us make our platform better with each update!</p>
            """
        },
        {
            'title': 'IoT Sensor Maintenance Tips',
            'summary': 'Learn how to maintain your sensors for optimal performance and longevity.',
            'content': """
            <p>Proper maintenance of your IoT sensors ensures accurate readings and extends their operational life. Here are our top tips for keeping your sensors in peak condition:</p>
            
            <h3>Regular Cleaning</h3>
            <p>Dust and debris can accumulate on sensors, affecting their accuracy. Gently clean sensors with a soft, dry cloth or compressed air. For stubborn dirt, use isopropyl alcohol on a cotton swab.</p>
            
            <h3>Check Power Sources</h3>
            <p>Battery-powered sensors need regular battery checks. Replace batteries before they're completely drained to avoid data loss. For wired sensors, inspect cables for damage or wear.</p>
            
            <h3>Calibrate Regularly</h3>
            <p>Sensors can drift over time. Follow manufacturer guidelines for calibration frequency—typically every 6-12 months. Our platform can remind you when calibration is due.</p>
            
            <h3>Monitor Environmental Conditions</h3>
            <p>Extreme temperatures and humidity can affect sensor performance. Ensure your sensors are installed in environments within their specified operating ranges.</p>
            
            <h3>Update Firmware</h3>
            <p>Keep your sensors' firmware up-to-date to benefit from bug fixes, security patches, and new features. Our platform automatically notifies you when updates are available.</p>
            
            <p>By following these simple maintenance tips, you can ensure your IoT sensor network continues to provide reliable data for your monitoring needs.</p>
            """
        },
        {
            'title': 'Case Study: Smart Agriculture Implementation',
            'summary': 'How a local farm increased crop yield by 30% using our IoT sensor solutions.',
            'content': """
            <p><strong>Client:</strong> Green Valley Farms</p>
            <p><strong>Challenge:</strong> Optimize irrigation and reduce water usage while maintaining or improving crop yields</p>
            
            <h3>Background</h3>
            <p>Green Valley Farms, a 500-acre vegetable farm, was facing increasing water costs and inconsistent crop yields due to inefficient irrigation practices. Traditional scheduling methods weren't accounting for varying soil conditions across different fields.</p>
            
            <h3>Solution</h3>
            <p>We implemented a network of 120 soil moisture sensors across the farm, strategically placed to cover different soil types and crop varieties. These sensors connected to our IoT platform provided real-time data on:</p>
            <ul>
                <li>Soil moisture at different depths</li>
                <li>Soil temperature</li>
                <li>Local weather conditions</li>
            </ul>
            
            <p>Our platform's machine learning algorithms analyzed the data to create automated, precision irrigation schedules tailored to each field section's needs.</p>
            
            <h3>Results</h3>
            <p>After one growing season with the IoT sensor system:</p>
            <ul>
                <li>30% increase in overall crop yield</li>
                <li>25% reduction in water usage</li>
                <li>20% decrease in fertilizer costs due to reduced runoff</li>
                <li>ROI achieved within 8 months of implementation</li>
            </ul>
            
            <p>The farm manager now receives automated alerts when soil conditions require attention and can monitor all fields from a mobile device. The system continues to improve its recommendations as it collects more seasonal data.</p>
            
            <p>"This technology has transformed how we approach farming. We're working smarter, not harder, and seeing better results while using fewer resources." - James Peterson, Farm Manager</p>
            """
        },
        {
            'title': 'Upcoming Webinar: Advanced IoT Security',
            'summary': 'Join our security experts for a free webinar on protecting your IoT ecosystem.',
            'content': """
            <h3>Advanced IoT Security: Protecting Your Connected Environment</h3>
            
            <p><strong>Date:</strong> June 15, 2023<br>
            <strong>Time:</strong> 2:00 PM - 3:30 PM EST<br>
            <strong>Format:</strong> Online Webinar (Zoom)<br>
            <strong>Cost:</strong> Free</p>
            
            <p>As IoT deployments expand across industries, security concerns continue to grow. Join us for this informative session where our security experts will discuss the latest threats to IoT systems and practical strategies to mitigate risks.</p>
            
            <h4>Topics covered:</h4>
            <ul>
                <li>Common vulnerabilities in IoT sensor networks</li>
                <li>Encryption best practices for IoT data</li>
                <li>Secure authentication and authorization methods</li>
                <li>Monitoring tools for threat detection</li>
                <li>Creating an IoT security policy for your organization</li>
            </ul>
            
            <h4>Who should attend:</h4>
            <ul>
                <li>IT Security Professionals</li>
                <li>IoT Project Managers</li>
                <li>System Administrators</li>
                <li>CISOs and Security Executives</li>
                <li>Anyone responsible for IoT implementation</li>
            </ul>
            
            <p>All participants will receive a complimentary IoT Security Checklist and access to the webinar recording.</p>
            
            <p><strong>Registration:</strong> Space is limited. Register now through our website or contact us at webinars@example.com.</p>
            """
        },
    ]
    
    for article_data in articles:
        article = News.objects.create(
            title=article_data['title'],
            summary=article_data['summary'],
            content=article_data['content'],
            slug=slugify(article_data['title']),
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        print(f"Created news article: {article.title}")

if __name__ == '__main__':
    print("Starting data initialization...")
    
    # Create data in the correct order
    create_users()
    create_sensor_types()
    create_sensors()
    create_news_articles()
    
    print("Data initialization complete!")
