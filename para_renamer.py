#!/usr/bin/env python3
"""
PARA Framework File Renamer for Pieces-to-Obsidian Imports
Renames .md files using PARA methodology and updates frontmatter accordingly.

Corrected Frontmatter Structure:
---
title: "Descriptive Title"
created: 2024-06-19T19:31:56.686651
tags: [pieces-import, workstream, debugging, "#project"]
type: project
content_category: debugging
source: pieces
pieces_id: original-uuid-preserved
---
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, List

def analyze_content_for_para(content: str, title: str) -> Tuple[str, str]:
    """
    Analyze content to determine PARA classification and content category.
    
    Returns:
        Tuple of (para_type, content_category)
    """
    content_lower = content.lower()
    title_lower = title.lower()
    
    # Project indicators - specific outcomes with deadlines
    project_keywords = ['debug', 'implement', 'fix', 'solve', 'error', 'issue', 'problem', 'troubleshoot']
    
    # Area indicators - ongoing responsibilities 
    area_keywords = ['standard', 'practice', 'convention', 'guideline', 'maintain', 'manage', 'process']
    
    # Resource indicators - reference materials
    resource_keywords = ['analysis', 'comparison', 'guide', 'reference', 'overview', 'technique', 'tool', 'method']
    
    # Archive indicators - completed/personal items
    archive_keywords = ['email', 'delivered-to', 'what was i doing', 'facebook', 'password reset']
    
    # Determine content category
    if any(keyword in content_lower or keyword in title_lower for keyword in ['debug', 'error', 'troubleshoot', 'issue']):
        content_category = 'debugging'
    elif any(keyword in content_lower or keyword in title_lower for keyword in ['code', 'python', 'function', 'blank lines']):
        content_category = 'code-fix'
    elif any(keyword in content_lower or keyword in title_lower for keyword in ['analysis', 'comparison', 'evaluate']):
        content_category = 'analysis'
    elif any(keyword in content_lower or keyword in title_lower for keyword in ['email', 'delivered-to', '@']):
        content_category = 'email'
    elif len(content.strip()) < 50:
        content_category = 'question'
    else:
        content_category = 'general'
    
    # Determine PARA type
    if any(keyword in content_lower or keyword in title_lower for keyword in archive_keywords):
        para_type = 'archive'
    elif any(keyword in content_lower or keyword in title_lower for keyword in project_keywords):
        para_type = 'project'
    elif any(keyword in content_lower or keyword in title_lower for keyword in area_keywords):
        para_type = 'area'
    elif any(keyword in content_lower or keyword in title_lower for keyword in resource_keywords):
        para_type = 'resource'
    else:
        # Default classification based on content category
        if content_category in ['debugging', 'code-fix']:
            para_type = 'project'
        elif content_category in ['email', 'question']:
            para_type = 'archive'
        elif content_category in ['analysis']:
            para_type = 'resource'
        else:
            para_type = 'resource'
    
    return para_type, content_category

def generate_descriptive_title(content: str, original_title: str) -> str:
    """Generate a descriptive title from content."""
    # Clean original title
    title = original_title.replace('"', '').strip()
    if title and not title.startswith('The error message') and len(title) > 10:
        # Use first part of original title
        words = title.split()[:4]
        return '-'.join(word.lower().strip('.,!?;:') for word in words if word.isalnum() or word in ['and', 'or', 'the', 'to', 'for'])
    
    # Extract from content
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 10 and not line.startswith('#') and not line.startswith('---'):
            words = line.split()[:4]
            clean_words = []
            for word in words:
                clean_word = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
                if clean_word and len(clean_word) > 1:
                    clean_words.append(clean_word)
            if clean_words:
                return '-'.join(clean_words[:4])
    
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

def update_frontmatter(frontmatter: Dict, para_type: str, content_category: str, new_title: str) -> Dict:
    """Update frontmatter with PARA classification following corrected structure."""
    # Preserve existing data
    updated = frontmatter.copy()
    
    # Update title if not descriptive
    if 'title' not in updated or updated['title'].startswith('The error message') or len(updated['title']) < 10:
        updated['title'] = new_title.replace('-', ' ').title()
    
    # Update tags - add PARA hashtag to existing tags
    current_tags = updated.get('tags', [])
    if isinstance(current_tags, str):
        current_tags = [current_tags]
    
    # Ensure required tags are present
    required_tags = ['pieces-import', 'workstream', content_category, f'#{para_type}']
    for tag in required_tags:
        if tag not in current_tags:
            current_tags.append(tag)
    
    updated['tags'] = current_tags
    
    # Set type (without hashtag)
    updated['type'] = para_type
    
    # Set content category
    updated['content_category'] = content_category
    
    return updated

def generate_new_filename(frontmatter: Dict, para_type: str, content_category: str, descriptive_title: str) -> str:
    """Generate new filename following PARA convention."""
    # Extract date from created field
    created = frontmatter.get('created', '')
    if created:
        try:
            if 'T' in created:
                date_str = created.split('T')[0]
            else:
                date_str = created[:10]
            # Validate date format
            datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            date_str = '2024-06-19'  # fallback
    else:
        date_str = '2024-06-19'  # fallback
    
    # Build filename: YYYY-MM-DD_PARA-type_content-category_descriptive-title.md
    filename = f"{date_str}_{para_type}_{content_category}_{descriptive_title}.md"
    
    # Clean filename of invalid characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '-', filename)
    filename = re.sub(r'-+', '-', filename)  # Remove multiple dashes
    
    return filename

def create_mapping_document(mappings: List[Tuple[str, str]], output_dir: Path):
    """Create a mapping document showing old -> new filename relationships."""
    mapping_content = """# File Renaming Mapping - PARA Framework Integration

