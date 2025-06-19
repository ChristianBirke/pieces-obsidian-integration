# Enhanced File Renaming Mapping - PARA Framework + Workstream Activities

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
| 2024-06-19_project_debugging_the-error-message-indicates.md | 2024-06-19_project_debugging_from-fastmcp-import-fastmcp.md | project | debugging |  [Activity: from-fastmcp-import-FastMCP] |\n| 2024-06-19_resource_general_what-was-my-secret-message.md | 2024-06-19_resource_general_what-was-my-secret-message-from.md | resource | general |  [Activity: What-was-my-secret-message-from] |\n| 2024-06-19_archive_debugging_deliveredto-christianbirkegmailcom.md | 2024-06-19_archive_debugging_delivered-to-christianbirkegmailcom.md | archive | debugging |  [Activity: Delivered-To-christianbirkegmailcom] |\n| 2024-06-19_resource_general_when-does-your-memory-start.md | 2024-06-19_resource_general_when-does-your-memory-start.md | resource | general |  [Activity: when-does-your-memory-start] |\n| 2024-06-19_resource_general_my-memory-starts-from-the.md | 2024-06-19_resource_general_my-memory-starts-from-the.md | resource | general |  |\n| 2024-06-19_project_debugging_to-effectively-diagnose-issues-related.md | 2024-06-19_project_debugging_recommended-debugging-tools-and-techniques.md | project | debugging |  [Activity: Recommended-Debugging-Tools-and-Techniques] |\n| 2024-06-19_project_debugging_to-assist-you-effectively-lets.md | 2024-06-19_project_debugging_1-analysis-of-past-use-of.md | project | debugging |  [Activity: 1-Analysis-of-Past-Use-of] |\n| 2024-06-19_resource_general_what-happened-that-day.md | 2024-06-19_resource_general_what-happened-that-day.md | resource | general |  [Activity: what-happened-that-day] |\n| 2024-06-19_project_debugging_reformat-the-following-to-useful.md | 2024-06-19_project_debugging_reformat-the-following-to-useful.md | project | debugging |  |\n| 2024-06-19_archive_debugging_this-document-tracks-the-renaming.md | 2024-06-19_archive_debugging_this-document-tracks-the-renaming.md | archive | debugging |  |\n| 2024-06-19_archive_general_what-was-doing.md | 2024-06-19_archive_general_what-was-doing.md | archive | general |  |\n| ENHANCED_PARA_MAPPING.md | 2024-06-19_archive_debugging_this-document-tracks-the-renaming.md | archive | debugging |  |\n

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

## Generated: 2025-06-19 20:04:42
