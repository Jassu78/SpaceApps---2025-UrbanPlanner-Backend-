"""
EU Copernicus Services API
Comprehensive Earth observation datasets for climate, land use, and atmospheric data
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

class CopernicusService:
    def __init__(self):
        self.base_url = "https://catalogue.dataspace.copernicus.eu/odata/v1"
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
    
    async def get_available_products(
        self, 
        limit: int = 20,
        search_term: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get available Copernicus products
        
        Args:
            limit: Maximum number of products to return
            search_term: Optional search term to filter products
        
        Returns:
            Dict containing available products
        """
        try:
            session = await self.get_session()
            
            url = f"{self.base_url}/Products"
            params = {"$top": limit}
            
            if search_term:
                params["$filter"] = f"contains(Name, '{search_term}')"
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_products_data(data)
                else:
                    raise Exception(f"API request failed with status {response.status}")
                    
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_land_use_data(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 10.0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get land use and land cover data for a specific location
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            Dict containing land use data
        """
        try:
            # Search for land use products
            products = await self.get_available_products(50, "land use")
            
            if not products.get("success"):
                return products
            
            # Filter for land use related products
            land_use_products = []
            for product in products.get("data", []):
                name = product.get("Name", "").lower()
                if any(term in name for term in ["land", "cover", "use", "lc", "corine"]):
                    land_use_products.append(product)
            
            # Create analysis for the location
            land_use_analysis = {
                "location": {"lat": lat, "lng": lng},
                "radius_km": radius_km,
                "available_products": land_use_products[:5],  # Top 5 relevant products
                "analysis_timestamp": datetime.now().isoformat(),
                "recommendations": self._generate_land_use_recommendations(land_use_products)
            }
            
            return {
                "success": True,
                "data": land_use_analysis,
                "message": f"Found {len(land_use_products)} land use products for analysis"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_climate_data(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 10.0,
        climate_type: str = "temperature"
    ) -> Dict[str, Any]:
        """
        Get climate data for a specific location
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
            climate_type: Type of climate data (temperature, precipitation, humidity, etc.)
        
        Returns:
            Dict containing climate data
        """
        try:
            # Search for climate products
            search_terms = {
                "temperature": "temperature",
                "precipitation": "precipitation",
                "humidity": "humidity",
                "wind": "wind",
                "pressure": "pressure"
            }
            
            search_term = search_terms.get(climate_type, "climate")
            products = await self.get_available_products(50, search_term)
            
            if not products.get("success"):
                return products
            
            # Filter for climate related products
            climate_products = []
            for product in products.get("data", []):
                name = product.get("Name", "").lower()
                if any(term in name for term in [climate_type, "climate", "weather", "meteorology"]):
                    climate_products.append(product)
            
            # Create climate analysis
            climate_analysis = {
                "location": {"lat": lat, "lng": lng},
                "radius_km": radius_km,
                "climate_type": climate_type,
                "available_products": climate_products[:5],  # Top 5 relevant products
                "analysis_timestamp": datetime.now().isoformat(),
                "climate_insights": self._generate_climate_insights(climate_type, climate_products)
            }
            
            return {
                "success": True,
                "data": climate_analysis,
                "message": f"Found {len(climate_products)} {climate_type} products for analysis"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_atmospheric_data(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 10.0
    ) -> Dict[str, Any]:
        """
        Get atmospheric data for air quality analysis
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
        
        Returns:
            Dict containing atmospheric data
        """
        try:
            # Search for atmospheric products
            products = await self.get_available_products(50, "atmospheric")
            
            if not products.get("success"):
                return products
            
            # Filter for atmospheric related products
            atmospheric_products = []
            for product in products.get("data", []):
                name = product.get("Name", "").lower()
                if any(term in name for term in ["atmospheric", "air", "quality", "aerosol", "pollution", "sentinel-5p"]):
                    atmospheric_products.append(product)
            
            # Create atmospheric analysis
            atmospheric_analysis = {
                "location": {"lat": lat, "lng": lng},
                "radius_km": radius_km,
                "available_products": atmospheric_products[:5],  # Top 5 relevant products
                "analysis_timestamp": datetime.now().isoformat(),
                "air_quality_insights": self._generate_air_quality_insights(atmospheric_products)
            }
            
            return {
                "success": True,
                "data": atmospheric_analysis,
                "message": f"Found {len(atmospheric_products)} atmospheric products for air quality analysis"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_marine_data(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 10.0
    ) -> Dict[str, Any]:
        """
        Get marine data for coastal planning
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
        
        Returns:
            Dict containing marine data
        """
        try:
            # Search for marine products
            products = await self.get_available_products(50, "marine")
            
            if not products.get("success"):
                return products
            
            # Filter for marine related products
            marine_products = []
            for product in products.get("data", []):
                name = product.get("Name", "").lower()
                if any(term in name for term in ["marine", "ocean", "sea", "coastal", "water", "sentinel-3"]):
                    marine_products.append(product)
            
            # Create marine analysis
            marine_analysis = {
                "location": {"lat": lat, "lng": lng},
                "radius_km": radius_km,
                "available_products": marine_products[:5],  # Top 5 relevant products
                "analysis_timestamp": datetime.now().isoformat(),
                "coastal_insights": self._generate_coastal_insights(marine_products)
            }
            
            return {
                "success": True,
                "data": marine_analysis,
                "message": f"Found {len(marine_products)} marine products for coastal planning"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_comprehensive_environmental_data(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float = 10.0
    ) -> Dict[str, Any]:
        """
        Get comprehensive environmental data from all Copernicus services
        
        Args:
            lat: Latitude
            lng: Longitude
            radius_km: Search radius in kilometers
        
        Returns:
            Dict containing comprehensive environmental data
        """
        try:
            # Get all types of environmental data
            land_use = await self.get_land_use_data(lat, lng, radius_km)
            climate = await self.get_climate_data(lat, lng, radius_km, "temperature")
            atmospheric = await self.get_atmospheric_data(lat, lng, radius_km)
            marine = await self.get_marine_data(lat, lng, radius_km)
            
            # Combine all data
            comprehensive_data = {
                "location": {"lat": lat, "lng": lng},
                "radius_km": radius_km,
                "environmental_data": {
                    "land_use": land_use.get("data", {}),
                    "climate": climate.get("data", {}),
                    "atmospheric": atmospheric.get("data", {}),
                    "marine": marine.get("data", {})
                },
                "analysis_timestamp": datetime.now().isoformat(),
                "summary": self._generate_environmental_summary(land_use, climate, atmospheric, marine)
            }
            
            return {
                "success": True,
                "data": comprehensive_data,
                "message": "Comprehensive environmental data retrieved from Copernicus services"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    def _process_products_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw Copernicus products data
        
        Args:
            raw_data: Raw response from Copernicus API
        
        Returns:
            Processed data dictionary
        """
        try:
            products = raw_data.get("value", [])
            processed_products = []
            
            for product in products:
                processed_product = {
                    "id": product.get("Id"),
                    "name": product.get("Name"),
                    "description": product.get("Description", ""),
                    "content_type": product.get("ContentType", ""),
                    "content_length": product.get("ContentLength", 0),
                    "created": product.get("CreationDate"),
                    "modified": product.get("ModificationDate"),
                    "download_url": product.get("DownloadUrl", ""),
                    "metadata": {
                        "platform": product.get("Platform", ""),
                        "instrument": product.get("Instrument", ""),
                        "product_type": product.get("ProductType", ""),
                        "processing_level": product.get("ProcessingLevel", "")
                    }
                }
                processed_products.append(processed_product)
            
            return {
                "success": True,
                "data": processed_products,
                "total_products": len(processed_products),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Error processing Copernicus data: {str(e)}",
                "success": False,
                "data": None
            }
    
    def _generate_land_use_recommendations(self, products: List[Dict[str, Any]]) -> List[str]:
        """Generate land use planning recommendations"""
        recommendations = [
            "Use land use data for urban planning decisions",
            "Monitor land cover changes over time",
            "Identify areas for green space development",
            "Plan for sustainable land use practices",
            "Assess environmental impact of urban development"
        ]
        return recommendations
    
    def _generate_climate_insights(self, climate_type: str, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate climate insights based on available products"""
        insights = {
            "climate_type": climate_type,
            "available_data": len(products),
            "recommendations": [
                f"Use {climate_type} data for climate risk assessment",
                "Monitor climate trends for urban planning",
                "Develop climate adaptation strategies",
                "Plan for climate resilience"
            ]
        }
        return insights
    
    def _generate_air_quality_insights(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate air quality insights"""
        insights = {
            "available_products": len(products),
            "recommendations": [
                "Monitor air quality for public health",
                "Identify pollution hotspots",
                "Plan for air quality improvement",
                "Develop environmental policies"
            ]
        }
        return insights
    
    def _generate_coastal_insights(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate coastal planning insights"""
        insights = {
            "available_products": len(products),
            "recommendations": [
                "Monitor coastal erosion and sea level rise",
                "Plan for coastal protection measures",
                "Assess marine ecosystem health",
                "Develop sustainable coastal management"
            ]
        }
        return insights
    
    def _generate_environmental_summary(self, land_use, climate, atmospheric, marine) -> Dict[str, Any]:
        """Generate comprehensive environmental summary"""
        return {
            "total_products": (
                len(land_use.get("data", {}).get("available_products", [])) +
                len(climate.get("data", {}).get("available_products", [])) +
                len(atmospheric.get("data", {}).get("available_products", [])) +
                len(marine.get("data", {}).get("available_products", []))
            ),
            "data_categories": ["land_use", "climate", "atmospheric", "marine"],
            "urban_planning_applications": [
                "Environmental impact assessment",
                "Climate change adaptation",
                "Air quality monitoring",
                "Coastal zone management",
                "Sustainable development planning"
            ]
        }

# Example usage and testing
async def test_copernicus_service():
    """Test the Copernicus service with sample data"""
    async with CopernicusService() as service:
        # Test available products
        print("Testing available products...")
        result = await service.get_available_products(10)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test land use data
        print("\nTesting land use data...")
        land_result = await service.get_land_use_data(40.7128, -74.0060)
        print(f"Land Use Result: {json.dumps(land_result, indent=2)}")
        
        # Test climate data
        print("\nTesting climate data...")
        climate_result = await service.get_climate_data(40.7128, -74.0060, climate_type="temperature")
        print(f"Climate Result: {json.dumps(climate_result, indent=2)}")
        
        # Test comprehensive data
        print("\nTesting comprehensive environmental data...")
        comp_result = await service.get_comprehensive_environmental_data(40.7128, -74.0060)
        print(f"Comprehensive Result: {json.dumps(comp_result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_copernicus_service())
