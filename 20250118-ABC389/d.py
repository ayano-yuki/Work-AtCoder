def count_squares(R):
    count = 0
    R_squared = R * R

    for i in range(R + 1):
        for j in range(R + 1):
            xi = i + 0.5
            yi = j + 0.5

            d1_squared = xi**2 + yi**2
            d2_squared = xi**2 + (yi - 1)**2
            d3_squared = (xi - 1)**2 + yi**2
            d4_squared = (xi - 1)**2 + (yi - 1)**2
            
            max_distance_squared = max(d1_squared, d2_squared, d3_squared, d4_squared)
            
            if max_distance_squared <= R_squared:
                if i == 0 and j == 0:
                    count += 1
                elif i == 0 or j == 0:
                    count += 2
                else:
                    count += 4

    return count


R = int(input())

print(count_squares(R))
