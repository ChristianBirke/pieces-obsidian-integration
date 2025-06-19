#!/usr/bin/env python3
"""
Enhanced PARA Framework File Renamer with Workstream Activity Name Extraction
Extracts actual workstream activity names from Pieces data and creates automated workflow.
"""

import os
import re
import json
import gzip
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, List, Optional

def extract_workstream_activity_name(pieces_dir: Path, uuid: str) -> Optional[str]:
    """
    Extract the actual workstream activity name from Pieces data.
    Checks both WorkstreamEvents and Messages directories.
    """
    # Check WorkstreamEvents directory first
    workstream_file = pieces_dir / "WorkstreamEvents" / f"{uuid}.piece"
    if workstream_file.exists():
        try:
            with gzip.open(workstream_file, 'rt', encoding='utf-8') as f:
                content = f.read()
                data = json.loads(content)
                
                # Extract activity name from various possible fields
                activity_name = None
                if 'native_ocr' in data and 'appTitle' in data['native_ocr']:
                    app_title = data['native_ocr']['appTitle']
                    if app_title and app_title != "UserNotificationCenter":
                        activity_name = app_title
                
                if 'native_ocr' in data and 'windowTitle' in data['native_ocr']:
                    window_title = data['native_ocr']['windowTitle']
                    if window_title:
                        activity_name = window_title
                
                if 'native_ocr' in data and 'ocrText' in data['native_ocr']:
                    ocr_text = data['native_ocr']['ocrText']
                    if ocr_text:
                        # Extract first meaningful line as activity name
                        lines = ocr_text.split('\\n')
                        for line in lines:
                            line = line.strip().strip('"')
                            if line and len(line) > 5 and len(line) < 100:
                                activity_name = line
                                break
                
                if activity_name:
                    # Clean activity name for filename use
                    clean_name = re.sub(r'[^a-zA-Z0-9\s\-_]', '', activity_name)
                    clean_name = re.sub(r'\s+', '-', clean_name.strip())
                    return clean_name[:50]  # Limit length
                    
        except Exception as e:
            print(f"⚠️  Could not extract workstream activity name for {uuid}: {e}")
    
    # Fallback: Check Messages directory for content-based naming
    messages_file = pieces_dir / "Messages" / f"{uuid}.piece"
    if messages_file.exists():
        try:
            with gzip.open(messages_file, 'rt', encoding='utf-8') as f:
                content = f.read()
                # Extract first meaningful sentence as activity name
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 20 and len(line) < 100:
                        # Clean and use first part as activity name
                        clean_name = re.sub(r'[^a-zA-Z0-9\s\-_]', '', line)
                        clean_name = re.sub(r'\s+', '-', clean_name.strip())
                        words = clean_name.split('-')[:6]  # First 6 words
                        return '-'.join(words)
        except Exception as e:
            print(f"⚠️  Could not extract activity name from messages for {uuid}: {e}")
    
    return None

