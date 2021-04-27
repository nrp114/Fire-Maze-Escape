# Fire-Maze-Escape

To create a maze with a given dimension and obstacle density p, we created a method where we take two arguments i.e., dim and p. Then, we created a list, and we append “dim” lists inside it of size “dim” making it a dim * dim maze. However, while creating the inner list, we randomly generate a number between 0 and 1, if it is less than or equal to “p” we add 1 (obstacle) else 0 (normal path) in that inner list.

Imporved AI agent uses A* algorithm to find its way through fire maze.

"A* Explanation": To search a path in the maze using A* algorithm, we used min heap as a fringe. 
Initially, the min heap is going have one element in it i.e., the struct (class) a_node containing the position (0, 0), 0 as an actual cost, no parent and heuristic value.
We start the A* algorithm. Firstly, we pop the element from the min heap with the minimum heuristic value and append all its neighbor’s a_node(s) with the updated actual and
heuristic value. To avoid adding the same position a_node again and again in the queue, we used the visited boolean to keep track of the positions that are already in the min heap 
and update that a_node if there is any improvement in the actual cost. Then, we repeat this process till we reach the destination, or all the possible positions are visited and 
there is no path to reach the destination. Once the destination is reached, we backtrack the path using the parent stored in the struct (class) a_node and return the grid with 
the path between start and end position.


**NOTE: Red color boxes are the open path and white color boxes are the obstacles.**

Video to demonstrate the working or Basic agents vs Improved Agents : - https://youtu.be/EnwLSRm0tdA


[![...](https://i9.ytimg.com/vi_webp/EnwLSRm0tdA/mqdefault.webp?time=1619551800000&sqp=CLjMoYQG&rs=AOn4CLB_UW40kBQoJ4sYOt6G2uCQqWdBxA)](https://youtu.be/EnwLSRm0tdA)
