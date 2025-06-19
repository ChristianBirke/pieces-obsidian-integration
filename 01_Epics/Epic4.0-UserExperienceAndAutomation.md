# Epic 4.0 - User Experience Enhancement (Simplified)

## Epic Overview
Add essential CLI features and configuration to make the working prototype more user-friendly and production-ready.

## Epic Goals (Lean Approach)
- Add basic command-line arguments for flexibility
- Remove hardcoded limitations from prototype
- Simple configuration file support
- Better title extraction and filtering

## User Stories (Simplified from 6 to 3)

### US 4.1 - Basic CLI Interface
**As a** user  
**I want to** specify input/output paths and basic options via command line  
**So that** I can customize the converter without editing code  

**Acceptance Criteria:**
- [ ] Add argparse for input/output directory paths
- [ ] Support --limit option to control number of files processed
- [ ] Add --help with clear usage examples
- [ ] Include basic progress output
- [ ] Simple error handling with helpful messages

**Technical Notes:**
- Use Python's built-in argparse (no external dependencies)
- Keep interface simple and intuitive
- Default to current behavior if no args provided

### US 4.2 - Enhanced Processing
**As a** user  
**I want to** process files without artificial limitations  
**So that** I can convert all my Workstream Activities  

**Acceptance Criteria:**
- [ ] Remove hardcoded 5-file limit from prototype
- [ ] Add date range filtering (--since, --until)
- [ ] Improve title extraction from content (first meaningful line)
- [ ] Add minimum content length filter to skip empty files
- [ ] Support different output filename patterns

**Technical Notes:**
- Parse dates from piece file metadata or content
- Extract titles from first non-empty line or meaningful content
- Add content validation before processing

### US 4.3 - Simple Configuration
**As a** user  
**I want to** save my preferences in a config file  
**So that** I don't have to specify the same options repeatedly  

**Acceptance Criteria:**
- [ ] Support simple YAML config file (config.yaml)
- [ ] Override config with command-line arguments
- [ ] Include paths, limits, and formatting options
- [ ] Provide example config file
- [ ] Graceful fallback if config file missing

**Technical Notes:**
- Use PyYAML for config parsing (optional dependency)
- Keep config structure flat and simple
- Provide sensible defaults for all options

## Definition of Done (Simplified)
- [ ] CLI accepts input/output paths and basic options
- [ ] Tool processes all available files (no artificial limits)
- [ ] Config file support for common preferences
- [ ] Better title extraction from content
- [ ] Clear error messages and basic progress feedback

## Dependencies
- ✅ Epic 3.0 Complete - Working prototype ready for enhancement

## Estimated Effort (Simplified)
**Story Points:** 6 (down from 18)  
**Duration:** 1-2 days (down from 2-3 weeks)  
**Implementation:** 6-8 hours total

## Technical Implementation Notes (Lean)
- **CLI Framework:** Built-in `argparse` (zero dependencies)
- **Configuration:** Simple YAML file with `PyYAML` (optional)
- **Progress:** Basic print statements, no fancy progress bars needed
- **Focus:** Essential functionality, not enterprise features

## User Experience Considerations (Simplified)
- Maintain zero-dependency core functionality
- Command-line args override config file settings
- Sensible defaults so tool works without configuration
- Keep it simple - users can use cron for scheduling if needed