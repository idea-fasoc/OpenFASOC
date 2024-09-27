# x by y array of elements (e.g. fet, mimcap, or via)
create a x by y array of elements is a common request. 
NOTE, An array is NOT itself a single component that can be placed. You MUST MANUALLY place each element in the array.
To fulfill this request, you must place the element (a component) several times into a matrix. Arrays require placing the same component many times into a matrix like structure. The single component which is placed many times (also called the array element) is typically included in the designers request. Arrays are typically described by their dimensions (rows by columns). The dimensions are NOT a parameter and are hard coded. Dimensions should NOT be confused with single element parameters (which should be same for all elements in the array).
## place
when placing elements of an array, always multiply rows by columns to get number of elements in the array. Name the placed components by their element index (start with element1, then element2, and so on).
## move
move the other elements in the first row to the right of element1
move each element in the second row above the first row, and move the other elements in the second row to the right of the leftmost element in the second row
continue this until all rows are moved into position.
## Routing
routing depends on the component in the array, but route from the first element until the last element, routing each element to the elements which are nearest to it.