"""
Landsat STAC API Service
High-resolution satellite imagery and surface reflectance data
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

class LandsatService:
    def __init__(self):
        self.base_url = "https://landsatlook.usgs.gov/stac-server"
        self.collection = "landsat-c2l2-sr"  # Landsat Collection 2 Level-2 Surface Reflectance
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def search_satellite_data(
        self, 
        bbox: List[float], 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        cloud_cover: Optional[int] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search for Landsat satellite data within a bounding box
        
        Args:
            bbox: [min_lon, min_lat, max_lon, max_lat]
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            cloud_cover: Maximum cloud cover percentage (0-100)
            limit: Maximum number of results
        
        Returns:
            Dict containing satellite data and metadata
        """
        try:
            session = await self.get_session()
            
            # Build query parameters
            params = {
                "bbox": ",".join(map(str, bbox)),
                "limit": limit,
                "collections": self.collection
            }
            
            if start_date:
                params["datetime"] = start_date
                if end_date:
                    params["datetime"] = f"{start_date}/{end_date}"
            
            if cloud_cover is not None:
                params["query"] = json.dumps({
                    "eo:cloud_cover": {"lte": cloud_cover}
                })
            
            url = f"{self.base_url}/collections/{self.collection}/items"
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_landsat_data(data)
                else:
                    raise Exception(f"API request failed with status {response.status}")
                    
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_satellite_imagery(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 5.0,
        cloud_cover: int = 20,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get satellite imagery for a specific location with radius
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
            cloud_cover: Maximum cloud cover percentage
            limit: Maximum number of results
        
        Returns:
            Dict containing satellite imagery data
        """
        # Calculate bounding box from center point and radius
        # Approximate conversion: 1 degree ≈ 111 km
        lat_offset = radius_km / 111.0
        lng_offset = radius_km / (111.0 * abs(lat) / 90.0)  # Adjust for latitude
        
        bbox = [
            lng - lng_offset,  # min_lon
            lat - lat_offset,  # min_lat
            lng + lng_offset,  # max_lon
            lat + lat_offset   # max_lat
        ]
        
        return await self.search_satellite_data(bbox, cloud_cover=cloud_cover, limit=limit)
    
    async def get_vegetation_analysis(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 5.0
    ) -> Dict[str, Any]:
        """
        Get vegetation analysis data (NDVI) for a location
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
        
        Returns:
            Dict containing vegetation analysis data
        """
        try:
            # Get satellite data
            satellite_data = await self.get_satellite_imagery(lat, lng, radius_km)
            
            if not satellite_data.get("success"):
                return satellite_data
            
            # Process vegetation data
            vegetation_analysis = {
                "location": {"lat": lat, "lng": lng},
                "radius_km": radius_km,
                "vegetation_metrics": [],
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            for item in satellite_data.get("data", []):
                if "assets" in item:
                    # Look for vegetation-related bands
                    vegetation_bands = {}
                    for band_name, band_info in item["assets"].items():
                        if band_name in ["nir08", "red", "green", "blue"]:
                            vegetation_bands[band_name] = band_info
                    
                    if vegetation_bands:
                        vegetation_analysis["vegetation_metrics"].append({
                            "date": item.get("properties", {}).get("datetime", ""),
                            "cloud_cover": item.get("properties", {}).get("eo:cloud_cover", 0),
                            "available_bands": list(vegetation_bands.keys()),
                            "band_info": vegetation_bands
                        })
            
            return {
                "success": True,
                "data": vegetation_analysis,
                "message": f"Found {len(vegetation_analysis['vegetation_metrics'])} vegetation data points"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_urban_heat_island_data(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 10.0
    ) -> Dict[str, Any]:
        """
        Get urban heat island analysis data
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
        
        Returns:
            Dict containing urban heat island data
        """
        try:
            # Get satellite data with low cloud cover for thermal analysis
            satellite_data = await self.get_satellite_imagery(
                lat, lng, radius_km, cloud_cover=10, limit=3
            )
            
            if not satellite_data.get("success"):
                return satellite_data
            
            heat_analysis = {
                "location": {"lat": lat, "lng": lng},
                "radius_km": radius_km,
                "thermal_data": [],
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            for item in satellite_data.get("data", []):
                if "assets" in item:
                    # Look for thermal bands
                    thermal_bands = {}
                    for band_name, band_info in item["assets"].items():
                        if "thermal" in band_name.lower() or band_name in ["lwir11", "lwir12"]:
                            thermal_bands[band_name] = band_info
                    
                    if thermal_bands:
                        heat_analysis["thermal_data"].append({
                            "date": item.get("properties", {}).get("datetime", ""),
                            "cloud_cover": item.get("properties", {}).get("eo:cloud_cover", 0),
                            "thermal_bands": thermal_bands
                        })
            
            return {
                "success": True,
                "data": heat_analysis,
                "message": f"Found {len(heat_analysis['thermal_data'])} thermal data points"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    def _process_landsat_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw Landsat STAC data into a more usable format
        
        Args:
            raw_data: Raw response from Landsat STAC API
        
        Returns:
            Processed data dictionary
        """
        try:
            processed_items = []
            
            for item in raw_data.get("features", []):
                processed_item = {
                    "id": item.get("id"),
                    "datetime": item.get("properties", {}).get("datetime"),
                    "cloud_cover": item.get("properties", {}).get("eo:cloud_cover", 0),
                    "satellite": item.get("properties", {}).get("platform"),
                    "instrument": item.get("properties", {}).get("instruments", [""])[0],
                    "geometry": item.get("geometry"),
                    "bbox": item.get("bbox"),
                    "assets": {}
                }
                
                # Process available bands/assets
                if "assets" in item:
                    for band_name, band_info in item["assets"].items():
                        processed_item["assets"][band_name] = {
                            "href": band_info.get("href"),
                            "title": band_info.get("title", band_name),
                            "description": band_info.get("description", ""),
                            "type": band_info.get("type", "image/tiff"),
                            "roles": band_info.get("roles", [])
                        }
                
                processed_items.append(processed_item)
            
            return {
                "success": True,
                "data": processed_items,
                "total_items": len(processed_items),
                "collection": self.collection,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Error processing Landsat data: {str(e)}",
                "success": False,
                "data": None
            }
    
    async def get_band_information(self) -> Dict[str, Any]:
        """
        Get information about available Landsat bands
        
        Returns:
            Dict containing band information
        """
        return {
            "success": True,
            "data": {
                "collection": self.collection,
                "bands": {
                    "coastal": {
                        "name": "Coastal Aerosol",
                        "wavelength": "0.43-0.45 μm",
                        "resolution": "30m",
                        "purpose": "Aerosol studies, coastal water mapping"
                    },
                    "blue": {
                        "name": "Blue",
                        "wavelength": "0.45-0.51 μm",
                        "resolution": "30m",
                        "purpose": "Water body detection, atmospheric haze penetration"
                    },
                    "green": {
                        "name": "Green",
                        "wavelength": "0.53-0.59 μm",
                        "resolution": "30m",
                        "purpose": "Vegetation health, water body detection"
                    },
                    "red": {
                        "name": "Red",
                        "wavelength": "0.64-0.67 μm",
                        "resolution": "30m",
                        "purpose": "Vegetation discrimination, soil analysis"
                    },
                    "nir08": {
                        "name": "Near-Infrared",
                        "wavelength": "0.85-0.88 μm",
                        "resolution": "30m",
                        "purpose": "Vegetation health, biomass estimation"
                    },
                    "swir16": {
                        "name": "Short-wave Infrared 1",
                        "wavelength": "1.57-1.65 μm",
                        "resolution": "30m",
                        "purpose": "Soil moisture, vegetation stress"
                    },
                    "swir22": {
                        "name": "Short-wave Infrared 2",
                        "wavelength": "2.11-2.29 μm",
                        "resolution": "30m",
                        "purpose": "Mineral mapping, soil analysis"
                    },
                    "lwir11": {
                        "name": "Thermal Infrared 1",
                        "wavelength": "10.60-11.19 μm",
                        "resolution": "100m",
                        "purpose": "Surface temperature, urban heat island"
                    },
                    "lwir12": {
                        "name": "Thermal Infrared 2",
                        "wavelength": "11.50-12.51 μm",
                        "resolution": "100m",
                        "purpose": "Surface temperature, atmospheric correction"
                    }
                },
                "applications": [
                    "Urban heat island analysis",
                    "Vegetation health monitoring",
                    "Water body detection",
                    "Land use classification",
                    "Environmental monitoring",
                    "Climate change studies"
                ]
            }
        }

# Example usage and testing
async def test_landsat_service():
    """Test the Landsat service with sample data"""
    async with LandsatService() as service:
        # Test satellite imagery search
        print("Testing satellite imagery search...")
        result = await service.get_satellite_imagery(40.7128, -74.0060, radius_km=5.0)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test vegetation analysis
        print("\nTesting vegetation analysis...")
        veg_result = await service.get_vegetation_analysis(40.7128, -74.0060)
        print(f"Vegetation Result: {json.dumps(veg_result, indent=2)}")
        
        # Test band information
        print("\nTesting band information...")
        band_info = await service.get_band_information()
        print(f"Band Info: {json.dumps(band_info, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_landsat_service())
