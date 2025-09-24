"""
Example of well-written Python code with minimal issues
"""

import logging
import numpy as np
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_statistics(numbers: List[float]) -> dict:
    """
    Calculate basic statistics for a list of numbers.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        Dictionary containing mean, median, and std deviation
    """
    if not numbers:
        logger.warning("Empty list provided to calculate_statistics")
        return {}
    
    arr = np.array(numbers)
    
    stats = {
        'mean': float(np.mean(arr)),
        'median': float(np.median(arr)),
        'std': float(np.std(arr)),
        'count': len(numbers)
    }
    
    logger.info(f"Calculated statistics for {len(numbers)} values")
    return stats


class DataAnalyzer:
    """A simple data analyzer class."""
    
    def __init__(self, data: Optional[List[float]] = None):
        """Initialize the analyzer with optional data."""
        self.data = data or []
        logger.info("DataAnalyzer initialized")
    
    def add_data(self, values: List[float]) -> None:
        """Add new data points."""
        self.data.extend(values)
        logger.info(f"Added {len(values)} data points")
    
    def get_summary(self) -> dict:
        """Get statistical summary of the data."""
        return calculate_statistics(self.data)


if __name__ == "__main__":
    # Example usage
    analyzer = DataAnalyzer([1.0, 2.0, 3.0, 4.0, 5.0])
    summary = analyzer.get_summary()
    logger.info(f"Data summary: {summary}")