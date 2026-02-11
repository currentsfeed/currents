#!/usr/bin/env python3
"""
BRain + Rain Service Manager
Manages both the main BRain app (port 5555) and Rain API (port 5001)
"""
import subprocess
import sys
import time
import os
import signal

def start_services():
    """Start both Rain API and BRain app"""
    processes = []
    
    print("🌧️  Starting Rain API (port 5001)...")
    rain_process = subprocess.Popen(
        ['python3', 'rain_api_standalone.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(('Rain API', rain_process))
    time.sleep(2)
    
    # Check if Rain API started
    if rain_process.poll() is not None:
        print("❌ Rain API failed to start")
        return False
    
    print("✅ Rain API started on port 5001")
    
    print("\n🧠 Starting BRain app (port 5555)...")
    brain_process = subprocess.Popen(
        ['python3', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(('BRain App', brain_process))
    time.sleep(2)
    
    # Check if BRain started
    if brain_process.poll() is not None:
        print("❌ BRain app failed to start")
        rain_process.terminate()
        return False
    
    print("✅ BRain app started on port 5555")
    
    print("\n" + "="*60)
    print("✅ ALL SERVICES RUNNING")
    print("="*60)
    print("🌧️  Rain API:    http://localhost:5001")
    print("🧠 BRain App:   http://localhost:5555")
    print("="*60)
    print("\nPress Ctrl+C to stop all services")
    
    # Wait for Ctrl+C
    try:
        while True:
            time.sleep(1)
            # Check if any process died
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"\n❌ {name} stopped unexpectedly!")
                    stop_all(processes)
                    return False
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...")
        stop_all(processes)
        print("✅ All services stopped")
        return True

def stop_all(processes):
    """Stop all processes"""
    for name, proc in processes:
        if proc.poll() is None:
            print(f"   Stopping {name}...")
            proc.terminate()
            proc.wait(timeout=5)

def check_status():
    """Check if services are running"""
    import requests
    
    print("Checking service status...\n")
    
    # Check Rain API
    try:
        response = requests.get('http://localhost:5001/health', timeout=2)
        if response.status_code == 200:
            print("✅ Rain API: Running (port 5001)")
        else:
            print("⚠️  Rain API: Unhealthy")
    except:
        print("❌ Rain API: Not running")
    
    # Check BRain App
    try:
        response = requests.get('http://localhost:5555/health', timeout=2)
        if response.status_code == 200:
            print("✅ BRain App: Running (port 5555)")
        else:
            print("⚠️  BRain App: Unhealthy")
    except:
        print("❌ BRain App: Not running")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        check_status()
    else:
        start_services()
