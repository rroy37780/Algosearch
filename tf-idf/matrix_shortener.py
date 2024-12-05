import zlib

input_file = 'tfidf_matrix.txt'
output_file = 'tfidf_compressed.zlib'

with open(input_file, 'rb') as f_in:
    data = f_in.read()
    compressed_data = zlib.compress(data, level=9)

with open(output_file, 'wb') as f_out:
    f_out.write(compressed_data)

print("File compressed successfully.")
