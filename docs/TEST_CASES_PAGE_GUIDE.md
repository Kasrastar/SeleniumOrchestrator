# Test Cases Page - Implementation Guide

## Overview

This document provides comprehensive information about the **TestCasesPage** and **NewTestCaseModal** page objects, which enable automation of Jira Zephyr Scale Test Cases Library functionality.

**Page URL Pattern**: `https://jira.inside45.ir/secure/Tests.jspa#/v2/testCases?projectId={projectId}`

**Design Pattern**: Page + Modal Component Pattern

---

## Architecture

### Page Object Model (POM)

The implementation follows the **Composite Pattern** where:

1. **TestCasesPage** - Main page object handling:
   - Folder tree navigation
   - Test case grid/list operations
   - Search and filter functionality
   - Page-level actions

2. **NewTestCaseModal** - Modal component handling:
   - Form field interactions
   - Test case creation
   - Modal lifecycle (open/close)
   - Field validation

### Why Separate Modal Component?

The modal is separated from the main page because:
- **Single Responsibility**: Each class has one clear purpose
- **Reusability**: Modal can be opened from multiple locations
- **Testability**: Modal can be tested independently
- **Maintainability**: Changes to modal don't affect main page logic
- **No Navigation**: Modal overlays the page without navigation

---

## File Structure

```
src/pages/
├── test_cases_page.py          # Main page object (750+ lines)
├── new_test_case_modal.py      # Modal component (650+ lines)
└── __init__.py                 # Updated with new exports

examples/
└── test_cases_page_example.py  # 10 comprehensive usage examples
```

---

## TestCasesPage Class

### Initialization

```python
from src.pages.test_cases_page import TestCasesPage

# Initialize with default project ID
test_cases_page = TestCasesPage(session)

# Initialize with custom project ID
test_cases_page = TestCasesPage(session, project_id="10200")
```

### Key Features

#### 1. Navigation Methods

```python
# Navigate to test cases page
test_cases_page.navigate()

# Navigate to specific project
test_cases_page.navigate_to_project("10200")

# Switch between tabs
test_cases_page.switch_to_test_cycles()
test_cases_page.switch_to_test_plans()
test_cases_page.switch_to_reports()

# Open configuration
test_cases_page.click_configuration()
```

#### 2. Folder Tree Operations

```python
# Click root folder
test_cases_page.click_all_test_cases_folder()

# Click folder by ID
test_cases_page.click_folder_by_id("2")  # ID 2 = Login folder

# Click folder by name
test_cases_page.click_folder_by_name("Login")

# Navigate to nested folder path
test_cases_page.navigate_to_folder_path("/K45-library/dealer/aaa/login")

# Expand folder to show children
test_cases_page.expand_folder("10")

# Get folder test case count
count = test_cases_page.get_folder_count("2")  # Returns "(14)"

# Check if folder is selected
is_selected = test_cases_page.is_folder_selected("2")

# Get all visible folders
folders = test_cases_page.get_all_visible_folders()
# Returns: [{"id": "2", "name": "Login", "count": "(14)"}, ...]
```

#### 3. Action Bar Operations

```python
# Create new test case (returns modal instance)
modal = test_cases_page.click_new_test_case()

# Other actions
test_cases_page.click_archive()
test_cases_page.click_clone()
test_cases_page.click_more()
test_cases_page.click_new_folder()
```

#### 4. Search and Filter

```python
# Search for test cases
test_cases_page.enter_search_text("login")

# Clear search
test_cases_page.clear_search()

# Open filters panel
test_cases_page.click_filters()
```

#### 5. Verification Methods

```python
# Wait for page to be ready
is_ready = test_cases_page.wait_for_page_ready(timeout=10)

# Check if Test Cases tab is active
is_active = test_cases_page.is_test_cases_tab_active()

# Get current project name
project_name = test_cases_page.get_current_project_name()

# Get total test case count
count = test_cases_page.get_all_test_cases_count()

# Get selected folder name
folder = test_cases_page.get_selected_folder_name()

# Check for empty state
is_empty = test_cases_page.is_empty_state_displayed()
message = test_cases_page.get_empty_state_message()
```

