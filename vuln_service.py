#!/usr/bin/env python3
"""
Vulnerable File Processing Service - Target
Running on Kali VM with limited resources
"""

from flask import Flask, request, jsonify, send_file
import zipfile
import os
import tempfile
import psutil
import threading
import time
import shutil
from datetime import datetime

app = Flask(__name__)

# Global stats
stats = {
    'total_uploads': 0,
    'total_bytes_processed': 0,
    'attacks_detected': 0,
    'start_time': datetime.now()
}

def monitor_resources():
    log_file = 'resource_usage.log'
    
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"{timestamp} | CPU: {cpu:5.1f}% | Memory: {memory.percent:5.1f}% | Disk: {disk.percent:5.1f}%\n"
        
        # Log to file
        with open(log_file, 'a') as f:
            f.write(log_line)
        
        if cpu > 80 or memory.percent > 80:
            print(f"\033[91m{log_line.strip()}\033[0m")  # Red for high load
        elif cpu > 50 or memory.percent > 50:
            print(f"\033[93m{log_line.strip()}\033[0m")  # Yellow for medium load
        else:
            print(f"\033[92m{log_line.strip()}\033[0m")  # Green for normal
        
        time.sleep(2)

@app.route('/', methods=['GET'])
def index():
    uptime = (datetime.now() - stats['start_time']).total_seconds()
    
    return jsonify({
        'service': 'Vulnerable File Processing Service',
        'status': 'online',
        'version': '1.0.0',
        'uptime_seconds': uptime,
        'total_uploads': stats['total_uploads'],
        'total_bytes_processed': stats['total_bytes_processed'],
        'attacks_detected': stats['attacks_detected'],
        'endpoints': {
            'upload': '/upload (POST)',
            'status': '/status (GET)',
            'logs': '/logs (GET)',
            'stats': '/stats (GET)'
        }
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    VULNERABLE file upload endpoint
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    stats['total_uploads'] += 1
    
    try:
        temp_dir = tempfile.mkdtemp(prefix='upload_')
        filepath = os.path.join(temp_dir, file.filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        stats['total_bytes_processed'] += file_size
        
        print(f"\n{'='*70}")
        print(f"[{datetime.now()}] NEW UPLOAD")
        print(f"File: {file.filename}")
        print(f"Size: {file_size / (1024*1024):.2f} MB")
        print(f"From: {request.remote_addr}")
        print(f"{'='*70}")
        
        if file.filename.endswith('.zip'):
            extract_dir = os.path.join(temp_dir, 'extracted')
            os.makedirs(extract_dir, exist_ok=True)
            
            print(f"[*] Beginning extraction...")
            start_time = time.time()
            
            # No size checks, no file count limits, no ratio checks
            try:
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    file_count = len(file_list)
                    
                    if file_count > 1000:
                        stats['attacks_detected'] += 1
                        print(f"[!] WARNING: Large file count detected: {file_count}")
                    
                    # Extract anyway
                    zip_ref.extractall(extract_dir)
                
                end_time = time.time()
                extraction_time = end_time - start_time
                
                # Calculate extracted size
                total_extracted = 0
                extracted_files = 0
                for root, dirs, files in os.walk(extract_dir):
                    for f in files:
                        fp = os.path.join(root, f)
                        if os.path.exists(fp):
                            total_extracted += os.path.getsize(fp)
                            extracted_files += 1
                
                expansion_ratio = total_extracted / file_size if file_size > 0 else 0
                
                print(f"[+] Extraction complete!")
                print(f"    Files extracted: {extracted_files:,}")
                print(f"    Total size: {total_extracted / (1024**3):.2f} GB")
                print(f"    Expansion ratio: {expansion_ratio:.1f}x")
                print(f"    Time taken: {extraction_time:.2f}s")
                
                # Cleanup
                shutil.rmtree(temp_dir)
                
                return jsonify({
                    'status': 'success',
                    'filename': file.filename,
                    'compressed_size_mb': file_size / (1024**2),
                    'files_extracted': extracted_files,
                    'total_size_gb': total_extracted / (1024**3),
                    'expansion_ratio': expansion_ratio,
                    'extraction_time': extraction_time,
                    'warning': 'Potential bomb detected' if expansion_ratio > 100 else None
                })
                
            except zipfile.BadZipFile:
                return jsonify({'error': 'Invalid ZIP file'}), 400
            
            except Exception as e:
                error_msg = str(e)
                print(f"[!!!] EXTRACTION FAILED: {error_msg}")
                
                return jsonify({
                    'status': 'dos_achieved',
                    'error': error_msg,
                    'message': 'Service overwhelmed - DOS successful'
                }), 507
        
        else:
            return jsonify({'error': 'Only ZIP files supported'}), 400
    
    except MemoryError:
        print(f"[!!!] MEMORY EXHAUSTED!")
        return jsonify({
            'status': 'dos_achieved',
            'error': 'Memory exhaustion',
            'message': 'DOS successful'
        }), 507
    
    except Exception as e:
        print(f"[!!!] CRITICAL ERROR: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/status', methods=['GET'])
def status():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': cpu,
        'memory_percent': memory.percent,
        'memory_available_mb': memory.available / (1024**2),
        'disk_percent': disk.percent,
        'disk_free_gb': disk.free / (1024**3),
        'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
    })

@app.route('/logs', methods=['GET'])
def logs():
    try:
        with open('resource_usage.log', 'r') as f:
            logs = f.readlines()[-100:]
        return jsonify({'logs': logs})
    except FileNotFoundError:
        return jsonify({'logs': []})

@app.route('/stats', methods=['GET'])
def get_stats():
    uptime = (datetime.now() - stats['start_time']).total_seconds()
    
    return jsonify({
        'uptime_seconds': uptime,
        'total_uploads': stats['total_uploads'],
        'total_bytes_processed': stats['total_bytes_processed'],
        'total_gb_processed': stats['total_bytes_processed'] / (1024**3),
        'attacks_detected': stats['attacks_detected'],
        'current_cpu': psutil.cpu_percent(interval=0.5),
        'current_memory': psutil.virtual_memory().percent
    })

if __name__ == '__main__':
    print("="*70)
    print("VULNERABLE FILE PROCESSING SERVICE")
    print("="*70)
    print(f"Starting time: {stats['start_time']}")
    print(f"Host: 0.0.0.0")
    print(f"Port: 5000")
    print()
    print("[!] WARNING: This service is intentionally vulnerable")
    print("[!] For educational/testing purposes only")
    print("[!] Do not expose to public networks")
    print("="*70)
    print()
    
    monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
    monitor_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)