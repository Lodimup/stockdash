def chunkify(arr, n):
    # Calculate the size of each chunk
    chunk_size = len(arr) // n

    # Calculate the number of chunks that will have an extra element
    num_larger_chunks = len(arr) % n

    # Initialize the start and end indices for each chunk
    start = 0
    end = chunk_size

    # Initialize the result array
    result = []

    # Iterate over the chunks
    for i in range(n):
        # If this is a larger chunk, add an extra element
        if i < num_larger_chunks:
            end += 1

        # Add the current chunk to the result array
        result.append(arr[start:end])

        # Update the start and end indices for the next chunk
        start = end
        end += chunk_size

    # Return the result array
    return result