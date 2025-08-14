import pickle
import gzip
import os

def compress_similarity_matrix():
    print("Loading similarity matrix...")
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    original_size = os.path.getsize('similarity.pkl')
    print(f"Original file size: {original_size / (1024*1024):.2f} MB")
    print("Compressing similarity matrix...")
    with gzip.open('similarity.pkl.gz', 'wb') as f:
        pickle.dump(similarity, f)
    compressed_size = os.path.getsize('similarity.pkl.gz')
    print(f"Compressed file size: {compressed_size / (1024*1024):.2f} MB")
    print(f"Compression ratio: {(1 - compressed_size/original_size) * 100:.1f}% reduction")
    print("Verifying compressed file...")
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity_loaded = pickle.load(f)
    print(f"Original shape: {similarity.shape}")
    print(f"Loaded shape: {similarity_loaded.shape}")
    print("✓ Compression successful!")
    return compressed_size < 100 * 1024 * 1024 

if __name__ == "__main__":
    success = compress_similarity_matrix()