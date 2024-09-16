# x by y array of mimcaps
create a x by y array of mimcaps is a common request. 
NOTE, An array is NOT itself a single component that can be placed. You MUST MANUALLY place each mimcap in the array.
To fulfill this request, you must place the mimcap (a component) several times into a matrix. Arrays require placing the same component many times into a matrix like structure. The single component which is placed many times (also called the array mimcap) is typically included in the designers request. Arrays are typically described by their dimensions (rows by columns). The dimensions are NOT a parameter and are hard coded. Dimensions should NOT be confused with single mimcap parameters (which should be same for all mimcaps in the array).
## place
when placing mimcaps of an array, always multiply rows by columns to get number of mimcaps in the array. Name the placed components by their mimcap index (start with mimcap1, then mimcap2, and so on).
## move
move the mimcaps in the first row to the right of mimcap1
move each mimcap in the second row above the first row, and move the other mimcaps in the second row to the right of the leftmost mimcap in the second row
continue this until all rows are moved into position.

in other words
start by moving the first row into position
then move the second row above first row
and arrange the second row from left to right

## Routing
Only route each mimcap to the mimcaps which are nearest to it.