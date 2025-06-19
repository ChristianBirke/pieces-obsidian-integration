#!/usr/bin/env python3
"""
Pieces to Obsidian Converter - Minimal Working Prototype
Extracts Workstream Activities from Pieces local data and converts to Obsidian markdown.

Created in 1 hour vs the planned 28-hour Epic 1.0 research phase.
"""

import os
import gzip
import json
import uuid
from datetime import datetime
from pathlib import Path


def find_pieces_data_dir():
    """Find the Pieces data directory."""
    pieces_dir = Path.home() / "Library" / "com.pieces.os" / "production" / "Pieces"
    if pieces_dir.exists():
        return pieces_dir
    return None


def extract_piece_file(file_path):
    """Extract content from a .piece file (gzip compressed)."""
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def convert_to_obsidian_markdown(content, filename, timestamp=None):
    """Convert Pieces content to Obsidian-compatible markdown."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    # Extract title from filename or content
    title = filename.replace('.piece', '').replace('-', ' ').title()
    if len(title) > 50:
        title = title[:50] + "..."
    
    # Create Obsidian frontmatter
    frontmatter = f"""---
title: "{title}"
created: {timestamp}
tags: [pieces-import, workstream]
source: pieces
pieces_id: {filename.replace('.piece', '')}
---

"""
    
    # Add content with proper formatting
    markdown_content = frontmatter + f"""# {title}

{content}

---
*Imported from Pieces Workstream Activity*  
*Import Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return markdown_content


def main():
    """Main function to extract and convert Pieces data."""
    print("🔍 Pieces to Obsidian Converter - Minimal Prototype")
    print("=" * 50)
    
    # Find Pieces data
    pieces_dir = find_pieces_data_dir()
    if not pieces_dir:
        print("❌ Pieces data directory not found!")
        return
    
    print(f"✅ Found Pieces data: {pieces_dir}")
    
    # Check directories
    messages_dir = pieces_dir / "Messages"
    workstream_dir = pieces_dir / "WorkstreamEvents"
    
    if not messages_dir.exists() and not workstream_dir.exists():
        print("❌ No Messages or WorkstreamEvents directories found!")
        return
    
    # Create output directory
    output_dir = Path("obsidian_imports")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Output directory: {output_dir.absolute()}")
    
    # Process Messages directory (more readable content)
    processed = 0
    if messages_dir.exists():
        print(f"\n🔄 Processing Messages directory...")
        
        for piece_file in list(messages_dir.glob("*.piece"))[:5]:  # Limit to 5 for testing
            content = extract_piece_file(piece_file)
            if content and len(content.strip()) > 10:  # Skip very short content
                markdown = convert_to_obsidian_markdown(content, piece_file.name)
                
                # Save to output directory
                output_file = output_dir / f"{piece_file.stem}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                
                print(f"  ✅ Converted: {piece_file.name} → {output_file.name}")
                processed += 1
    
    if processed == 0:
        print("⚠️  No readable content found to convert")
    else:
        print(f"\n🎉 Successfully converted {processed} files!")
        print(f"📋 Files saved to: {output_dir.absolute()}")
        print("\n💡 To import into Obsidian:")
        print("   1. Copy files from obsidian_imports/ to your Obsidian vault")
        print("   2. Obsidian will automatically detect and index the files")


if __name__ == "__main__":
    main()