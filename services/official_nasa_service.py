"""
Official NASA Space Apps Challenge 2025 Data Integration Service
Integrates with official NASA resources for Data Pathways to Healthy Cities
"""

import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class OfficialNASAService:
    """
    Official NASA Space Apps Challenge 2025 Data Integration Service
    Connects to official NASA resources for urban planning and health data
    """
    
    def __init__(self):
        self.base_urls = {
            'earthdata_worldview': 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best',
            'sedac': 'https://sedac.ciesin.columbia.edu/data/set',
            'ghsl': 'https://ghsl.jrc.ec.europa.eu',
            'worldpop': 'https://www.worldpop.org/rest/data',
            'copernicus': 'https://dataspace.copernicus.eu/analyse/apis/catalogue-apis',
            'wri': 'https://resource-watch.github.io/doc-api'
        }
        
        # NASA Earthdata credentials
        self.earthdata_token = os.getenv('NASA_EARTHDATA_TOKEN')
        self.earthdata_username = os.getenv('NASA_EARTHDATA_USERNAME')
        self.earthdata_password = os.getenv('NASA_EARTHDATA_PASSWORD')
        
    async def get_earthdata_worldview_data(self, 
                                         lat: float, 
                                         lng: float, 
                                         layer: str = 'MODIS_Terra_Land_Surface_Temperature_Day',
                                         date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get data from NASA Earthdata Worldview
        Primary satellite data visualization platform
        """
        try:
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            
            # Calculate zoom level based on coordinates
            zoom = self._calculate_zoom_level(lat, lng)
            
            # Construct Worldview URL
            url = f"{self.base_urls['earthdata_worldview']}/{layer}/default/{date}/{zoom}/{self._lat_to_tile(lat, zoom)}/{self._lng_to_tile(lng, zoom)}.png"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # For now, return metadata about the tile
                        # In production, you'd process the actual image data
                        return {
                            'source': 'NASA Earthdata Worldview',
                            'layer': layer,
                            'date': date,
                            'coordinates': {'lat': lat, 'lng': lng},
                            'tile_url': url,
                            'status': 'success',
                            'description': 'Satellite data visualization from NASA Earthdata Worldview'
                        }
                    else:
                        return {'error': f'Failed to fetch data: {response.status}'}
                        
        except Exception as e:
            return {'error': f'Error accessing Earthdata Worldview: {str(e)}'}
    
    async def get_sedac_demographic_data(self, 
                                       lat: float, 
                                       lng: float,
                                       dataset: str = 'gpw-v4-population-density') -> Dict[str, Any]:
        """
        Get demographic and equity data from NASA SEDAC
        Social and environmental dynamics data (UN SDGs)
        """
        try:
            # SEDAC API endpoint for population density
            url = f"https://sedac.ciesin.columbia.edu/data/set/{dataset}/api"
            
            params = {
                'lat': lat,
                'lng': lng,
                'format': 'json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'source': 'NASA SEDAC',
                            'dataset': dataset,
                            'coordinates': {'lat': lat, 'lng': lng},
                            'data': data,
                            'status': 'success',
                            'description': 'Demographic and equity data from NASA SEDAC'
                        }
                    else:
                        return {'error': f'Failed to fetch SEDAC data: {response.status}'}
                        
        except Exception as e:
            return {'error': f'Error accessing SEDAC data: {str(e)}'}
    
    async def get_ghsl_urban_data(self, 
                                 lat: float, 
                                 lng: float,
                                 dataset: str = 'built-up-area') -> Dict[str, Any]:
        """
        Get urban settlement data from EU Copernicus GHSL
        Global population and urban density data
        """
        try:
            # GHSL API endpoint
            url = f"{self.base_urls['ghsl']}/api/urban-settlement"
            
            params = {
                'lat': lat,
                'lng': lng,
                'dataset': dataset,
                'format': 'json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'source': 'EU Copernicus GHSL',
                            'dataset': dataset,
                            'coordinates': {'lat': lat, 'lng': lng},
                            'data': data,
                            'status': 'success',
                            'description': 'Urban settlement data from EU Copernicus GHSL'
                        }
                    else:
                        return {'error': f'Failed to fetch GHSL data: {response.status}'}
                        
        except Exception as e:
            return {'error': f'Error accessing GHSL data: {str(e)}'}
    
    async def get_worldpop_data(self, 
                               lat: float, 
                               lng: float,
                               year: int = 2020) -> Dict[str, Any]:
        """
        Get population data from WorldPop
        Open source population data for urban change analysis
        """
        try:
            # WorldPop API endpoint
            url = f"{self.base_urls['worldpop']}/population"
            
            params = {
                'lat': lat,
                'lng': lng,
                'year': year,
                'format': 'json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'source': 'WorldPop',
                            'year': year,
                            'coordinates': {'lat': lat, 'lng': lng},
                            'data': data,
                            'status': 'success',
                            'description': 'Population data from WorldPop'
                        }
                    else:
                        return {'error': f'Failed to fetch WorldPop data: {response.status}'}
                        
        except Exception as e:
            return {'error': f'Error accessing WorldPop data: {str(e)}'}
    
    async def get_copernicus_climate_data(self, 
                                        lat: float, 
                                        lng: float,
                                        dataset: str = 'land-use') -> Dict[str, Any]:
        """
        Get climate and land use data from EU Copernicus
        Comprehensive Earth observation datasets
        """
        try:
            # Copernicus API endpoint
            url = f"{self.base_urls['copernicus']}/land-use"
            
            params = {
                'lat': lat,
                'lng': lng,
                'dataset': dataset,
                'format': 'json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'source': 'EU Copernicus',
                            'dataset': dataset,
                            'coordinates': {'lat': lat, 'lng': lng},
                            'data': data,
                            'status': 'success',
                            'description': 'Climate and land use data from EU Copernicus'
                        }
                    else:
                        return {'error': f'Failed to fetch Copernicus data: {response.status}'}
                        
        except Exception as e:
            return {'error': f'Error accessing Copernicus data: {str(e)}'}
    
    async def get_wri_urban_data(self, 
                                lat: float, 
                                lng: float,
                                dataset: str = 'urban-landscape') -> Dict[str, Any]:
        """
        Get urban landscape data from World Resources Institute
        Urban landscapes, ecosystems, climate, and economic data
        """
        try:
            # WRI API endpoint
            url = f"{self.base_urls['wri']}/urban-landscape"
            
            params = {
                'lat': lat,
                'lng': lng,
                'dataset': dataset,
                'format': 'json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'source': 'World Resources Institute',
                            'dataset': dataset,
                            'coordinates': {'lat': lat, 'lng': lng},
                            'data': data,
                            'status': 'success',
                            'description': 'Urban landscape data from World Resources Institute'
                        }
                    else:
                        return {'error': f'Failed to fetch WRI data: {response.status}'}
                        
        except Exception as e:
            return {'error': f'Error accessing WRI data: {str(e)}'}
    
    async def get_comprehensive_urban_data(self, 
                                         lat: float, 
                                         lng: float) -> Dict[str, Any]:
        """
        Get comprehensive urban data from all official sources
        Combines data from NASA, SEDAC, GHSL, WorldPop, Copernicus, and WRI
        """
        try:
            # Fetch data from all sources concurrently
            tasks = [
                self.get_earthdata_worldview_data(lat, lng),
                self.get_sedac_demographic_data(lat, lng),
                self.get_ghsl_urban_data(lat, lng),
                self.get_worldpop_data(lat, lng),
                self.get_copernicus_climate_data(lat, lng),
                self.get_wri_urban_data(lat, lng)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Organize results by source
            comprehensive_data = {
                'coordinates': {'lat': lat, 'lng': lng},
                'timestamp': datetime.now().isoformat(),
                'sources': {
                    'nasa_earthdata': results[0],
                    'nasa_sedac': results[1],
                    'eu_ghsl': results[2],
                    'worldpop': results[3],
                    'eu_copernicus': results[4],
                    'wri': results[5]
                },
                'summary': {
                    'total_sources': len([r for r in results if not isinstance(r, Exception)]),
                    'successful_sources': [r.get('source', 'Unknown') for r in results if not isinstance(r, Exception) and 'source' in r],
                    'failed_sources': [str(r) for r in results if isinstance(r, Exception)]
                }
            }
            
            return comprehensive_data
            
        except Exception as e:
            return {'error': f'Error getting comprehensive data: {str(e)}'}
    
    def _calculate_zoom_level(self, lat: float, lng: float) -> int:
        """Calculate appropriate zoom level for coordinates"""
        # Simple zoom calculation based on latitude
        if abs(lat) > 60:
            return 3
        elif abs(lat) > 30:
            return 4
        elif abs(lat) > 15:
            return 5
        else:
            return 6
    
    def _lat_to_tile(self, lat: float, zoom: int) -> int:
        """Convert latitude to tile Y coordinate"""
        import math
        return int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * (2 ** zoom))
    
    def _lng_to_tile(self, lng: float, zoom: int) -> int:
        """Convert longitude to tile X coordinate"""
        import math
        return int((lng + 180) / 360 * (2 ** zoom))
