import requests
from bs4 import BeautifulSoup

def main():
    # Ask user to enter the published Google Doc URL
    doc_url = input("Enter the Google Doc URL: ").strip()
    
    # Fetch the HTML from the provided URL
    try:
        response = requests.get(doc_url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching the URL: {e}")
        return
    
    html = response.text
    
    # Parse the HTML and find the table
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No <table> found in the document.")
        return
    
    # Parse each row, extracting x, character, and y
    coords = []
    rows = table.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 3:
            # Possibly a header or incomplete row
            continue
        
        x_str = cells[0].get_text(strip=True)
        ch    = cells[1].get_text(strip=True)
        y_str = cells[2].get_text(strip=True)
        
        # Convert x_str, y_str into integers if possible
        try:
            x = int(x_str)
            y = int(y_str)
        except ValueError:
            # If they're not integers, skip
            continue
        
        coords.append((x, y, ch))
    
    if not coords:
        print("No valid coordinate data found in the table.")
        return
    
    # Determine grid size
    max_x = max(c[0] for c in coords)
    max_y = max(c[1] for c in coords)
    
    # Create a grid filled with spaces
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Place each character into the grid
    for (x, y, ch) in coords:
        grid[y][x] = ch
    
    # Print each row of the grid
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    main()
