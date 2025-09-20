"""
Test script for Real NASA Space Apps Challenge 2025 Data Sources
Tests actual API calls to official NASA resources
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.official_nasa_service import OfficialNASAService

async def test_real_apis():
    """Test real API calls to official NASA resources"""
    
    print("🚀 Testing Real NASA Space Apps Challenge 2025 Data Sources")
    print("=" * 70)
    print("⚠️  Note: This will make real API calls to external services")
    print("   Some calls may fail due to authentication or rate limits")
    print("=" * 70)
    
    # Initialize service
    nasa_service = OfficialNASAService()
    
    # Test coordinates (New York City)
    test_lat = 40.7128
    test_lng = -74.0060
    
    print(f"📍 Test Location: New York City ({test_lat}, {test_lng})")
    print()
    
    # Test individual sources with timeout
    print("1. 🌍 Testing NASA Earthdata Worldview...")
    try:
        earthdata_result = await asyncio.wait_for(
            nasa_service.get_earthdata_worldview_data(test_lat, test_lng), 
            timeout=10.0
        )
        print(f"   Status: {'✅ Success' if 'error' not in earthdata_result else '❌ Error'}")
        if 'error' not in earthdata_result:
            print(f"   Source: {earthdata_result.get('source', 'Unknown')}")
        else:
            print(f"   Error: {earthdata_result['error']}")
    except asyncio.TimeoutError:
        print("   Status: ⏰ Timeout (10s)")
    except Exception as e:
        print(f"   Status: ❌ Exception: {str(e)}")
    print()
    
    print("2. 👥 Testing NASA SEDAC Demographic Data...")
    try:
        sedac_result = await asyncio.wait_for(
            nasa_service.get_sedac_demographic_data(test_lat, test_lng), 
            timeout=10.0
        )
        print(f"   Status: {'✅ Success' if 'error' not in sedac_result else '❌ Error'}")
        if 'error' not in sedac_result:
            print(f"   Source: {sedac_result.get('source', 'Unknown')}")
        else:
            print(f"   Error: {sedac_result['error']}")
    except asyncio.TimeoutError:
        print("   Status: ⏰ Timeout (10s)")
    except Exception as e:
        print(f"   Status: ❌ Exception: {str(e)}")
    print()
    
    print("3. 🏙️ Testing EU Copernicus GHSL Urban Data...")
    try:
        ghsl_result = await asyncio.wait_for(
            nasa_service.get_ghsl_urban_data(test_lat, test_lng), 
            timeout=10.0
        )
        print(f"   Status: {'✅ Success' if 'error' not in ghsl_result else '❌ Error'}")
        if 'error' not in ghsl_result:
            print(f"   Source: {ghsl_result.get('source', 'Unknown')}")
        else:
            print(f"   Error: {ghsl_result['error']}")
    except asyncio.TimeoutError:
        print("   Status: ⏰ Timeout (10s)")
    except Exception as e:
        print(f"   Status: ❌ Exception: {str(e)}")
    print()
    
    print("=" * 70)
    print("🎯 Test Summary:")
    print("   - Real API calls tested with 10-second timeouts")
    print("   - Some calls may fail due to authentication requirements")
    print("   - This is normal for external API testing")
    print("   - Ready for hackathon with real data integration! 🚀")

if __name__ == "__main__":
    asyncio.run(test_real_apis())
