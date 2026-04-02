"""
API Key Validation Test Module

This module tests whether all API keys used in the project are:
- Loaded (available in settings)
- Valid (can authenticate)
- Functional (can make requests)
"""

import sys
import os
from pathlib import Path
from typing import Dict, Tuple

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIKeyTester:
    """Test suite for API key validation."""
    
    def __init__(self):
        self.results: Dict[str, Dict[str, str]] = {}
    
    def test_gemini_api_key(self) -> Tuple[str, str]:
        """
        Test Gemini API key:
        1. Check if key is loaded
        2. Check if key can authenticate
        3. Check if API calls work
        """
        test_name = "Gemini API"
        try:
            logger.info(f"Testing {test_name}...")
            
            # Step 1: Check if key is loaded
            if not settings.gemini_api_key:
                logger.warning(f"{test_name}: Key not loaded")
                return "FAILED", "API key not found in settings"
            
            logger.info(f"{test_name}: Key loaded successfully")
            
            # Step 2: Configure and test API
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.gemini_api_key)
                
                # Step 3: Try to generate content (minimal test)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content("Say 'test' and nothing else.")
                
                if response.text and len(response.text.strip()) > 0:
                    logger.info(f"{test_name}: Successfully generated content")
                    return "SUCCESS", "API key is valid and working"
                else:
                    logger.error(f"{test_name}: Empty response from API")
                    return "FAILED", "API returned empty response"
                    
            except Exception as e:
                error_msg = str(e)
                if "401" in error_msg or "authentication" in error_msg.lower():
                    logger.error(f"{test_name}: Authentication failed")
                    return "FAILED", "API key authentication failed (401)"
                elif "403" in error_msg or "permission" in error_msg.lower():
                    logger.error(f"{test_name}: Permission denied")
                    return "FAILED", "API key has no permission (403)"
                else:
                    logger.error(f"{test_name}: API request failed: {error_msg}")
                    return "FAILED", f"API request failed: {error_msg}"
                    
        except Exception as e:
            logger.error(f"{test_name}: Unexpected error: {str(e)}")
            return "FAILED", f"Unexpected error: {str(e)}"
    
    def test_huggingface_api_key(self) -> Tuple[str, str]:
        """
        Test Hugging Face API key:
        1. Check if key is loaded
        2. Check if key can authenticate
        3. Check if API calls work
        """
        test_name = "Hugging Face API"
        try:
            logger.info(f"Testing {test_name}...")
            
            # Step 1: Check if key is loaded
            if not settings.huggingface_api_key:
                logger.warning(f"{test_name}: Key not loaded")
                return "FAILED", "API key not found in settings"
            
            logger.info(f"{test_name}: Key loaded successfully")
            
            # Step 2: Test API authentication with minimal request
            try:
                import requests
                
                # Use a minimal API endpoint to test authentication
                url = "https://huggingface.co/api/whoami"
                headers = {"Authorization": f"Bearer {settings.huggingface_api_key}"}
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    logger.info(f"{test_name}: Successfully authenticated")
                    return "SUCCESS", "API key is valid and working"
                elif response.status_code == 401:
                    logger.error(f"{test_name}: Authentication failed (401)")
                    return "FAILED", "API key authentication failed (401)"
                elif response.status_code == 403:
                    logger.error(f"{test_name}: Permission denied (403)")
                    return "FAILED", "API key has no permission (403)"
                else:
                    logger.error(f"{test_name}: Unexpected status code {response.status_code}")
                    return "FAILED", f"Unexpected response: {response.status_code}"
                    
            except requests.exceptions.Timeout:
                logger.error(f"{test_name}: Request timeout")
                return "FAILED", "Request timeout - check network connectivity"
            except requests.exceptions.ConnectionError:
                logger.error(f"{test_name}: Connection error")
                return "FAILED", "Connection error - check network connectivity"
            except Exception as e:
                logger.error(f"{test_name}: API request failed: {str(e)}")
                return "FAILED", f"API request failed: {str(e)}"
                    
        except Exception as e:
            logger.error(f"{test_name}: Unexpected error: {str(e)}")
            return "FAILED", f"Unexpected error: {str(e)}"
    
    def test_all_api_keys(self) -> Dict[str, Dict[str, str]]:
        """Run all API key tests and return results."""
        logger.info("=" * 60)
        logger.info("Starting API Key Validation Tests")
        logger.info("=" * 60)
        
        # Test Gemini
        status, message = self.test_gemini_api_key()
        self.results["gemini"] = {
            "status": status,
            "message": message
        }
        
        # Test Hugging Face
        status, message = self.test_huggingface_api_key()
        self.results["huggingface"] = {
            "status": status,
            "message": message
        }
        
        return self.results
    
    def print_results(self) -> None:
        """Print test results in a formatted way."""
        logger.info("=" * 60)
        logger.info("API Key Validation Results")
        logger.info("=" * 60)
        
        all_passed = True
        for api_name, result in self.results.items():
            status = result["status"]
            message = result["message"]
            
            icon = "✓" if status == "SUCCESS" else "✗"
            logger.info(f"{icon} {api_name.upper()}: {status}")
            logger.info(f"  Message: {message}")
            
            if status != "SUCCESS":
                all_passed = False
        
        logger.info("=" * 60)
        if all_passed:
            logger.info("✓ All API keys are valid and working!")
        else:
            logger.warning("✗ Some API keys have issues. Check the messages above.")
        logger.info("=" * 60)
        
        return all_passed


def main():
    """Main entry point for API key testing."""
    tester = APIKeyTester()
    tester.test_all_api_keys()
    all_passed = tester.print_results()
    
    # Exit with appropriate code for CI/CD
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
