"""
Unit Tests for Domain Layer - Tab Entity

Tests the Tab domain model including:
- Tab creation
- Status management
- Tab information retrieval
"""

import pytest
from src.domain.tab import Tab, DefaultTabStatus


class TestTab:
    """Test suite for Tab entity."""
    
    def test_tab_creation(self):
        """Test creating a new tab instance."""
        tab = Tab(
            name="test_tab",
            window_handle="window-123",
            status=DefaultTabStatus.ACTIVE
        )
        
        assert tab.name == "test_tab"
        assert tab.window_handle == "window-123"
        assert tab.status == DefaultTabStatus.ACTIVE
    
    def test_tab_update_name(self):
        """Test updating tab name."""
        tab = Tab("original_name", "handle-1", DefaultTabStatus.ACTIVE)
        
        tab.update_name("new_name")
        
        assert tab.name == "new_name"
        assert tab.window_handle == "handle-1"  # Unchanged
    
    def test_tab_update_status(self):
        """Test updating tab status."""
        tab = Tab("tab1", "handle-1", DefaultTabStatus.ACTIVE)
        
        tab.update_status(DefaultTabStatus.INACTIVE)
        
        assert tab.status == DefaultTabStatus.INACTIVE
        assert not tab.is_active()
    
    def test_tab_is_active_when_active(self):
        """Test is_active returns True for active tab."""
        tab = Tab("tab1", "handle-1", DefaultTabStatus.ACTIVE)
        
        assert tab.is_active() is True
    
    def test_tab_is_active_when_inactive(self):
        """Test is_active returns False for inactive tab."""
        tab = Tab("tab1", "handle-1", DefaultTabStatus.INACTIVE)
        
        assert tab.is_active() is False
    
    def test_tab_str_representation(self):
        """Test string representation of tab."""
        tab = Tab("my_tab", "handle-xyz", DefaultTabStatus.ACTIVE)
        
        result = str(tab)
        
        assert "my_tab" in result
        assert "handle-xyz" in result
        assert "ACTIVE" in result
    
    def test_tab_repr_representation(self):
        """Test repr representation of tab."""
        tab = Tab("my_tab", "handle-xyz", DefaultTabStatus.ACTIVE)
        
        result = repr(tab)
        
        assert "Tab(" in result
        assert "'my_tab'" in result
        assert "'handle-xyz'" in result
    
    def test_tab_get_info(self):
        """Test getting tab information as dictionary."""
        tab = Tab("info_tab", "handle-abc", DefaultTabStatus.ACTIVE)
        
        info = tab.get_info()
        
        assert isinstance(info, dict)
        assert info['name'] == "info_tab"
        assert info['window_handle'] == "handle-abc"
        assert info['status'] == DefaultTabStatus.ACTIVE
    
    def test_tab_status_enum_values(self):
        """Test TabStatus enum values."""
        assert DefaultTabStatus.ACTIVE.value == 'active'
        assert DefaultTabStatus.INACTIVE.value == 'inactive'
    
    def test_multiple_tabs_with_same_status(self):
        """Test creating multiple tabs with same status."""
        tab1 = Tab("tab1", "handle-1", DefaultTabStatus.ACTIVE)
        tab2 = Tab("tab2", "handle-2", DefaultTabStatus.ACTIVE)
        
        assert tab1.is_active()
        assert tab2.is_active()
        assert tab1.name != tab2.name
        assert tab1.window_handle != tab2.window_handle
    
    def test_tab_status_transition(self):
        """Test transitioning tab status multiple times."""
        tab = Tab("tab", "handle", DefaultTabStatus.ACTIVE)
        
        assert tab.is_active()
        
        tab.update_status(DefaultTabStatus.INACTIVE)
        assert not tab.is_active()
        
        tab.update_status(DefaultTabStatus.ACTIVE)
        assert tab.is_active()
