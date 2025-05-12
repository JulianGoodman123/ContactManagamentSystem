import unittest
from unittest.mock import patch, MagicMock
from Application import *

class TestContactApp(unittest.TestCase):

    @patch('Application.tree')  # Mock Treeview
    def test_populate_treeview(self, mock_tree):
        mock_tree.get_children.return_value = ["child1", "child2"]
        populate_treeview()  # Test treeview population
        mock_tree.get_children.assert_called_once()  # Verify method call

    @patch('Application.run_query')  # Mock run_query
    def test_add_item(self, mock_query):
        name = MagicMock()
        name.get.return_value = "John Doe"
        age = MagicMock()
        age.get.return_value = "30"
        phone = MagicMock()
        phone.get.return_value = "1234567890"
        
        add_item()  # Test item addition
        mock_query.assert_called_once_with(
            "INSERT INTO contacts (name, age, phone) VALUES (?, ?, ?)",
            ("John Doe", 30, "1234567890")
        )

    @patch('Application.tree')  # Mock Treeview
    def test_search_item(self, mock_tree):
        mock_tree.get_children.return_value = []
        search_item()  # Test search functionality
        mock_tree.get_children.assert_called_once()  # Verify method call

    @patch('Application.tree')  # Mock Treeview
    def test_refresh_table(self, mock_tree):
        mock_tree.get_children.return_value = []
        refresh_table()  # Test refresh functionality
        mock_tree.get_children.assert_called_once()  # Verify method call

    @patch('Application.tree')  # Mock Treeview
    def test_delete_item(self, mock_tree):
        mock_tree.selection.return_value = ["1234567890"]
        mock_tree.item.return_value = {"values": [None, None, None, "1234567890"]}
        delete_item()  # Test item deletion
        mock_tree.item.assert_called_once()  # Verify method call

    @patch('Application.tree')  # Mock Treeview
    def test_update_item(self, mock_tree):
        mock_tree.selection.return_value = ["1234567890"]
        mock_tree.item.return_value = {"values": [None, None, None, "1234567890"]}
        update_item()  # Test item update
        mock_tree.item.assert_called_once()  # Verify method call

    @patch('Application.tree')  # Mock Treeview
    def test_on_item_double_click(self, mock_tree):
        mock_tree.item.return_value = {"values": [None, None, None, "1234567890", "Some Address"]}
        on_item_double_click(None)  # Test double-click behavior
        mock_tree.item.assert_called_once()  # Verify method call

    @patch('Application.tree')  # Mock Treeview
    def test_clear_text(self, mock_tree):
        name = MagicMock()
        name.get.return_value = ""
        age = MagicMock()
        age.get.return_value = ""
        phone = MagicMock()
        phone.get.return_value = ""

        clear_text()  # Test clear text functionality
        self.assertEqual(name.get(), "")
        self.assertEqual(age.get(), "")
        self.assertEqual(phone.get(), "")

    @patch('Application.run_query')  # Mock run_query
    def test_search_item(self, mock_query):
        search_item()  # Test search functionality
        mock_query.assert_called_once_with("SELECT * FROM contacts WHERE name LIKE ?", ('%',))

    @patch('Application.run_query')  # Mock run_query
    def test_update_item(self, mock_query):
        name = MagicMock()
        name.get.return_value = "Jane Doe"
        age = MagicMock()
        age.get.return_value = "25"
        phone = MagicMock()
        phone.get.return_value = "9876543210"

        update_item()  # Test update item functionality
        mock_query.assert_called_once_with(
            "UPDATE contacts SET name=?, age=?, phone=? WHERE phone=?",
            ("Jane Doe", 25, "9876543210", "9876543210")
        )

    @patch('Application.run_query')  # Mock run_query
    def test_delete_item(self, mock_query):
        delete_item()  # Test delete item functionality
        mock_query.assert_called_once_with("DELETE FROM contacts WHERE phone=?", ('9876543210',))

if __name__ == "__main__":
    unittest.main()