### Important Locators

The page contains 40+ locator definitions organized by section:

- **Header Locators**: Project selector, configuration button
- **Tab Navigation**: Test Cases, Cycles, Plans, Reports tabs
- **Folder Tree**: All folder-related elements with dynamic templates
- **Action Bar**: New test case, archive, clone, more buttons
- **Search/Filter**: Search input, filters button
- **Content Area**: Empty state, grid area

---

## NewTestCaseModal Class

### Initialization

```python
from src.pages.new_test_case_modal import NewTestCaseModal

# Usually created from TestCasesPage
modal = test_cases_page.click_new_test_case()

# Or manually instantiated
modal = NewTestCaseModal(session)
```

### Modal Lifecycle

```python
# Wait for modal to appear
modal.wait_for_modal_visible(timeout=10)

# Check if modal is visible
is_visible = modal.is_modal_visible()

# Wait for modal to be ready (fully loaded)
modal.wait_for_modal_ready(timeout=10)

# Get modal title
title = modal.get_modal_title()  # Returns "Create Test Case"

# Close modal
modal.click_close_button()  # Using X button
modal.click_cancel()        # Using Cancel button

# Wait for modal to close
modal.wait_for_modal_closed(timeout=10)
```

### Form Fields

#### Required Fields

```python
# Name field (Required)
modal.enter_name("Verify Login Functionality")
modal.clear_name()
name = modal.get_name()
is_empty = modal.is_name_field_empty()
```

#### Optional Rich Text Fields

```python
# Objective (with rich text editor)
modal.enter_objective("Verify that users can successfully log in")
modal.clear_objective()

# Apply formatting
modal.click_objective_bold()
modal.click_objective_italic()
modal.click_objective_underline()
modal.click_objective_insert_link()

# Precondition (with rich text editor)
modal.enter_precondition("User account exists in the system")
modal.clear_precondition()
modal.click_precondition_bold()
modal.click_precondition_italic()
```

#### Details Section

```python
# Status dropdown
modal.click_status_dropdown()
modal.select_status("Draft")  # Options: Draft, Approved, etc.
status = modal.get_selected_status()

# Component dropdown
modal.click_component_dropdown()
modal.select_component("Backend API")

# Estimated run time (hh:mm format)
modal.enter_estimated_time("01:30")  # 1 hour 30 minutes
modal.clear_estimated_time()

# Priority dropdown
modal.click_priority_dropdown()
modal.select_priority("High")  # Options: High, Normal, Low
priority = modal.get_selected_priority()

# Owner dropdown
modal.click_owner_dropdown()
modal.select_owner("Ali Khamoush")
owner = modal.get_selected_owner()
modal.clear_owner()

# Folder selection
folder = modal.get_selected_folder()  # Returns path like "/K45-library/dealer/aaa/login"
modal.click_folder_select()  # Opens folder picker
modal.clear_folder()

# Labels (multi-select)
modal.click_labels_dropdown()
modal.add_label("regression")
modal.add_label("smoke-test")
```

### Form Submission

```python
# Create another checkbox
modal.check_create_another()
modal.uncheck_create_another()
is_checked = modal.is_create_another_checked()

# Submit form
modal.click_create()
modal.click_create_dropdown()  # For dropdown options

# Convenience method to fill all fields at once
modal.create_test_case(
    name="My Test Case",
    objective="Test objective description",
    precondition="Required preconditions",
    status="Draft",
    priority="High",
    estimated_time="00:30",
    create_another=False
)
```

---

## Usage Patterns

### Pattern 1: Simple Test Case Creation

```python
# Navigate to page
test_cases_page = TestCasesPage(session, project_id="10200")
test_cases_page.navigate()
test_cases_page.wait_for_page_ready()

# Open modal and create
modal = test_cases_page.click_new_test_case()
modal.wait_for_modal_ready()
modal.enter_name("Verify Login")
modal.click_create()
modal.wait_for_modal_closed()
```

### Pattern 2: Complete Test Case with All Details

