
# Engineering Project: **Block Sorting Robotic System**

## Project Title: **Block Sorting Robotic System**

### Author: Jakub Pajak

### Date: 10.2024 - 01.2025

---

## Project Overview

This project focuses on building a robotic system designed for **sorting blocks**. The robot's primary functionality is to transport blocks using a **gripper** from a starting position to a designated location. The destination is determined based on a pre-programmed path.

The robot utilizes **image processing** for visual analysis, which allows it to select the appropriate path based on the current block's color. After placing the block in the target location, the robot returns to the starting station and repeats the process.

---

## Technology Stack

- **Hardware**:
  - **Raspberry Pi**
  - **Arduino UNO R3**
  
- **Programming Languages**:
  - **Python**
  - **C/C++**

---

## Functional Overview

1. **Block Pickup and Transport**:
   - The robot uses a **gripper** to pick up blocks from the starting station and transport them to the designated location.

2. **Path Selection**:
   - The robot employs **image processing** to analyze the block's color and determines the path accordingly.

3. **Block Placement**:
   - After selecting the path, the robot places the block at the target location.

4. **Return Process**:
   - Once the block is placed, the robot returns to the starting station and repeats the process for the next block.
