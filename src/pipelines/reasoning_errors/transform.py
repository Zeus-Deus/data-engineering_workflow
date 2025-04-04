#from extract import get_raw_data
from src.pipelines.reasoning_errors.extract import get_raw_data
import logging
from bs4 import BeautifulSoup
import re
from tabulate import tabulate

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_data(data):
    try:
        # Handle case where data is a list
        if isinstance(data, list):
            logging.info("Raw data is a list; using the first element.")
            if not data:
                logging.error("Received an empty list for raw data.")
                return []
            data = data[0] if isinstance(data[0], (str, bytes)) else str(data[0])
        
        # Ensure data is a string or bytes-like object.
        if not isinstance(data, (str, bytes)):
            logging.error(f"Invalid raw data type: {type(data)}. Expected string or bytes.")
            return []
            
        soup = BeautifulSoup(data, 'html.parser')
        results = []
        current_h2 = None
        current_h3 = None
        current_h4 = None

        content = soup.find("div", class_="mw-parser-output")
        if not content:
            logging.warning("No content found with class 'mw-parser-output'")
            return results

        for elem in content.find_all(['h2', 'h3', 'h4', 'li']):
            if elem.name == 'h2':
                current_h2 = elem.get_text(strip=True)
                current_h3 = None
                current_h4 = None
            elif elem.name == 'h3':
                current_h3 = elem.get_text(strip=True)
                current_h4 = None
            elif elem.name == 'h4':
                current_h4 = elem.get_text(strip=True)
            elif elem.name == 'li':
                a_tag = elem.find('a', title=True)
                bias_name = a_tag.get("title", "").strip() if a_tag else elem.get_text(strip=True)
                if isinstance(bias_name, str) and len(bias_name) > 1 and not re.fullmatch(r'[\W_]+', bias_name):
                    results.append({
                        "bias_name": bias_name,
                        "h4_tag": current_h4,
                        "h3_tag": current_h3,
                        "h2_tag": current_h2
                    })
                else:
                    logging.warning(f"Invalid bias name found: {bias_name}")
        return results
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        return []

if __name__ == "__main__":
    raw_data = get_raw_data()
    transformed_data = transform_data(raw_data)
    
    # Print the first 30 rows of the transformed data in a tabular format
    if transformed_data:
        print(tabulate(transformed_data[:30], headers="keys", tablefmt="psql"))
    else:
        print("No transformed data available.")
    
    logging.info(f"Transformed Data: {transformed_data[:30]}")