def analyze_content_for_para(content: str, title: str, activity_name: str = None) -> Tuple[str, str]:
    """
    Analyze content to determine PARA classification and content category.
    Enhanced with activity name context.
    """
    content_lower = content.lower()
    title_lower = title.lower()
    activity_lower = (activity_name or "").lower()
    
    # Combined text for analysis
    combined_text = f"{content_lower} {title_lower} {activity_lower}"
    
    # Project indicators - specific outcomes with deadlines
    project_keywords = ['debug', 'implement', 'fix', 'solve', 'error', 'issue', 'problem', 'troubleshoot', 'task', 'todo']
    
    # Area indicators - ongoing responsibilities 
    area_keywords = ['standard', 'practice', 'convention', 'guideline', 'maintain', 'manage', 'process', 'workflow']
    
    # Resource indicators - reference materials
    resource_keywords = ['analysis', 'comparison', 'guide', 'reference', 'overview', 'technique', 'tool', 'method', 'documentation']
    
    # Archive indicators - completed/personal items
    archive_keywords = ['email', 'delivered-to', 'what was i doing', 'facebook', 'password reset', 'notification']
    
    # Determine content category based on activity name and content
    if any(keyword in combined_text for keyword in ['debug', 'error', 'troubleshoot', 'issue', 'log']):
        content_category = 'debugging'
    elif any(keyword in combined_text for keyword in ['code', 'python', 'function', 'blank lines', 'syntax']):
        content_category = 'code-fix'
    elif any(keyword in combined_text for keyword in ['analysis', 'comparison', 'evaluate', 'model', 'review']):
        content_category = 'analysis'
    elif any(keyword in combined_text for keyword in ['email', 'delivered-to', '@', 'notification']):
        content_category = 'email'
    elif any(keyword in combined_text for keyword in ['meeting', 'discussion', 'conversation']):
        content_category = 'meeting'
    elif any(keyword in combined_text for keyword in ['research', 'learning', 'study', 'tutorial']):
        content_category = 'research'
    elif len(content.strip()) < 50:
        content_category = 'question'
    else:
        content_category = 'general'
    
    # Determine PARA type with enhanced logic
    if any(keyword in combined_text for keyword in archive_keywords) or content_category in ['email', 'question']:
        para_type = 'archive'
    elif any(keyword in combined_text for keyword in project_keywords) or content_category in ['debugging', 'code-fix']:
        para_type = 'project'
    elif any(keyword in combined_text for keyword in area_keywords):
        para_type = 'area'
    elif any(keyword in combined_text for keyword in resource_keywords) or content_category in ['analysis', 'research']:
        para_type = 'resource'
    else:
        # Smart defaults based on content category
        if content_category in ['debugging', 'code-fix']:
            para_type = 'project'
        elif content_category in ['email', 'question']:
            para_type = 'archive'
        elif content_category in ['analysis', 'research', 'meeting']:
            para_type = 'resource'
        else:
            para_type = 'resource'
    
    return para_type, content_category

def generate_descriptive_title_with_activity(content: str, original_title: str, activity_name: str = None) -> str:
    """Generate a descriptive title prioritizing workstream activity name."""
    
    # Priority 1: Use workstream activity name if available and meaningful
    if activity_name and len(activity_name) > 5:
        # Clean and format activity name
        clean_activity = re.sub(r'[^a-zA-Z0-9\s\-]', '', activity_name)
        clean_activity = re.sub(r'\s+', '-', clean_activity.strip().lower())
        if len(clean_activity) > 5:
            return clean_activity[:50]
    
    # Priority 2: Use original title if meaningful
    title = original_title.replace('"', '').strip()
    if title and not title.startswith('The error message') and len(title) > 10:
        words = title.split()[:5]
        clean_words = []
        for word in words:
            clean_word = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
            if clean_word and len(clean_word) > 1:
                clean_words.append(clean_word)
        if clean_words:
            return '-'.join(clean_words[:5])
    
    # Priority 3: Extract from content
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 10 and not line.startswith('#') and not line.startswith('---'):
            words = line.split()[:5]
            clean_words = []
            for word in words:
                clean_word = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
                if clean_word and len(clean_word) > 1:
                    clean_words.append(clean_word)
            if clean_words:
                return '-'.join(clean_words[:5])
    
    return 'untitled-content'

