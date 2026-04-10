# AI TASK NO 8
# Min-Max Algorithm 

def minmax(depth,node_index, is_max, values):

    if depth == 0:
        return values[node_index]
    
    if is_max:
        best = -999

        for i in range(2):
            val = minmax(depth -1, node_index *2 + i,False, values )
            best = max(best,val)

        return best
    else:
        best = 999

        for i in range(2):
            val =minmax(depth -1, node_index * 2 + i, True ,values)
            best = min(best,val)

        return best 

values = [3,2,3,7,6,5,68,4]

depth = 3 
result = minmax(depth, 0 , True, values)

print("best values is:", result)