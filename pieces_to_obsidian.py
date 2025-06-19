#!/usr/bin/env python3
"""
Pieces to Obsidian Converter - Enhanced with CLI Support
Extracts Workstream Activities from Pieces local data and converts to Obsidian markdown.

Originally created in 1 hour vs the planned 28-hour Epic 1.0 research phase.
Enhanced with Epic 4.0 simplified improvements.
"""

import argparse
import os
import gzip
import json
import uuid
import sys
from datetime import datetime
from pathlib import Path

# Try to import PyYAML for config file support (optional)
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def find_pieces_data_dir(custom_path=None):
    """Find the Pieces data directory."""
    if custom_path:
        custom_pieces_dir = Path(custom_path)
        if custom_pieces_dir.exists():
            return custom_pieces_dir
        else:
            print(f"❌ Custom Pieces directory not found: {custom_path}")
            return None
    
    # Default macOS location
    pieces_dir = Path.home() / "Library" / "com.pieces.os" / "production" / "Pieces"
    if pieces_dir.exists():
        return pieces_dir
    
    # TODO: Add Windows/Linux paths in future
    print("❌ Pieces data directory not found!")
    print("💡 Try specifying custom path with --pieces-dir")
    return None


def extract_piece_file(file_path):
    """Extract content from a .piece file (gzip compressed)."""
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def extract_title_from_content(content, filename):
    """Extract a meaningful title from content."""
    # Try to find the first meaningful line
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 5 and not line.startswith('#'):
            # Take first 50 chars as title
            title = line[:50]
            if len(line) > 50:
                title += "..."
            return title
    
    # Fallback to filename-based title
    title = filename.replace('.piece', '').replace('-', ' ').title()
    if len(title) > 50:
        title = title[:50] + "..."
    return title


def convert_to_obsidian_markdown(content, filename, timestamp=None):
    """Convert Pieces content to Obsidian-compatible markdown."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    # Extract title from content
    title = extract_title_from_content(content, filename)
    
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


def load_config(config_file='config.yaml'):
    """Load configuration from YAML file if available."""
    config = {}
    
    if not HAS_YAML:
        return config
    
    config_path = Path(config_file)
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"⚠️  Warning: Could not load config file {config_file}: {e}")
    
    return config


def parse_args():
    """Parse command line arguments."""
    # Load config file first
    config = load_config()
    
    parser = argparse.ArgumentParser(
        description="Convert Pieces Workstream Activities to Obsidian markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 pieces_to_obsidian.py                          # Use defaults
  python3 pieces_to_obsidian.py --limit 20               # Convert up to 20 files
  python3 pieces_to_obsidian.py --output ~/MyVault       # Custom output directory
  python3 pieces_to_obsidian.py --pieces-dir /custom/path # Custom Pieces directory
  python3 pieces_to_obsidian.py --min-length 50          # Skip short content
  python3 pieces_to_obsidian.py --config custom.yaml     # Use custom config file
        """
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)',
        metavar='FILE'
    )
    
    parser.add_argument(
        '--pieces-dir',
        default=config.get('pieces_dir'),
        help='Path to Pieces data directory (default: auto-detect)',
        metavar='PATH'
    )
    
    parser.add_argument(
        '--output', '-o',
        default=config.get('output', 'obsidian_imports'),
        help='Output directory for converted files (default: obsidian_imports)',
        metavar='PATH'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=config.get('limit'),
        help='Maximum number of files to process (default: process all)',
        metavar='N'
    )
    
    parser.add_argument(
        '--min-length',
        type=int,
        default=config.get('min_length', 10),
        help='Minimum content length to process (default: 10)',
        metavar='N'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        default=config.get('quiet', False),
        help='Reduce output verbosity'
    )
    
    return parser.parse_args()


def main():
    """Main function to extract and convert Pieces data."""
    args = parse_args()
    
    if not args.quiet:
        print("🔍 Pieces to Obsidian Converter - Enhanced Edition")
        print("=" * 55)
    
    # Find Pieces data
    pieces_dir = find_pieces_data_dir(args.pieces_dir)
    if not pieces_dir:
        sys.exit(1)
    
    if not args.quiet:
        print(f"✅ Found Pieces data: {pieces_dir}")
    
    # Check directories
    messages_dir = pieces_dir / "Messages"
    workstream_dir = pieces_dir / "WorkstreamEvents"
    
    if not messages_dir.exists() and not workstream_dir.exists():
        print("❌ No Messages or WorkstreamEvents directories found!")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    if not args.quiet:
        print(f"📁 Output directory: {output_dir.absolute()}")
    
    # Process Messages directory (more readable content)
    processed = 0
    skipped = 0
    
    if messages_dir.exists():
        if not args.quiet:
            print(f"\n🔄 Processing Messages directory...")
        
        piece_files = list(messages_dir.glob("*.piece"))
        if args.limit:
            piece_files = piece_files[:args.limit]
            
        for piece_file in piece_files:
            content = extract_piece_file(piece_file)
            if content and len(content.strip()) >= args.min_length:
                markdown = convert_to_obsidian_markdown(content, piece_file.name)
                
                # Save to output directory
                output_file = output_dir / f"{piece_file.stem}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                
                if not args.quiet:
                    print(f"  ✅ Converted: {piece_file.name} → {output_file.name}")
                processed += 1
            else:
                skipped += 1
    
    # Print summary
    if processed == 0:
        print("⚠️  No files converted")
    else:
        print(f"\n🎉 Successfully converted {processed} files!")
        if skipped > 0:
            print(f"⏭️  Skipped {skipped} files (too short or unreadable)")
        print(f"📋 Files saved to: {output_dir.absolute()}")
        
        if not args.quiet:
            print("\n💡 To import into Obsidian:")
            print("   1. Copy files from output directory to your Obsidian vault")
            print("   2. Obsidian will automatically detect and index the files")


if __name__ == "__main__":
    main()