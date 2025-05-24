import pytest
import json
import os


class TestBasic:
    """Basic tests to verify pytest setup"""
    
    def test_simple_math(self):
        """Test basic math operations"""
        assert 2 + 2 == 4
        assert 10 - 5 == 5
        assert 3 * 4 == 12
        assert 8 / 2 == 4.0
    
    def test_string_operations(self):
        """Test string operations"""
        text = "Hello World"
        assert text.lower() == "hello world"
        assert text.upper() == "HELLO WORLD"
        assert "Hello" in text
        assert text.startswith("Hello")
        assert text.endswith("World")
    
    def test_list_operations(self):
        """Test list operations"""
        my_list = [1, 2, 3, 4, 5]
        assert len(my_list) == 5
        assert my_list[0] == 1
        assert my_list[-1] == 5
        assert 3 in my_list
        assert max(my_list) == 5
        assert min(my_list) == 1
    
    def test_dict_operations(self):
        """Test dictionary operations"""
        my_dict = {"name": "Test", "age": 25, "active": True}
        assert my_dict["name"] == "Test"
        assert "age" in my_dict
        assert len(my_dict) == 3
        assert my_dict.get("height", 0) == 0
    
    def test_json_operations(self):
        """Test JSON operations"""
        data = {"source": "en", "target": "es", "text": "Hello"}
        json_string = json.dumps(data)
        parsed = json.loads(json_string)
        
        assert parsed == data
        assert parsed["source"] == "en"
        assert isinstance(json_string, str)
    
    def test_file_path_operations(self):
        """Test file path operations"""
        path = os.path.join("data", "models", "test.txt")
        assert "data" in path
        assert "models" in path
        assert "test.txt" in path
        
        # Test path normalization
        normalized = os.path.normpath(path)
        assert isinstance(normalized, str)
    
    def test_environment_variables(self):
        """Test environment variable operations"""
        # Test getting PATH variable (should exist on all systems)
        path_var = os.environ.get("PATH")
        assert path_var is not None
        assert isinstance(path_var, str)
        
        # Test setting a custom environment variable
        os.environ["TEST_VAR"] = "test_value"
        assert os.environ.get("TEST_VAR") == "test_value"
        
        # Cleanup
        del os.environ["TEST_VAR"]
    
    def test_exception_handling(self):
        """Test exception handling"""
        with pytest.raises(ZeroDivisionError):
            result = 10 / 0
        
        with pytest.raises(KeyError):
            my_dict = {"key": "value"}
            value = my_dict["nonexistent_key"]
        
        with pytest.raises(IndexError):
            my_list = [1, 2, 3]
            value = my_list[10]
    
    def test_boolean_logic(self):
        """Test boolean operations"""
        assert True is True
        assert False is False
        assert not False
        assert True and True
        assert True or False
        assert not (False and True)
    
    def test_type_checking(self):
        """Test type checking"""
        assert isinstance("hello", str)
        assert isinstance(42, int)
        assert isinstance(3.14, float)
        assert isinstance([], list)
        assert isinstance({}, dict)
        assert isinstance(True, bool)
