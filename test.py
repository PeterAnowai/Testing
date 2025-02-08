import requests

def decode_document(doc_url):
    # Fetch the document’s text
    response = requests.get(doc_url)
    lines = response.text.splitlines()

    # Collect all parsed (x, y, char) values
    coords = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Expect lines in the form "x, y, CHARACTER"
        parts = [p.strip() for p in line.split(',')]
        if len(parts) != 3:
            # Skip anything not matching our expected format
            continue
        
        x_str, y_str, ch = parts
        x = int(x_str)
        y = int(y_str)
        
        coords.append((x, y, ch))

    if not coords:
        # If nothing was parsed, just return (or print nothing)
        return

    # Find how large our grid needs to be
    max_x = max(pt[0] for pt in coords)
    max_y = max(pt[1] for pt in coords)

    # Create a 2D grid filled with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place each character in the appropriate location
    for (x, y, ch) in coords:
        grid[y][x] = ch

    # Print row by row
    for row in grid:
        print(''.join(row))
