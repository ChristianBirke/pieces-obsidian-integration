#!/usr/bin/env python3
"""
Automated Pieces Workstream Activity Monitor
Monitors for new .piece files and automatically processes them with PARA framework.
"""

import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys

class PiecesWorkstreamHandler(FileSystemEventHandler):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.script_dir = Path(__file__).parent
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        if event.src_path.endswith('.piece'):
            print(f"🔍 New workstream activity detected: {event.src_path}")
            
            # Wait a moment for file to be fully written
            time.sleep(2)
            
            # Process the new file
            try:
                result = subprocess.run([
                    sys.executable,
                    str(self.script_dir / "enhanced_para_renamer.py"),
                    str(Path(event.src_path).parent),
                    "--single-file",
                    Path(event.src_path).name,
                    "--output",
                    self.output_dir
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Successfully processed new workstream activity")
                else:
                    print(f"❌ Error processing workstream activity: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Error running processor: {e}")

def main():
    # Configuration
    pieces_dir = Path("/Users/christianbirke/Library/com.pieces.os/production/Pieces")
    output_dir = Path("obsidian_imports")
    
    # Watch both Messages and WorkstreamEvents directories
    watch_dirs = [
        pieces_dir / "Messages",
        pieces_dir / "WorkstreamEvents"
    ]
    
    event_handler = PiecesWorkstreamHandler(str(output_dir))
    observer = Observer()
    
    for watch_dir in watch_dirs:
        if watch_dir.exists():
            observer.schedule(event_handler, str(watch_dir), recursive=False)
            print(f"📁 Monitoring {watch_dir} for new workstream activities...")
    
    observer.start()
    
    try:
        print("🚀 Automated Pieces Workstream Monitor started!")
        print("Press Ctrl+C to stop monitoring")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Monitoring stopped")
    
    observer.join()

if __name__ == "__main__":
    main()
