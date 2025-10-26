#!/usr/bin/env python3
"""
Gas Station Finder - Application Launcher
This script helps manage the Flask application
"""

import subprocess
import sys
import time
import requests
import signal
import os

def check_port(port):
    """Check if a port is available"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=1)
        return True
    except:
        return False

def kill_existing_processes():
    """Kill any existing Flask processes"""
    try:
        subprocess.run(["pkill", "-f", "gas_station_finder_web.py"], 
                      capture_output=True, text=True)
        subprocess.run(["pkill", "-f", "flask"], 
                      capture_output=True, text=True)
        print("🧹 Cleaned up existing processes")
    except:
        pass

def start_application():
    """Start the Flask application"""
    print("🚀 Starting Gas Station Finder...")
    
    # Kill existing processes
    kill_existing_processes()
    time.sleep(2)
    
    # Try to start the application
    try:
        print("🌐 Launching web interface...")
        subprocess.run([sys.executable, "gas_station_finder_web.py"])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def show_status():
    """Show application status"""
    ports = [5000, 5001, 5002, 8000, 8080]
    running = False
    
    for port in ports:
        if check_port(port):
            print(f"✅ Application is running on http://localhost:{port}")
            running = True
            break
    
    if not running:
        print("❌ Application is not running")
        print("💡 Run: python3 start_app.py start")

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            start_application()
        elif command == "stop":
            kill_existing_processes()
            print("🛑 Application stopped")
        elif command == "status":
            show_status()
        elif command == "restart":
            kill_existing_processes()
            time.sleep(2)
            start_application()
        else:
            print("❌ Unknown command. Use: start, stop, status, or restart")
    else:
        print("🚗 Gas Station Finder - Application Manager")
        print("=" * 50)
        print("Commands:")
        print("  start    - Start the application")
        print("  stop     - Stop the application")
        print("  status   - Check if running")
        print("  restart  - Restart the application")
        print("")
        print("Examples:")
        print("  python3 start_app.py start")
        print("  python3 start_app.py status")

if __name__ == "__main__":
    main()