```python
# Select target folder
test_cases_page.click_folder_by_name("Login")

# Create test case with all fields
modal = test_cases_page.click_new_test_case()
modal.create_test_case(
    name="Verify Password Reset Email",
    objective="Ensure password reset email contains correct link",
    precondition="User account exists with verified email",
    status="Approved",
    priority="High",
    estimated_time="00:15"
)
modal.wait_for_modal_closed()
```

### Pattern 3: Creating Multiple Test Cases

```python
test_cases = [
    {"name": "Test 1", "priority": "High"},
    {"name": "Test 2", "priority": "Normal"},
    {"name": "Test 3", "priority": "Low"}
]

modal = test_cases_page.click_new_test_case()

for idx, tc in enumerate(test_cases):
    is_last = (idx == len(test_cases) - 1)
    
    modal.enter_name(tc["name"])
    modal.select_priority(tc["priority"])
    
    if not is_last:
        modal.check_create_another()
    else:
        modal.uncheck_create_another()
    
    modal.click_create()
    
    if not is_last:
        modal.wait_for_modal_ready()
        modal.clear_name()

modal.wait_for_modal_closed()
```

### Pattern 4: Folder Navigation with Verification

```python
# Navigate and verify
test_cases_page.navigate_to_folder_path("/K45-library/dealer/login")

# Verify selection
if test_cases_page.is_folder_selected("21"):
    folder_name = test_cases_page.get_selected_folder_name()
    print(f"Selected: {folder_name}")

# Get folder statistics
count = test_cases_page.get_folder_count("21")
print(f"Test cases in folder: {count}")
```

### Pattern 5: Search and Create

```python
# Search for existing test cases
test_cases_page.enter_search_text("login")
test_cases_page.wait(2)  # Wait for search results

# If not found, create new one
if test_cases_page.is_empty_state_displayed():
    modal = test_cases_page.click_empty_state_create_link()
    modal.create_test_case(name="New Login Test", priority="High")
    modal.wait_for_modal_closed()
```

---

## Testing Examples

The `examples/test_cases_page_example.py` file contains 10 comprehensive examples:

1. **Example 1**: Basic navigation and verification
2. **Example 2**: Folder tree navigation
3. **Example 3**: Simple test case creation
4. **Example 4**: Complete test case with all fields
5. **Example 5**: Creating multiple test cases
6. **Example 6**: Search and filter operations
7. **Example 7**: Modal field operations
8. **Example 8**: Archived test cases
9. **Example 9**: Empty state handling
10. **Example 10**: Complete end-to-end workflow

### Running Examples

```bash
# From project root
cd /home/lighthouse/projects/SeleniumOrchestrator

# Run specific example (uncomment in main block)
python examples/test_cases_page_example.py
```

---

## Best Practices

### 1. Wait Strategies

Always wait for page/modal readiness:

```python
# Wait for page
test_cases_page.wait_for_page_ready(timeout=15)

# Wait for folder tree
test_cases_page.wait_for_folder_tree_loaded(timeout=10)

# Wait for modal
modal.wait_for_modal_ready(timeout=10)
modal.wait_for_modal_closed(timeout=10)
```

### 2. Error Handling

```python
try:
    modal = test_cases_page.click_new_test_case()
    if not modal.wait_for_modal_visible(timeout=10):
        raise Exception("Modal did not appear")
    
    modal.create_test_case(name="Test Case", priority="High")
    
    if not modal.wait_for_modal_closed(timeout=10):
        raise Exception("Modal did not close")
        
except Exception as e:
    print(f"Error creating test case: {e}")
    # Take screenshot or log error
```

### 3. Verification After Actions

```python
# Verify folder selection
test_cases_page.click_folder_by_name("Login")
assert test_cases_page.is_folder_selected("2")

# Verify test case created (check count)
initial_count = test_cases_page.get_folder_count("2")
# ... create test case ...
final_count = test_cases_page.get_folder_count("2")
# Note: Count is string like "(14)", needs parsing for comparison
```

### 4. Use Convenience Methods

```python
# Instead of this:
modal.enter_name("Test")
modal.enter_objective("Objective")
modal.select_priority("High")
modal.click_create()

# Use this:
modal.create_test_case(
    name="Test",
    objective="Objective",
    priority="High"
)
```