def extract_frontmatter_and_content(file_content: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter and main content from markdown file."""
    if not file_content.startswith('---'):
        return {}, file_content
    
    parts = file_content.split('---', 2)
    if len(parts) < 3:
        return {}, file_content
    
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
        content = parts[2].strip()
        return frontmatter, content
    except yaml.YAMLError:
        return {}, file_content

def update_frontmatter_with_activity(frontmatter: Dict, para_type: str, content_category: str, 
                                   new_title: str, activity_name: str = None) -> Dict:
    """Update frontmatter with PARA classification and workstream activity info."""
    updated = frontmatter.copy()
    
    # Update title with activity name if available
    if activity_name:
        updated['title'] = activity_name.replace('-', ' ').title()
    elif 'title' not in updated or updated['title'].startswith('The error message') or len(updated['title']) < 10:
        updated['title'] = new_title.replace('-', ' ').title()
    
    # Update tags - add PARA hashtag and activity-related tags
    current_tags = updated.get('tags', [])
    if isinstance(current_tags, str):
        current_tags = [current_tags]
    
    # Ensure required tags are present
    required_tags = ['pieces-import', 'workstream', content_category, f'#{para_type}']
    
    # Add activity-related tags if activity name exists
    if activity_name:
        # Extract meaningful words from activity name for tags
        activity_words = re.findall(r'\w+', activity_name.lower())
        for word in activity_words:
            if len(word) > 3 and word not in ['the', 'and', 'for', 'with']:
                required_tags.append(word)
    
    for tag in required_tags:
        if tag not in current_tags:
            current_tags.append(tag)
    
    updated['tags'] = current_tags
    updated['type'] = para_type
    updated['content_category'] = content_category
    
    # Add workstream activity name if available
    if activity_name:
        updated['workstream_activity'] = activity_name
    
    return updated

def create_automated_workflow_script(pieces_dir: Path, output_dir: Path):
    """Create a script for automated workflow monitoring."""
    
    workflow_script = f'''#!/usr/bin/env python3
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
            print(f"🔍 New workstream activity detected: {{event.src_path}}")
            
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
                    print(f"❌ Error processing workstream activity: {{result.stderr}}")
                    
            except Exception as e:
                print(f"❌ Error running processor: {{e}}")

def main():
    # Configuration
    pieces_dir = Path("{pieces_dir}")
    output_dir = Path("{output_dir}")
    
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
            print(f"📁 Monitoring {{watch_dir}} for new workstream activities...")
    
    observer.start()
    
    try:
        print("🚀 Automated Pieces Workstream Monitor started!")
        print("Press Ctrl+C to stop monitoring")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\\n🛑 Monitoring stopped")
    
    observer.join()

if __name__ == "__main__":
    main()
'''
    
    workflow_file = Path(__file__).parent / "pieces_workstream_monitor.py"
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(workflow_script)
    
    # Make executable
    os.chmod(workflow_file, 0o755)
    
    print(f"📋 Created automated workflow script: {workflow_file}")
    return workflow_file

def process_files_enhanced(input_dir: str, pieces_data_dir: str = None):
    """Enhanced processing with workstream activity name extraction."""
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Directory not found: {input_dir}")
        return
    
    # Auto-detect Pieces data directory if not provided
    if not pieces_data_dir:
        pieces_data_dir = Path.home() / "Library" / "com.pieces.os" / "production" / "Pieces"
        if not pieces_data_dir.exists():
            print(f"❌ Pieces data directory not found: {pieces_data_dir}")
            print("💡 Please specify --pieces-data-dir manually")
            return
    else:
        pieces_data_dir = Path(pieces_data_dir)
    
    print(f"🔍 Using Pieces data directory: {pieces_data_dir}")
    
    md_files = list(input_path.glob("*.md"))
    if not md_files:
        print(f"❌ No .md files found in {input_dir}")
        return
    
    print(f"🔍 Found {len(md_files)} .md files to process")
    
    mappings = []
    processed = 0
    
    for file_path in md_files:
        try:
            # Read original file
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Extract frontmatter and content
            frontmatter, content = extract_frontmatter_and_content(file_content)
            
            # Get original UUID from filename or frontmatter
            original_uuid = frontmatter.get('pieces_id', file_path.stem)
            
            # Extract workstream activity name
            activity_name = extract_workstream_activity_name(pieces_data_dir, original_uuid)
            
            # Analyze content for PARA classification
            original_title = frontmatter.get('title', '')
            para_type, content_category = analyze_content_for_para(content, original_title, activity_name)
            
            # Generate descriptive title with activity name priority
            descriptive_title = generate_descriptive_title_with_activity(content, original_title, activity_name)
            
            # Update frontmatter with activity information
            updated_frontmatter = update_frontmatter_with_activity(
                frontmatter, para_type, content_category, descriptive_title, activity_name
            )
            
            # Preserve original UUID in frontmatter
            updated_frontmatter['pieces_id'] = original_uuid
            
            # Generate new filename with activity name if available
            if activity_name:
                clean_activity = re.sub(r'[^a-zA-Z0-9\-_]', '-', activity_name.lower())
                clean_activity = re.sub(r'-+', '-', clean_activity)
                final_title = clean_activity
            else:
                final_title = descriptive_title
            
            # Create filename: YYYY-MM-DD_PARA-type_content-category_title.md
            created = updated_frontmatter.get('created', '')
            if created:
                try:
                    if 'T' in created:
                        date_str = created.split('T')[0]
                    else:
                        date_str = created[:10]
                    datetime.strptime(date_str, '%Y-%m-%d')
                except (ValueError, TypeError):
                    date_str = '2024-06-19'
            else:
                date_str = '2024-06-19'
            
            new_filename = f"{date_str}_{para_type}_{content_category}_{final_title}.md"
            new_filename = re.sub(r'[^a-zA-Z0-9._-]', '-', new_filename)
            new_filename = re.sub(r'-+', '-', new_filename)
            
            new_file_path = input_path / new_filename
            
            # Reconstruct file content with updated frontmatter
            yaml_content = yaml.dump(updated_frontmatter, default_flow_style=False, allow_unicode=True)
            new_file_content = f"---\\n{yaml_content}---\\n\\n{content}"
            
            # Write new file
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_file_content)
            
            # Track mapping
            activity_info = f" [Activity: {activity_name}]" if activity_name else ""
            mappings.append((file_path.name, new_filename, para_type, content_category, activity_info))
            
            print(f"✅ {file_path.name} → {new_filename} [{para_type}/{content_category}]{activity_info}")
            
            # Remove original file if different name
            if file_path.name != new_filename:
                file_path.unlink()
            
            processed += 1
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
    
    # Create enhanced mapping document
    create_enhanced_mapping_document(mappings, input_path)
    
    # Create automated workflow
    pieces_data_path = pieces_data_dir
    workflow_script = create_automated_workflow_script(pieces_data_path, input_path)
    
    print(f"\\n🎉 Successfully processed {processed} files with enhanced PARA framework!")
    print(f"📁 Files updated in: {input_path}")
    print(f"🤖 Automated workflow created: {workflow_script}")
    print(f"\\n💡 To enable automated processing of new workstream activities:")
    print(f"   python3 {workflow_script}")

def create_enhanced_mapping_document(mappings: List[Tuple], output_dir: Path):
    """Create enhanced mapping document with workstream activity information."""
    mapping_content = f"""# Enhanced File Renaming Mapping - PARA Framework + Workstream Activities

This document tracks the renaming of Pieces import files with workstream activity name extraction.

## Enhanced Naming Convention
`YYYY-MM-DD_PARA-type_content-category_workstream-activity-name.md`

## PARA Framework
- **Project**: Specific outcomes with deadlines (debugging, implementations)
- **Area**: Ongoing responsibilities (code standards, maintenance)  
- **Resource**: Reference materials (analysis, guides, learning)
- **Archive**: Completed/inactive items (emails, old questions)

## Workstream Activity Integration
- Activity names extracted from Pieces WorkstreamEvents and Messages data
- Filenames now include actual workstream activity names when available
- Enhanced tagging includes activity-specific keywords

## File Mappings

| Original Filename | New Filename | PARA Type | Category | Activity Info |
|-------------------|-------------|-----------|----------|---------------|
"""
    
    for mapping in mappings:
        old_name, new_name, para_type, category = mapping[:4]
        activity_info = mapping[4] if len(mapping) > 4 else ""
        mapping_content += f"| {old_name} | {new_name} | {para_type} | {category} | {activity_info} |\\n"
    
    mapping_content += f"""

## Automated Workflow
An automated monitoring script has been created to process new workstream activities in real-time.

### Features:
- Monitors Pieces Messages and WorkstreamEvents directories
- Automatically extracts workstream activity names
- Applies PARA framework classification
- Generates properly named markdown files
- Includes activity-specific metadata and tags

### Usage:
```bash
python3 pieces_workstream_monitor.py
```

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    mapping_file = output_dir / "ENHANCED_PARA_MAPPING.md"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write(mapping_content)
    
    print(f"📋 Created enhanced mapping document: {mapping_file}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 enhanced_para_renamer.py <directory_path> [--pieces-data-dir <path>]")
        print("Example: python3 enhanced_para_renamer.py /path/to/obsidian_imports")
        print("         python3 enhanced_para_renamer.py /path/to/obsidian_imports --pieces-data-dir /custom/pieces/path")
        sys.exit(1)
    
    directory = sys.argv[1]
    pieces_data_dir = None
    
    # Parse optional pieces data directory
    if "--pieces-data-dir" in sys.argv:
        idx = sys.argv.index("--pieces-data-dir")
        if idx + 1 < len(sys.argv):
            pieces_data_dir = sys.argv[idx + 1]
    
    process_files_enhanced(directory, pieces_data_dir)