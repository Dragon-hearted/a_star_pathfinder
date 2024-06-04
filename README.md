# A* Pathfinder Algorithm

This project implements the A* Pathfinding Algorithm using Pygame to visualize the shortest path between two points on a grid. The user can create a grid, set start and end points, add barriers, and watch the algorithm find the shortest path.

## Features

- Visual representation of the A* Pathfinding Algorithm.
- Interactive grid creation.
- Start and end point selection.
- Barrier placement.
- Path visualization.
- Options to restart and quit the visualization.

## Installation and Setup

### Requirements

- Python 3.7 or higher
- Pygame

### Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Dragon-hearted/a_star_pathfinder.git
    cd a_star_pathfinder
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the Required Packages**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Program**
    ```bash
    python main.py
    ```

## Usage Instructions

1. **Start the Program**: Run the `main.py` script to start the visualization.
2. **Instructions Page**: Read through the instructions displayed on the screen.
3. **Start the Visualization**:
    - Left-click to add the start node (orange).
    - Left-click again to add the end node (turquoise).
    - Continue left-clicking to add barrier nodes (black).
    - Right-click to remove nodes.
    - Press `Space` to start the algorithm.
    - Press `R` to reset the grid.
4. **Path Visualization**: Watch as the A* algorithm finds the shortest path.
5. **Restart or Quit**: After the path is found, use the Restart and Quit buttons to either start over or exit the application.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

MIT License

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

Feel free to customize the repository link and other details as per your project specifics.