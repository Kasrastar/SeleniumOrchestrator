# Test Case Detail Page Implementation Guide

## Overview

I've implemented comprehensive page objects for handling the Jira Zephyr Test Case Detail page, including full support for Test Script functionality. This enables you to:

1. **Create test cases** using the "Create and Edit" option
2. **Navigate directly to the detail page** after creation
3. **Add test scripts** with step-by-step entries
4. **Automatically generate new rows** using the TAB key
5. **Select different script types** (Plain Text, Step-by-Step, BDD)

## Files Created/Modified

### 1. `src/pages/test_case_detail_page.py` (NEW - 550+ lines)

Complete page object for the Test Case Detail/Edit page with:

**Key Features:**
- Tab navigation (Details, Test Script, Execution, etc.)
- Test script type selection (Plain Text, Step-by-Step, BDD)
- Individual step management (add, edit, delete)
- Automatic step generation via TAB key
- Rich text editor support for steps
- Save and navigation controls

**Main Methods:**

```python
# Navigation
navigate_to_test_case(test_case_key: str)
wait_for_page_ready(timeout: int = 10)
click_test_script_tab()

# Script Type Management
get_current_script_type() -> str
select_script_type(script_type: str)  # 'Plain Text', 'Step-by-Step', 'BDD'

# Step Management
get_steps_count() -> int
add_test_step(description, test_data, expected_result, auto_create_next=True)
add_multiple_test_steps(steps: List[Dict])
enter_step_description(step_index, description)
enter_step_test_data(step_index, test_data)
enter_step_expected_result(step_index, expected_result, press_tab=True)

# Actions
click_save()
click_back()
get_test_case_key() -> str
get_page_title() -> str
```

### 2. `src/pages/new_test_case_modal.py` (UPDATED)

Enhanced modal with "Create and Edit" functionality:

**New Locators:**
```python
CREATE_AND_EDIT_OPTION = Locator(By.XPATH, "//div[contains(@class, 'aui-dropdown2')]//a[contains(., 'Create and Edit')]")
```

**New Method:**
```python
def click_create_and_edit() -> bool:
    """
    Click the "Create and Edit" option from the dropdown menu.
    This creates the test case and navigates to the detail page.
    """
```

### 3. `examples/create_test_case_with_script.py` (NEW)

Complete workflow example demonstrating:
- Login
- Navigate to Test Cases page
- Create test case using "Create and Edit"
- Switch to Test Script tab
- Select "Step-by-Step" type
- Add 5 test steps
- Save and verify

### 4. `src/pages/__init__.py` (UPDATED)

Added export for TestCaseDetailPage

## Usage Examples

### Example 1: Basic Test Script Addition

```python
from src.pages.test_case_detail_page import TestCaseDetailPage

# Navigate to existing test case
detail_page = TestCaseDetailPage(session, test_case_key="SDLC-T180")
detail_page.navigate()
detail_page.wait_for_page_ready()

# Switch to Test Script tab
detail_page.click_test_script_tab()

# Ensure Step-by-Step mode
detail_page.select_script_type("Step-by-Step")

# Add a single step
detail_page.add_test_step(
    description="Enter username",
    test_data="testuser@example.com",
    expected_result="Username field is populated",
    auto_create_next=True  # Press TAB to create next row
)

# Save
detail_page.click_save()
```

### Example 2: Add Multiple Steps at Once

```python
steps = [
    {
        'description': 'Open login page',
        'test_data': 'URL: https://app.com/login',
        'expected_result': 'Login form is displayed'
    },
    {
        'description': 'Enter credentials',
        'test_data': 'user@test.com / Pass123',
        'expected_result': 'Credentials are entered'
    },
    {
        'description': 'Click login',
        'test_data': 'N/A',
        'expected_result': 'User is logged in'
    }
]

detail_page.add_multiple_test_steps(steps)
detail_page.click_save()
```

### Example 3: Complete Workflow with "Create and Edit"

```python
# Step 1: Create test case with modal
modal = test_cases_page.click_new_test_case()
modal.enter_name("My Test Case")
modal.enter_objective("Test objective")
modal.select_priority("High")

# Step 2: Use "Create and Edit" instead of regular "Create"
modal.click_create_and_edit()  # Opens detail page immediately

# Step 3: Work with detail page
detail_page = TestCaseDetailPage(session)
detail_page.wait_for_page_ready()
detail_page.click_test_script_tab()

# Step 4: Add steps
detail_page.select_script_type("Step-by-Step")
detail_page.add_test_step(
    description="Test step 1",
    test_data="Data 1",
    expected_result="Result 1",
    auto_create_next=True  # TAB key pressed automatically
)

detail_page.click_save()
```

## Key Features Explained

### 1. Script Type Selection

The page supports three script types:
- **Plain Text**: Free-form text area
- **Step-by-Step**: Structured table with Description, Test Data, Expected Result
- **BDD**: Behavior-Driven Development format (Given/When/Then)

