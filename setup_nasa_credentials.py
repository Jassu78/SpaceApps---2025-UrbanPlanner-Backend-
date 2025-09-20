#!/usr/bin/env python3
"""
NASA Earthdata Credentials Setup Script
Helps configure NASA API access for the Urban Planning Tool
"""

import os
import getpass
from pathlib import Path

def setup_nasa_credentials():
    """Interactive setup for NASA Earthdata credentials"""
    print("🚀 NASA Urban Planning Tool - Credentials Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Found existing .env file")
        overwrite = input("Do you want to update your NASA credentials? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📋 NASA Earthdata Account Setup:")
    print("1. Go to https://urs.earthdata.nasa.gov/")
    print("2. Create an account or log in")
    print("3. Generate an app password for this application")
    print("4. Copy your username and app password")
    
    print("\n🔑 Enter your NASA Earthdata credentials:")
    username = input("Username: ").strip()
    password = getpass.getpass("App Password: ").strip()
    
    if not username or not password:
        print("❌ Username and password are required!")
        return
    
    # Create .env file
    env_content = f"""# NASA Earthdata API Configuration
NASA_EARTHDATA_USERNAME={username}
NASA_EARTHDATA_PASSWORD={password}
NASA_EARTHDATA_TOKEN=

# Gemini AI API Configuration (Optional)
GEMINI_API_KEY=

# Database Configuration (for future use)
DATABASE_URL=postgresql://user:password@localhost:5432/urban_planning

# Redis Configuration (for future use)
REDIS_URL=redis://localhost:6379

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://space-apps-2025-urban-planner.vercel.app
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("\n✅ Credentials saved to .env file")
    print("\n🔧 Next steps:")
    print("1. Test your credentials with: python test_nasa_connection.py")
    print("2. Start the API server with: python main.py")
    print("3. Access the API docs at: http://localhost:8000/docs")
    
    print("\n📚 For more information:")
    print("- NASA Earthdata: https://earthdata.nasa.gov/")
    print("- CMR API: https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html")
    print("- GIBS API: https://gibs.earthdata.nasa.gov/")

def test_nasa_connection():
    """Test NASA API connection"""
    print("🧪 Testing NASA API Connection...")
    
    try:
        from services.real_nasa_service import RealNASAService
        
        nasa_service = RealNASAService()
        
        # Test with a simple coordinate
        print("Testing with coordinates: 40.7128, -74.0060 (New York)")
        
        import asyncio
        result = asyncio.run(nasa_service.get_modis_temperature_data(40.7128, -74.0060))
        
        print("✅ NASA API connection successful!")
        print(f"Data source: {result.get('data_source', 'unknown')}")
        print(f"Granules found: {result.get('granules_found', 0)}")
        print(f"Temperature: {result.get('temperature_celsius', 'N/A')}°C")
        
    except Exception as e:
        print(f"❌ NASA API connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your credentials in .env file")
        print("2. Verify your internet connection")
        print("3. Make sure your NASA account has proper permissions")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Setup NASA credentials")
    print("2. Test NASA connection")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        setup_nasa_credentials()
    elif choice == "2":
        test_nasa_connection()
    else:
        print("Invalid choice. Please run the script again.")