---

## Integration with Existing Code

### With JiraLoginPage

```python
from src.pages.jira_login_page import JiraLoginPage
from src.pages.test_cases_page import TestCasesPage

# Login first
jira_login = JiraLoginPage(session)
jira_login.navigate()
jira_login.login_with_credentials("username", "password")
jira_login.wait_for_successful_login()

# Then navigate to test cases
test_cases_page = TestCasesPage(session, project_id="10200")
test_cases_page.navigate()
test_cases_page.wait_for_page_ready()
```

### With Test Framework

```python
import pytest
from src.pages.test_cases_page import TestCasesPage
from src.pages.new_test_case_modal import NewTestCaseModal

@pytest.fixture
def test_cases_page(session):
    page = TestCasesPage(session, project_id="10200")
    page.navigate()
    page.wait_for_page_ready()
    return page

def test_create_test_case(test_cases_page):
    """Test creating a new test case."""
    # Arrange
    test_cases_page.click_folder_by_name("Login")
    
    # Act
    modal = test_cases_page.click_new_test_case()
    modal.create_test_case(
        name="Verify Login Success",
        priority="High"
    )
    
    # Assert
    assert modal.wait_for_modal_closed(timeout=10)
```

---

## Locator Strategy

All locators use the following selectors (in priority order):

1. **data-testid attributes** - Most reliable
   ```python
   NEW_TEST_CASE_BUTTON = Locator("css", "button[data-testid='ktm-create-new-folder']")
   ```

2. **ID attributes** - Unique identifiers
   ```python
   SEARCH_INPUT = Locator("css", "input#zephyr-scale-grid-search")
   ```

3. **CSS classes** - Stable classes
   ```python
   SELECTED_FOLDER = Locator("css", ".ktm-folder-tree-item.isSelected")
   ```

4. **Dynamic templates** - For similar elements
   ```python
   FOLDER_ITEM_TEMPLATE = "div[data-testid='folder-item-{folder_id}']"
   ```

---

## Known Limitations

1. **Rich Text Editor**: The Froala editor has limited automation support. Use simple text entry for most cases.

2. **Dropdown Options**: Dropdown option locators may need adjustment based on actual option values.

3. **Modal Animations**: Modal open/close animations may require additional wait time.

4. **Folder Tree Loading**: Large folder trees may take time to load; increase timeout if needed.

5. **Search Debouncing**: Search has debounce delay; add explicit wait after search input.

---

## Troubleshooting

### Modal Not Appearing

```python
# Ensure button is clickable
button = test_cases_page.find_element(
    test_cases_page.NEW_TEST_CASE_BUTTON,
    condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE
)

# Try alternative method
test_cases_page.click_empty_state_create_link()
```

### Folder Not Selecting

```python
# Expand parent folder first
test_cases_page.expand_folder("10")
test_cases_page.wait(1)

# Then click child
test_cases_page.click_folder_by_id("21")
```

### Dropdown Not Opening

```python
# Click directly on input
modal.click_status_dropdown()
modal.wait(0.5)  # Wait for dropdown animation

# Then select option
modal.select_status("Draft")
```

---

## Maintenance

### Adding New Locators

1. Identify element in DOM
2. Add locator to appropriate section
3. Create accessor method
4. Add to docstring
5. Test with actual page

### Updating for DOM Changes

1. Check browser DevTools for new attributes
2. Update locator definitions
3. Run verification tests
4. Update documentation

---

## Summary

The **TestCasesPage** and **NewTestCaseModal** provide:

- ✅ **750+ lines** of comprehensive page object code
- ✅ **90+ methods** for all page interactions
- ✅ **40+ locators** organized by section
- ✅ **10 usage examples** covering all scenarios
- ✅ **Page + Modal pattern** for clean architecture
- ✅ **Full CRUD support** for test case management
- ✅ **Folder navigation** with nested path support
- ✅ **Rich text editor** interactions
- ✅ **Search and filter** functionality
- ✅ **Complete documentation** with best practices

This implementation follows all established patterns in the repository and integrates seamlessly with existing `JiraLoginPage` and other page objects.