This document tracks the renaming of Pieces import files to PARA framework convention.

## Naming Convention
`YYYY-MM-DD_PARA-type_content-category_descriptive-title.md`

## PARA Framework
- **Project**: Specific outcomes with deadlines (debugging, implementations)
- **Area**: Ongoing responsibilities (code standards, maintenance)  
- **Resource**: Reference materials (analysis, guides, learning)
- **Archive**: Completed/inactive items (emails, old questions)

## File Mappings

| Original Filename | New Filename | PARA Type | Category |
|-------------------|-------------|-----------|----------|
"""
    
    for old_name, new_name in mappings:
        # Extract PARA type and category from new filename
        parts = new_name.replace('.md', '').split('_')
        if len(parts) >= 3:
            para_type = parts[1]
            category = parts[2]
        else:
            para_type = 'unknown'
            category = 'unknown'
        
        mapping_content += f"| {old_name} | {new_name} | {para_type} | {category} |\n"
    
    mapping_file = output_dir / "PARA_RENAMING_MAPPING.md"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write(mapping_content)
    
    print(f"📋 Created mapping document: {mapping_file}")

def process_files(input_dir: str):
    """Process all .md files in the input directory."""
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Directory not found: {input_dir}")
        return
    
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
            
            # Analyze content for PARA classification
            original_title = frontmatter.get('title', '')
            para_type, content_category = analyze_content_for_para(content, original_title)
            
            # Generate descriptive title
            descriptive_title = generate_descriptive_title(content, original_title)
            
            # Update frontmatter
            updated_frontmatter = update_frontmatter(frontmatter, para_type, content_category, descriptive_title)
            
            # Preserve original UUID in frontmatter
            original_uuid = file_path.stem
            updated_frontmatter['pieces_id'] = original_uuid
            
            # Generate new filename
            new_filename = generate_new_filename(updated_frontmatter, para_type, content_category, descriptive_title)
            new_file_path = input_path / new_filename
            
            # Reconstruct file content with updated frontmatter
            yaml_content = yaml.dump(updated_frontmatter, default_flow_style=False, allow_unicode=True)
            new_file_content = f"---\n{yaml_content}---\n\n{content}"
            
            # Write new file
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_file_content)
            
            # Track mapping
            mappings.append((file_path.name, new_filename))
            
            print(f"✅ {file_path.name} → {new_filename} [{para_type}/{content_category}]")
            
            # Remove original file if different name
            if file_path.name != new_filename:
                file_path.unlink()
            
            processed += 1
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
    
    # Create mapping document
    create_mapping_document(mappings, input_path)
    
    print(f"\n🎉 Successfully processed {processed} files with PARA framework integration!")
    print(f"📁 Files updated in: {input_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 para_renamer.py <directory_path>")
        print("Example: python3 para_renamer.py /path/to/obsidian_imports")
        sys.exit(1)
    
    directory = sys.argv[1]
    process_files(directory)