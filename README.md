# Reuse Distance Analysis

This project aims to analyze reuse distance in memory traces to optimize cache architectures. The goal is to understand application behavior and select appropriate caching policies for improved performance.

## Project Overview

The reuse distance is a critical metric for determining data locality. It measures the number of distinct memory accesses between two consecutive accesses to the same memory address. In this project, we implement an efficient algorithm to compute the average reuse distance with a time complexity of O(nlogn) and space complexity of O(n).

## Implementation

The core implementation is provided in Python and involves processing memory trace files to compute various reuse distance statistics.

### Components

1. **TreeNode and Tree Classes**:
   - Implemented to maintain a balanced binary search tree (AVL tree). Nodes store information about content, left and right children, parent, height, and subtree size.
   - The `Tree` class includes methods for inserting and deleting nodes, updating sizes and heights, balancing the tree, and calculating the rank of nodes.

2. **Reuse Distance Calculation**:
   - The `calculate_reuse_distance` function processes a trace file, updates the tree structure, and calculates reuse distances for each memory address access.
   - Results include average, minimum, maximum, variance, median reuse distances, and counts of reuse distances within specific ranges.

3. **Output Generation**:
   - Functions like `convert_list_to_output` and `update_reuse_distance` process reuse distance data to generate required statistics.
   - The `add_to_output` function writes results to an output CSV file.

### Trace File Format

Trace files used in this project adhere to the following format:

Time Stamp(ns), Response Time(ns), Offset(Byte), Request Size (Byte), Request Type(Read/Write), Process ID, Major Disk Number, Minor Disk Number


## Usage

To run the code, ensure you have the required trace files in the correct format. The script processes these files and generates an output CSV file with reuse distance statistics.

### Running the Script

1. Clone the repository:

git clone <your-repo-url>
cd <your-repo-directory>

2. Ensure the trace files are in the working directory.

3. Run the script:

python main.py


### Example Output

The output CSV file will contain columns for:

- Trace File Name
- Average Reuse Distance
- Minimum Reuse Distance
- Maximum Reuse Distance
- Variance
- Median
- Count of Reuse Distances in Various Ranges (0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1.0K, 2.0K, 4.0K, 8.0K, 16.0K, 32.0K, 64.0K, 128.0K, 256.0K, 512.0K, >512K)

## Additional Features

For additional points or improvements, consider:

1. Adding computations for mode, maximum, and minimum reuse distances.
2. Implementing the Useful Reuse Distance algorithm described in the ECI-Cache paper.

## References

- [Data Structures and Algorithms for Calculating Reuse Distance](#)
- Ahmadian, Saba, Onur Mutlu, and Hossein Asadi. "ECI-Cache: A high-endurance and cost-efficient I/O caching scheme for virtualized platforms." Proceedings of the ACM on Measurement and Analysis of Computing Systems 2, no. 1 (2018): 1-34.
