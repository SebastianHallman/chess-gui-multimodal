def coords_to_tuples(coords):
  if len(coords) != 4:
    return
  
  n = 2

  squares = [coords[i:i+n] for i in range(0, len(coords), n)]

  tuples_for_output = []

  for square in squares:
    tuples_for_output.append((ord(square[0]) - 97, int(square[1]) - 1))

  return tuples_for_output                          
