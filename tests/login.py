import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))

from PyQt5 import QtWidgets, QtTest, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox

# Mockea los módulos necesarios antes de importar LoginView
with patch.dict('sys.modules', {
    'app.database.auth.auth': Mock(),
    'app.views.management.inventoryMainView': Mock()
}):
    from app.views.auth.LoginView import LoginView

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

# Mock para authData - ahora apunta a la ubicación CORRECTA donde está definida
@pytest.fixture
def mock_auth_data():
    with patch('app.database.auth.auth.authData') as mock:
        yield mock

# Mock para inventoryMainView
@pytest.fixture
def mock_inventory_view():
    with patch('app.views.auth.LoginView.inventoryMainView') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def login_view(qapp, mock_auth_data, mock_inventory_view):
    view = LoginView()
    yield view
    view.close()

class TestLoginView:
    
    def test_initialization(self, login_view):
        """Test que verifica la inicialización correcta del componente"""
        assert login_view.windowTitle() == "Autenticación"
        assert hasattr(login_view, 'cedulaField')
        assert hasattr(login_view, 'passwordField')
        assert hasattr(login_view, 'accessButtom')
    
    @pytest.mark.parametrize("cedula,password,auth_result,expected_message", [
        ("", "password123", None, "Por favor ingrese su cédula"),
        ("12345678", "", None, "Por favor ingrese su contraseña"),
        ("12345678", "wrongpass", False, "Usuario no encontrado"),
        ("31034826", "12345678", True, None),  # Caso exitoso
    ])
    def test_handle_login_validation(
        self, login_view, mock_auth_data, mock_inventory_view, 
        cedula, password, auth_result, expected_message
    ):
        """Test de validaciones y diferentes escenarios de login"""
        mock_auth_data.return_value = auth_result
        
        # Configurar campos
        login_view.cedulaField.setText(cedula)
        login_view.passwordField.setText(password)
        
        # Mock para QMessageBox
        with patch.object(QtWidgets.QMessageBox, 'warning') as mock_warning:
            login_view.handleLogin()
            
            if expected_message:
                # Verificar que se muestra el mensaje de error
                mock_warning.assert_called_once()
                args = mock_warning.call_args[0]
                assert args[2] == expected_message
            else:
                # Verificar que no hay mensaje de error y se abre la ventana
                mock_warning.assert_not_called()
                mock_inventory_view.return_value.showMaximized.assert_called_once()
    
    def test_successful_login_opens_inventory(self, login_view, mock_auth_data, mock_inventory_view):
        """Test de login exitoso"""
        mock_auth_data.return_value = True
        
        login_view.cedulaField.setText("31034826")
        login_view.passwordField.setText("12345678")
        
        print("=== ANTES de handleLogin ===")
        print(f"authData mock return value: {mock_auth_data.return_value}")
        
        login_view.handleLogin()
        
        print("=== DESPUÉS de handleLogin ===")
        print(f"authData called: {mock_auth_data.called}")
        print(f"authData call args: {mock_auth_data.call_args}")
        print(f"inventoryMainView called: {mock_inventory_view.called}")
        print(f"showMaximized called: {mock_inventory_view.return_value.showMaximized.called}")
        
        # Assertions - CORREGIDOS
        mock_auth_data.assert_called_once_with("31034826", "12345678")
        mock_inventory_view.assert_called_once()
        mock_inventory_view.return_value.showMaximized.assert_called_once()
