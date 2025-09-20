"""
WorldPop API Service
Open source population data for urban change and population density analysis
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class WorldPopService:
    def __init__(self):
        self.base_url = "https://hub.worldpop.org/rest/data"
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
    
    async def get_population_data(
        self, 
        country_code: str = "USA",
        year: int = 2020
    ) -> Dict[str, Any]:
        """
        Get population data for a specific country and year
        
        Args:
            country_code: ISO3 country code (e.g., 'USA', 'GBR', 'DEU')
            year: Year for population data (2000-2020)
        
        Returns:
            Dict containing population data and metadata
        """
        try:
            session = await self.get_session()
            
            # WorldPop API endpoint for population data
            url = f"{self.base_url}/pop/wpgp"
            params = {
                "iso3": country_code,
                "year": year
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_population_data(data, country_code, year)
                else:
                    raise Exception(f"API request failed with status {response.status}")
                    
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_urban_population_density(
        self, 
        lat: float, 
        lng: float, 
        country_code: str = "USA",
        year: int = 2020,
        radius_km: float = 10.0
    ) -> Dict[str, Any]:
        """
        Get urban population density for a specific location
        
        Args:
            lat: Latitude
            lng: Longitude
            country_code: ISO3 country code
            year: Year for population data
            radius_km: Search radius in kilometers
        
        Returns:
            Dict containing urban population density data
        """
        try:
            # First get country-level data
            country_data = await self.get_population_data(country_code, year)
            
            if not country_data.get("success"):
                return country_data
            
            # Process location-specific analysis
            urban_analysis = {
                "location": {"lat": lat, "lng": lng},
                "country": country_code,
                "year": year,
                "radius_km": radius_km,
                "population_metrics": {
                    "total_population": country_data.get("data", {}).get("total_population", 0),
                    "population_density": country_data.get("data", {}).get("population_density", 0),
                    "urban_percentage": country_data.get("data", {}).get("urban_percentage", 0)
                },
                "data_sources": country_data.get("data", {}).get("data_sources", []),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "data": urban_analysis,
                "message": f"Population density analysis for {country_code} in {year}"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_urban_growth_trends(
        self, 
        country_code: str = "USA",
        start_year: int = 2000,
        end_year: int = 2020
    ) -> Dict[str, Any]:
        """
        Get urban growth trends over time
        
        Args:
            country_code: ISO3 country code
            start_year: Starting year for trend analysis
            end_year: Ending year for trend analysis
        
        Returns:
            Dict containing urban growth trend data
        """
        try:
            session = await self.get_session()
            
            # Get data for multiple years
            trend_data = []
            years = list(range(start_year, end_year + 1, 5))  # Every 5 years
            
            for year in years:
                year_data = await self.get_population_data(country_code, year)
                if year_data.get("success"):
                    trend_data.append({
                        "year": year,
                        "total_population": year_data.get("data", {}).get("total_population", 0),
                        "population_density": year_data.get("data", {}).get("population_density", 0),
                        "urban_percentage": year_data.get("data", {}).get("urban_percentage", 0)
                    })
            
            # Calculate growth trends
            if len(trend_data) >= 2:
                first_year = trend_data[0]
                last_year = trend_data[-1]
                
                population_growth = ((last_year["total_population"] - first_year["total_population"]) / 
                                   first_year["total_population"]) * 100 if first_year["total_population"] > 0 else 0
                
                density_growth = ((last_year["population_density"] - first_year["population_density"]) / 
                                 first_year["population_density"]) * 100 if first_year["population_density"] > 0 else 0
                
                urban_growth = ((last_year["urban_percentage"] - first_year["urban_percentage"]) / 
                               first_year["urban_percentage"]) * 100 if first_year["urban_percentage"] > 0 else 0
            else:
                population_growth = density_growth = urban_growth = 0
            
            return {
                "success": True,
                "data": {
                    "country": country_code,
                    "period": f"{start_year}-{end_year}",
                    "trend_data": trend_data,
                    "growth_metrics": {
                        "population_growth_percent": round(population_growth, 2),
                        "density_growth_percent": round(density_growth, 2),
                        "urban_growth_percent": round(urban_growth, 2)
                    },
                    "analysis_timestamp": datetime.now().isoformat()
                },
                "message": f"Urban growth trends for {country_code} from {start_year} to {end_year}"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_demographic_analysis(
        self, 
        country_code: str = "USA",
        year: int = 2020
    ) -> Dict[str, Any]:
        """
        Get demographic analysis including age structure and urbanization
        
        Args:
            country_code: ISO3 country code
            year: Year for demographic data
        
        Returns:
            Dict containing demographic analysis data
        """
        try:
            # Get base population data
            population_data = await self.get_population_data(country_code, year)
            
            if not population_data.get("success"):
                return population_data
            
            # Enhanced demographic analysis
            demographic_analysis = {
                "country": country_code,
                "year": year,
                "demographics": {
                    "total_population": population_data.get("data", {}).get("total_population", 0),
                    "population_density": population_data.get("data", {}).get("population_density", 0),
                    "urban_percentage": population_data.get("data", {}).get("urban_percentage", 0),
                    "rural_percentage": 100 - population_data.get("data", {}).get("urban_percentage", 0)
                },
                "urban_planning_insights": {
                    "urbanization_level": self._categorize_urbanization(
                        population_data.get("data", {}).get("urban_percentage", 0)
                    ),
                    "density_category": self._categorize_density(
                        population_data.get("data", {}).get("population_density", 0)
                    ),
                    "planning_recommendations": self._generate_planning_recommendations(
                        population_data.get("data", {})
                    )
                },
                "data_sources": population_data.get("data", {}).get("data_sources", []),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "data": demographic_analysis,
                "message": f"Demographic analysis for {country_code} in {year}"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    def _process_population_data(self, raw_data: Dict[str, Any], country_code: str, year: int) -> Dict[str, Any]:
        """
        Process raw WorldPop data into a more usable format
        
        Args:
            raw_data: Raw response from WorldPop API
            country_code: Country code
            year: Year of data
        
        Returns:
            Processed data dictionary
        """
        try:
            # WorldPop API returns different structures, so we need to handle various formats
            processed_data = {
                "country": country_code,
                "year": year,
                "total_population": 0,
                "population_density": 0,
                "urban_percentage": 0,
                "data_sources": [],
                "metadata": {
                    "api_source": "WorldPop",
                    "resolution": "100m",
                    "methodology": "Unconstrained population estimates",
                    "last_updated": datetime.now().isoformat()
                }
            }
            
            # Handle different response formats
            if isinstance(raw_data, list) and len(raw_data) > 0:
                # If it's a list, take the first item
                data_item = raw_data[0]
                processed_data["total_population"] = data_item.get("total_population", 0)
                processed_data["population_density"] = data_item.get("population_density", 0)
                processed_data["urban_percentage"] = data_item.get("urban_percentage", 0)
                processed_data["data_sources"] = data_item.get("data_sources", [])
            elif isinstance(raw_data, dict):
                # If it's a dict, extract relevant fields
                processed_data["total_population"] = raw_data.get("total_population", 0)
                processed_data["population_density"] = raw_data.get("population_density", 0)
                processed_data["urban_percentage"] = raw_data.get("urban_percentage", 0)
                processed_data["data_sources"] = raw_data.get("data_sources", [])
            
            return {
                "success": True,
                "data": processed_data,
                "message": f"Population data retrieved for {country_code} in {year}"
            }
            
        except Exception as e:
            return {
                "error": f"Error processing WorldPop data: {str(e)}",
                "success": False,
                "data": None
            }
    
    def _categorize_urbanization(self, urban_percentage: float) -> str:
        """Categorize urbanization level based on percentage"""
        if urban_percentage >= 80:
            return "Highly Urbanized"
        elif urban_percentage >= 60:
            return "Moderately Urbanized"
        elif urban_percentage >= 40:
            return "Semi-Urbanized"
        else:
            return "Rural Dominant"
    
    def _categorize_density(self, density: float) -> str:
        """Categorize population density level"""
        if density >= 1000:
            return "Very High Density"
        elif density >= 500:
            return "High Density"
        elif density >= 100:
            return "Medium Density"
        elif density >= 50:
            return "Low Density"
        else:
            return "Very Low Density"
    
    def _generate_planning_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate urban planning recommendations based on demographic data"""
        recommendations = []
        
        urban_percentage = data.get("urban_percentage", 0)
        density = data.get("population_density", 0)
        
        if urban_percentage >= 80:
            recommendations.extend([
                "Focus on urban renewal and redevelopment",
                "Implement smart city technologies",
                "Enhance public transportation systems",
                "Develop vertical urban planning strategies"
            ])
        elif urban_percentage >= 60:
            recommendations.extend([
                "Plan for continued urbanization",
                "Invest in infrastructure development",
                "Balance urban and rural development",
                "Implement sustainable growth policies"
            ])
        else:
            recommendations.extend([
                "Prepare for urban migration trends",
                "Develop rural-urban connectivity",
                "Plan for future urban expansion",
                "Invest in rural infrastructure"
            ])
        
        if density >= 1000:
            recommendations.extend([
                "Implement high-density housing solutions",
                "Develop efficient public transport",
                "Create green spaces and parks",
                "Plan for vertical development"
            ])
        
        return recommendations
    
    async def get_available_countries(self) -> Dict[str, Any]:
        """
        Get list of available countries in WorldPop database
        
        Returns:
            Dict containing available countries
        """
        # Common country codes for testing
        common_countries = [
            {"code": "USA", "name": "United States of America"},
            {"code": "GBR", "name": "United Kingdom"},
            {"code": "DEU", "name": "Germany"},
            {"code": "FRA", "name": "France"},
            {"code": "JPN", "name": "Japan"},
            {"code": "CHN", "name": "China"},
            {"code": "IND", "name": "India"},
            {"code": "BRA", "name": "Brazil"},
            {"code": "CAN", "name": "Canada"},
            {"code": "AUS", "name": "Australia"}
        ]
        
        return {
            "success": True,
            "data": {
                "available_countries": common_countries,
                "total_countries": len(common_countries),
                "note": "This is a subset of available countries. Full list available from WorldPop API documentation."
            }
        }

# Example usage and testing
async def test_worldpop_service():
    """Test the WorldPop service with sample data"""
    async with WorldPopService() as service:
        # Test population data
        print("Testing population data...")
        result = await service.get_population_data("USA", 2020)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test urban population density
        print("\nTesting urban population density...")
        urban_result = await service.get_urban_population_density(40.7128, -74.0060, "USA", 2020)
        print(f"Urban Result: {json.dumps(urban_result, indent=2)}")
        
        # Test urban growth trends
        print("\nTesting urban growth trends...")
        trend_result = await service.get_urban_growth_trends("USA", 2000, 2020)
        print(f"Trend Result: {json.dumps(trend_result, indent=2)}")
        
        # Test demographic analysis
        print("\nTesting demographic analysis...")
        demo_result = await service.get_demographic_analysis("USA", 2020)
        print(f"Demo Result: {json.dumps(demo_result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_worldpop_service())
