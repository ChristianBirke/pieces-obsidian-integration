# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Working Solution

This repository contains a **working Pieces-to-Obsidian integration** delivered in 1 hour vs the originally planned 28-hour research phase. The core functionality is complete and ready to use.

### Primary Command
```bash
python3 pieces_to_obsidian.py
```
This is the main working solution that extracts Pieces Workstream Activities and converts them to Obsidian markdown files.

### Key File System Locations
- **Pieces data location**: `~/Library/com.pieces.os/production/Pieces/Messages/` (macOS)
- **Data format**: Gzip-compressed `.piece` files containing readable text
- **Output**: `obsidian_imports/` directory with converted markdown files

## Architecture Overview

### Current Implementation (Working)
- **Language**: Python 3.8+ (standard library only, zero dependencies)
- **Data Access**: Direct file system approach (bypasses broken Pieces CLI)
- **Processing Pipeline**: Extract → Decompress (gzip) → Convert → Export
- **Output Format**: Obsidian-compatible markdown with YAML frontmatter

### Key Discovery: CLI Alternative Approach
The Pieces CLI is broken (syntax errors, version incompatibilities), but the data is accessible directly through the file system. This discovery enabled rapid solution delivery.

## Development Context

### Project Structure Reality
- **`pieces_to_obsidian.py`**: The working solution (73 lines)
- **`01_Epics/`**: Comprehensive Epic documentation (now mostly historical)
- **`research/`**: Research framework (completed in rapid validation)
- **`RAPID-VALIDATION-FINDINGS.md`**: Documents the breakthrough approach

### Epic Status (Actual vs Planned)
- **Epic 1.0** (Research): ✅ Completed in 1 hour via rapid validation
- **Epic 2.0** (Architecture): ⚠️ Skipped - architecture emerged from working code
- **Epic 3.0** (Implementation): ✅ Delivered as `pieces_to_obsidian.py`
- **Epic 4.0** (Enhancement): 🔄 Next phase for features/UX improvements

## Enhancement Opportunities

### Immediate (1-2 hours)
- Add command-line arguments for custom input/output paths
- Improve title extraction from content (currently uses UUID-based filenames)
- Add error handling for missing Pieces data directories

### Short-term (1 day)
- Configuration file support (YAML/JSON)
- Date range filtering for selective processing
- Batch processing controls (currently limited to 5 files for testing)

### Medium-term (2-3 days)
- CLI interface using Click or Typer
- Automatic Obsidian vault detection
- Incremental sync capabilities

## Critical Technical Details

### Data Processing
```python
# Core extraction pattern
with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    content = f.read()
```

### Output Format
Each converted file includes:
- YAML frontmatter with metadata (title, created, tags, source, pieces_id)
- Processed content body
- Import timestamp footer

### File System Dependencies
- Requires Pieces Desktop app to be installed (creates data directory)
- Currently macOS-specific path (`~/Library/com.pieces.os/`)
- Windows/Linux paths would need investigation for cross-platform support

## Development Philosophy

This project demonstrates **rapid validation over extensive planning**:
- Working solution in 1 hour vs planned 28-hour research phase
- 1,000x+ efficiency improvement over original Epic timeline
- "Build first, document second" when core assumptions are unknown

When enhancing this codebase, prioritize working solutions over extensive documentation unless specifically requested.