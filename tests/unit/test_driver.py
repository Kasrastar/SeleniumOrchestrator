"""
Unit Tests for Domain Layer - Driver Entity

Tests the Driver domain model including:
- Driver status enumeration
"""

import pytest
from src.domain.driver import DefaultDriverStatus


class TestDriverStatus:
    """Test suite for DriverStatus enum."""
    
    def test_driver_status_open_value(self):
        """Test DriverStatus.OPEN value."""
        assert DefaultDriverStatus.OPEN.value == 'open'
    
    def test_driver_status_closed_value(self):
        """Test DriverStatus.CLOSED value."""
        assert DefaultDriverStatus.CLOSED.value == 'closed'
    
    def test_driver_status_comparison(self):
        """Test comparing driver status values."""
        status1 = DefaultDriverStatus.OPEN
        status2 = DefaultDriverStatus.OPEN
        status3 = DefaultDriverStatus.CLOSED
        
        assert status1 == status2
        assert status1 != status3
    
    def test_driver_status_enum_members(self):
        """Test that all expected enum members exist."""
        members = [member.name for member in DefaultDriverStatus]
        
        assert 'OPEN' in members
        assert 'CLOSED' in members
        assert len(members) == 2
