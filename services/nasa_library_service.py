"""
NASA Image and Video Library API Service
Historical imagery and videos for urban planning visualization
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

class NASALibraryService:
    def __init__(self):
        self.base_url = "https://images-api.nasa.gov"
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
    
    async def search_urban_imagery(
        self, 
        query: str = "urban",
        media_type: str = "image",
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Search for urban-related imagery and videos
        
        Args:
            query: Search query (e.g., "urban", "city", "satellite")
            media_type: Type of media ("image", "video", "audio")
            year_start: Start year for search
            year_end: End year for search
            page: Page number for pagination
            page_size: Number of results per page
        
        Returns:
            Dict containing search results
        """
        try:
            session = await self.get_session()
            
            # Build search parameters
            params = {
                "q": query,
                "media_type": media_type,
                "page": page
            }
            
            if year_start:
                params["year_start"] = year_start
            if year_end:
                params["year_end"] = year_end
            
            url = f"{self.base_url}/search"
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_search_results(data, query, media_type)
                else:
                    raise Exception(f"API request failed with status {response.status}")
                    
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_historical_urban_data(
        self, 
        city_name: str = "New York",
        decade: Optional[str] = None,
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """
        Get historical urban imagery for a specific city
        
        Args:
            city_name: Name of the city to search for
            decade: Specific decade (e.g., "1990s", "2000s", "2010s")
            media_type: Type of media to search for
        
        Returns:
            Dict containing historical urban data
        """
        try:
            # Build search query
            query = f"{city_name} urban city satellite"
            if decade:
                query += f" {decade}"
            
            # Search for historical data
            search_result = await self.search_urban_imagery(
                query=query,
                media_type=media_type,
                page_size=50
            )
            
            if not search_result.get("success"):
                return search_result
            
            # Process historical analysis
            historical_analysis = {
                "city": city_name,
                "decade": decade,
                "media_type": media_type,
                "total_results": search_result.get("data", {}).get("total_results", 0),
                "items": search_result.get("data", {}).get("items", []),
                "historical_insights": self._generate_historical_insights(
                    search_result.get("data", {}).get("items", []),
                    city_name,
                    decade
                ),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "data": historical_analysis,
                "message": f"Historical urban data retrieved for {city_name}"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_climate_change_visualization(
        self, 
        location: str = "global",
        time_period: str = "decade",
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """
        Get climate change visualization imagery
        
        Args:
            location: Location to search for (e.g., "global", "Arctic", "Antarctica")
            time_period: Time period for comparison (e.g., "decade", "year")
            media_type: Type of media to search for
        
        Returns:
            Dict containing climate change visualization data
        """
        try:
            # Build climate change search query
            climate_queries = [
                f"{location} climate change",
                f"{location} global warming",
                f"{location} temperature",
                f"{location} ice melting",
                f"{location} sea level rise"
            ]
            
            all_results = []
            for query in climate_queries:
                result = await self.search_urban_imagery(
                    query=query,
                    media_type=media_type,
                    page_size=10
                )
                if result.get("success"):
                    all_results.extend(result.get("data", {}).get("items", []))
            
            # Process climate change analysis
            climate_analysis = {
                "location": location,
                "time_period": time_period,
                "total_results": len(all_results),
                "items": all_results[:20],  # Top 20 results
                "climate_insights": self._generate_climate_insights(all_results, location),
                "visualization_recommendations": self._generate_visualization_recommendations(location),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "data": climate_analysis,
                "message": f"Climate change visualization data retrieved for {location}"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_earth_observation_data(
        self, 
        observation_type: str = "satellite",
        resolution: str = "high",
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """
        Get Earth observation data and imagery
        
        Args:
            observation_type: Type of observation (e.g., "satellite", "aerial", "space")
            resolution: Resolution preference (e.g., "high", "medium", "low")
            media_type: Type of media to search for
        
        Returns:
            Dict containing Earth observation data
        """
        try:
            # Build Earth observation search query
            query = f"Earth observation {observation_type} {resolution} resolution"
            
            search_result = await self.search_urban_imagery(
                query=query,
                media_type=media_type,
                page_size=30
            )
            
            if not search_result.get("success"):
                return search_result
            
            # Process Earth observation analysis
            earth_observation_analysis = {
                "observation_type": observation_type,
                "resolution": resolution,
                "total_results": search_result.get("data", {}).get("total_results", 0),
                "items": search_result.get("data", {}).get("items", []),
                "observation_insights": self._generate_observation_insights(
                    search_result.get("data", {}).get("items", []),
                    observation_type
                ),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "data": earth_observation_analysis,
                "message": f"Earth observation data retrieved for {observation_type}"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    async def get_urban_planning_visuals(
        self, 
        planning_aspect: str = "sustainability",
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """
        Get urban planning visualization materials
        
        Args:
            planning_aspect: Aspect of urban planning (e.g., "sustainability", "transportation", "housing")
            media_type: Type of media to search for
        
        Returns:
            Dict containing urban planning visuals
        """
        try:
            # Build urban planning search query
            planning_queries = [
                f"urban planning {planning_aspect}",
                f"smart city {planning_aspect}",
                f"sustainable city {planning_aspect}",
                f"urban development {planning_aspect}",
                f"city design {planning_aspect}"
            ]
            
            all_results = []
            for query in planning_queries:
                result = await self.search_urban_imagery(
                    query=query,
                    media_type=media_type,
                    page_size=10
                )
                if result.get("success"):
                    all_results.extend(result.get("data", {}).get("items", []))
            
            # Process urban planning analysis
            planning_analysis = {
                "planning_aspect": planning_aspect,
                "total_results": len(all_results),
                "items": all_results[:20],  # Top 20 results
                "planning_insights": self._generate_planning_insights(all_results, planning_aspect),
                "visualization_guidelines": self._generate_visualization_guidelines(planning_aspect),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "data": planning_analysis,
                "message": f"Urban planning visuals retrieved for {planning_aspect}"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "data": None
            }
    
    def _process_search_results(self, raw_data: Dict[str, Any], query: str, media_type: str) -> Dict[str, Any]:
        """
        Process raw NASA Library search results
        
        Args:
            raw_data: Raw response from NASA Library API
            query: Search query used
            media_type: Media type searched
        
        Returns:
            Processed data dictionary
        """
        try:
            items = raw_data.get("collection", {}).get("items", [])
            processed_items = []
            
            for item in items:
                processed_item = {
                    "nasa_id": item.get("data", [{}])[0].get("nasa_id", ""),
                    "title": item.get("data", [{}])[0].get("title", ""),
                    "description": item.get("data", [{}])[0].get("description", ""),
                    "date_created": item.get("data", [{}])[0].get("date_created", ""),
                    "center": item.get("data", [{}])[0].get("center", ""),
                    "keywords": item.get("data", [{}])[0].get("keywords", []),
                    "media_type": item.get("data", [{}])[0].get("media_type", ""),
                    "href": item.get("href", ""),
                    "links": item.get("links", [])
                }
                processed_items.append(processed_item)
            
            return {
                "success": True,
                "data": {
                    "query": query,
                    "media_type": media_type,
                    "total_results": raw_data.get("collection", {}).get("metadata", {}).get("total_hits", 0),
                    "items": processed_items,
                    "search_timestamp": datetime.now().isoformat()
                },
                "message": f"Found {len(processed_items)} results for '{query}'"
            }
            
        except Exception as e:
            return {
                "error": f"Error processing NASA Library data: {str(e)}",
                "success": False,
                "data": None
            }
    
    def _generate_historical_insights(self, items: List[Dict[str, Any]], city_name: str, decade: Optional[str]) -> Dict[str, Any]:
        """Generate historical insights from imagery"""
        insights = {
            "city": city_name,
            "decade": decade,
            "total_images": len(items),
            "date_range": self._extract_date_range(items),
            "common_themes": self._extract_common_themes(items),
            "urban_development_indicators": [
                "Building density changes",
                "Infrastructure development",
                "Green space evolution",
                "Transportation network growth"
            ]
        }
        return insights
    
    def _generate_climate_insights(self, items: List[Dict[str, Any]], location: str) -> Dict[str, Any]:
        """Generate climate change insights"""
        insights = {
            "location": location,
            "total_images": len(items),
            "climate_indicators": [
                "Temperature changes",
                "Ice cover variations",
                "Sea level changes",
                "Vegetation changes",
                "Urban heat island effects"
            ],
            "visualization_potential": "High - suitable for before/after comparisons"
        }
        return insights
    
    def _generate_observation_insights(self, items: List[Dict[str, Any]], observation_type: str) -> Dict[str, Any]:
        """Generate Earth observation insights"""
        insights = {
            "observation_type": observation_type,
            "total_images": len(items),
            "applications": [
                "Urban planning visualization",
                "Environmental monitoring",
                "Climate change documentation",
                "Public engagement materials"
            ],
            "quality_indicators": "High-resolution imagery available"
        }
        return insights
    
    def _generate_planning_insights(self, items: List[Dict[str, Any]], planning_aspect: str) -> Dict[str, Any]:
        """Generate urban planning insights"""
        insights = {
            "planning_aspect": planning_aspect,
            "total_images": len(items),
            "planning_applications": [
                "Public presentation materials",
                "Community engagement visuals",
                "Policy documentation",
                "Educational resources"
            ],
            "visualization_strengths": "Professional quality imagery for urban planning"
        }
        return insights
    
    def _generate_visualization_recommendations(self, location: str) -> List[str]:
        """Generate visualization recommendations"""
        recommendations = [
            "Use high-resolution imagery for presentations",
            "Create before/after comparisons for impact assessment",
            "Develop interactive visualizations for public engagement",
            "Incorporate time-lapse sequences for trend analysis"
        ]
        return recommendations
    
    def _generate_visualization_guidelines(self, planning_aspect: str) -> List[str]:
        """Generate visualization guidelines"""
        guidelines = [
            "Ensure imagery is relevant to planning context",
            "Use high-quality, professional images",
            "Include proper attribution and metadata",
            "Consider accessibility in visual design"
        ]
        return guidelines
    
    def _extract_date_range(self, items: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract date range from items"""
        dates = [item.get("date_created", "") for item in items if item.get("date_created")]
        if dates:
            return {
                "earliest": min(dates),
                "latest": max(dates)
            }
        return {"earliest": "", "latest": ""}
    
    def _extract_common_themes(self, items: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes from items"""
        all_keywords = []
        for item in items:
            keywords = item.get("keywords", [])
            if isinstance(keywords, list):
                all_keywords.extend(keywords)
        
        # Count keyword frequency
        keyword_count = {}
        for keyword in all_keywords:
            keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        # Return top 5 most common keywords
        sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
        return [keyword for keyword, count in sorted_keywords[:5]]

# Example usage and testing
async def test_nasa_library_service():
    """Test the NASA Library service with sample data"""
    async with NASALibraryService() as service:
        # Test urban imagery search
        print("Testing urban imagery search...")
        result = await service.search_urban_imagery("urban city satellite")
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test historical urban data
        print("\nTesting historical urban data...")
        hist_result = await service.get_historical_urban_data("New York", "2010s")
        print(f"Historical Result: {json.dumps(hist_result, indent=2)}")
        
        # Test climate change visualization
        print("\nTesting climate change visualization...")
        climate_result = await service.get_climate_change_visualization("global")
        print(f"Climate Result: {json.dumps(climate_result, indent=2)}")
        
        # Test urban planning visuals
        print("\nTesting urban planning visuals...")
        planning_result = await service.get_urban_planning_visuals("sustainability")
        print(f"Planning Result: {json.dumps(planning_result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_nasa_library_service())
