import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse

def scrape_hotels(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Create a BeautifulSoup object with the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all hotel listings on the page
        hotel_listings = soup.find_all('div', class_='oyo-row')
        
        # Initialize lists to store the extracted data
        hotel_names = []
        hotel_prices = []
        hotel_ratings = []
        
        # Extract data from each hotel listing
        for listing in hotel_listings:
            # Extract hotel name
            hotel_name = listing.find('h3', class_='listingHotelDescription__hotelName').text.strip()
            
            # Extract hotel price
            hotel_price = listing.find('span', class_='listingPrice__finalPrice').text.strip()
            
            # Extract hotel rating
            hotel_rating = listing.find('span', class_='hotelRating__rating').text.strip()
            
            # Append the extracted data to the respective lists
            hotel_names.append(hotel_name)
            hotel_prices.append(hotel_price)
            hotel_ratings.append(hotel_rating)
        
        # Create a pandas DataFrame with the extracted data
        data = {
            'Hotel Name': hotel_names,
            'Price': hotel_prices,
            'Rating': hotel_ratings
        }
        df = pd.DataFrame(data)
        
        # Return the DataFrame
        return df
    else:
        print("Error: Failed to retrieve the webpage.")
        return None

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Web scraping for hotel data')
    parser.add_argument('url', type=str, help='URL of the hotel website')
    parser.add_argument('-o', '--output', type=str, help='Output file path')
    args = parser.parse_args()

    # Scrape hotels data
    df = scrape_hotels(args.url)

    if df is not None:
        # Print the DataFrame
        print(df)
        
        # Save the DataFrame to a CSV file if output path is provided
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"Data saved to {args.output}")

if __name__ == '__main__':
    main()