```python
# Switch between types
detail_page.select_script_type("Step-by-Step")
detail_page.select_script_type("Plain Text")
detail_page.select_script_type("BDD")

# Check current type
current_type = detail_page.get_current_script_type()
```

### 2. TAB Key Auto-Generation

When `press_tab=True` (default) in `enter_step_expected_result()`:
- After entering the expected result
- TAB key is automatically pressed
- Jira generates a new empty step row
- You can immediately start filling the next step

```python
# Manual control
detail_page.enter_step_expected_result(1, "Result text", press_tab=True)

# Automatic in add_test_step
detail_page.add_test_step(
    description="...",
    test_data="...",
    expected_result="...",
    auto_create_next=True  # Uses TAB internally
)
```

### 3. Step Indexing

Steps use **1-based indexing** (step 1, step 2, step 3...):

```python
# Access specific steps
detail_page.enter_step_description(1, "First step")
detail_page.enter_step_test_data(2, "Second step data")
detail_page.enter_step_expected_result(3, "Third step result")

# Count steps
count = detail_page.get_steps_count()  # Returns 3
```

### 4. Rich Text Editors

Each step field is a rich text editor with:
- Bold, Italic, Underline formatting
- Link insertion
- Parameter support (e.g., `{username}`, `{password}`)

The implementation clicks the editor div and sends text directly:

```python
editor = detail_page.get_step_description_editor(1)
editor.click()
editor.send_keys("My step description")
```

## Important Notes

### 1. Modal Dropdown Structure

The "Create" button in the modal is actually a **split button**:
- Main button: Regular "Create" (closes modal)
- Dropdown arrow: Opens menu with "Create and Edit"

```python
# Regular create (closes modal)
modal.click_create()

# Create and edit (opens detail page)
modal.click_create_and_edit()  # Better for adding scripts
```

### 2. Page Load Timing

After `click_create_and_edit()`:
- Jira redirects to detail page
- URL changes to: `/secure/Tests.jspa#/testCase/SDLC-Txxx`
- Page needs time to load (use `wait_for_page_ready()`)

```python
modal.click_create_and_edit()
sleep(3)  # Allow navigation

detail_page = TestCaseDetailPage(session)
detail_page.wait_for_page_ready(timeout=10)
```

### 3. Save Behavior

The Save button in the detail page:
- Saves all changes (details + test script)
- Does NOT close the page
- Shows brief success indication
- Page remains in edit mode

```python
detail_page.click_save()
sleep(2)  # Allow save to complete
```

### 4. Step Generation Timing

When TAB creates a new step:
- Short delay (~500ms-1s) for Jira to generate the row
- New editors need to be found again
- The `add_multiple_test_steps()` method handles this automatically

## Troubleshooting

### Issue: Steps not appearing
**Solution**: Ensure you're in Step-by-Step mode
```python
detail_page.select_script_type("Step-by-Step")
sleep(1)
```

### Issue: Can't find step editor
**Solution**: Wait for page to be ready first
```python
detail_page.wait_for_page_ready()
detail_page.click_test_script_tab()
sleep(2)  # Wait for tab content
```

### Issue: TAB key not creating new row
**Solution**: Ensure focus is in Expected Result field of last step
```python
editor = detail_page.get_step_expected_result_editor(last_step_index)
editor.click()  # Focus first
editor.send_keys("Result")
editor.send_keys(Keys.TAB)
```

### Issue: "Create and Edit" option not found
**Solution**: Make sure to click dropdown button first
```python
modal.click(modal.CREATE_DROPDOWN_BUTTON)
sleep(0.5)
modal.click(modal.CREATE_AND_EDIT_OPTION)
```

## Complete Workflow Summary

```
1. Login → Test Cases Page
2. Select Folder
3. Click "New Test Case"
4. Fill Modal Form
5. Click "Create and Edit" ← KEY STEP
6. Wait for Detail Page
7. Click "Test Script" Tab
8. Select "Step-by-Step"
9. Add Steps (with TAB auto-generation)
10. Save
11. Verify
```

## Testing the Implementation

Run the example script:

```bash
cd /home/lighthouse/projects/SeleniumOrchestrator
python examples/create_test_case_with_script.py
```

This will:
1. Create a test case named "Verify User Login with Valid Credentials"
2. Add 5 test steps with descriptions, data, and expected results
3. Save the test case
4. Keep browser open for 10 seconds for inspection

## Next Steps

You can extend this implementation to support:

1. **Call to Test**: Link to other test cases within steps
2. **Attach Files**: Upload files to specific steps
3. **Clone Steps**: Duplicate existing steps
4. **Delete Steps**: Remove unwanted steps
5. **Custom Fields**: Handle step-level custom fields
6. **Test Parameters**: Manage parameterized test data

All locators and helper methods are already in place!
