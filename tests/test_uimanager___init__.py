import pytest
import pygame
from unittest.mock import MagicMock

# Assuming settings.py and ui_manager.py are in the python path
import settings
from ui_manager import UIManager


@pytest.fixture
def mock_pygame_essentials(mocker):
    # Mock pygame initialization functions
    mocker.patch('pygame.init')
    mocker.patch('pygame.font.init')

    # Store the original pygame.font.Font class BEFORE it's patched
    # This ensures we use the actual class for speccing, not a mock of it.
    original_pygame_font_class = pygame.font.Font

    # Mock font constructors to return MagicMock instances,
    # speccing them against the original pygame.font.Font class.
    mock_font_constructor = mocker.patch(
        'pygame.font.Font',
        return_value=MagicMock(spec=original_pygame_font_class)
    )
    # pygame.font.SysFont also returns a font object, so speccing against
    # original_pygame_font_class is appropriate here too.
    mock_sysfont_constructor = mocker.patch(
        'pygame.font.SysFont',
        return_value=MagicMock(spec=original_pygame_font_class)
    )

    # Mock the built-in print function to check for warning messages
    mock_print_function = mocker.patch('builtins.print')

    # Ensure pygame.error is a valid exception type that can be raised by mocks
    # and caught in try-except blocks in the code under test.
    # This is important as pygame.init() (which might set up pygame.error) is mocked.
    if not hasattr(pygame, 'error') or not (isinstance(pygame.error, type) and issubclass(pygame.error, Exception)):
        # If pygame.error isn't a usable exception class (e.g., it's None or not an exception type),
        # create a mock one for the tests.
        pygame.error = type('MockPygameError', (Exception,), {})

    return mock_font_constructor, mock_sysfont_constructor, mock_print_function


# --- CORRECTED TEST FUNCTIONS ---

def test_init_default_args_uses_sysfont(mock_pygame_essentials):  # Corresponds to Plan Test 1
    # Test UIManager initialization with default arguments (font_name is None)
    # EXPECTS pygame.font.Font(None, ...) to be called
    mock_font_constructor, mock_sysfont_constructor, _ = mock_pygame_essentials

    ui_manager = UIManager()  # Uses default font_name=None and font_size=36

    # Assertions
    # Check that pygame.font.Font was called with None for font_name
    assert mock_font_constructor.call_count == 3
    mock_font_constructor.assert_any_call(None, 36)  # For default_font
    mock_font_constructor.assert_any_call(None, 48)  # For medium_font
    mock_font_constructor.assert_any_call(None, 72)  # For large_font

    # Ensure pygame.font.SysFont constructor was NOT called (because Font(None,...) succeeds)
    assert mock_sysfont_constructor.call_count == 0

    # Verify other attributes are set correctly
    assert ui_manager.text_color == settings.WHITE
    assert ui_manager.screen_width == settings.SCREEN_WIDTH
    assert ui_manager.screen_height == settings.SCREEN_HEIGHT
    assert ui_manager.default_font is not None  # Check font objects were assigned
    assert ui_manager.medium_font is not None
    assert ui_manager.large_font is not None


def test_init_custom_font_size_and_color_with_sysfont(mock_pygame_essentials):  # Corresponds to Plan Test 4
    # Test initialization with custom font_size and text_color, (font_name is None)
    # EXPECTS pygame.font.Font(None, ...) to be called
    mock_font_constructor, mock_sysfont_constructor, _ = mock_pygame_essentials
    custom_size = 24
    custom_color = (100, 100, 100)  # A custom color

    ui_manager = UIManager(font_size=custom_size, text_color=custom_color)  # font_name is None

    # Assertions
    # pygame.font.Font is used with None; default_font gets custom_size, others get fixed sizes
    assert mock_font_constructor.call_count == 3
    mock_font_constructor.assert_any_call(None, custom_size)  # For default_font
    mock_font_constructor.assert_any_call(None, 48)  # For medium_font
    mock_font_constructor.assert_any_call(None, 72)  # For large_font

    # Ensure pygame.font.SysFont was NOT called
    assert mock_sysfont_constructor.call_count == 0

    assert ui_manager.text_color == custom_color  # Custom color should be set


# --- UNCHANGED TEST FUNCTIONS (already passing and correct) ---

def test_init_valid_custom_font_uses_font(mock_pygame_essentials):  # Corresponds to Plan Test 2
    # Test UIManager initialization with a valid custom font name
    mock_font_constructor, mock_sysfont_constructor, _ = mock_pygame_essentials
    custom_font_name = "custom_font.ttf"

    ui_manager = UIManager(font_name=custom_font_name)  # Uses default font_size=36

    # Assertions
    # Check that the custom pygame.font.Font constructor was called for all three fonts
    assert mock_font_constructor.call_count == 3
    mock_font_constructor.assert_any_call(custom_font_name, 36)  # For default_font
    mock_font_constructor.assert_any_call(custom_font_name, 48)  # For medium_font
    mock_font_constructor.assert_any_call(custom_font_name, 72)  # For large_font

    # Ensure SysFont constructor was not called
    assert not mock_sysfont_constructor.called

    assert ui_manager.text_color == settings.WHITE  # Default color


def test_init_invalid_custom_font_filenotfound_falls_back_to_sysfont(
        mock_pygame_essentials):  # Corresponds to Plan Test 3 (FileNotFound part)
    # Test fallback to SysFont when custom font file is not found
    mock_font_constructor, mock_sysfont_constructor, mock_print = mock_pygame_essentials
    # Configure the custom font constructor mock to raise FileNotFoundError
    mock_font_constructor.side_effect = FileNotFoundError("Font not found for test")

    invalid_font_name = "invalid_font.ttf"
    UIManager(font_name=invalid_font_name)

    # Assertions
    # Custom font constructor should have been attempted (it's called first for default_font)
    assert mock_font_constructor.called

    # SysFont should be called as a fallback for all three font attributes
    assert mock_sysfont_constructor.call_count == 3
    mock_sysfont_constructor.assert_any_call("arial", 36)  # Check one of the fallback calls

    # Verify that a warning message was printed
    mock_print.assert_called_once_with(
        f"Warning: Font '{invalid_font_name}' not found or error loading. Using system 'arial'."
    )


def test_init_pygame_error_on_font_load_falls_back_to_sysfont(
        mock_pygame_essentials):  # Corresponds to Plan Test 3 (pygame.error part)
    # Test fallback to SysFont when pygame.error occurs during custom font loading
    mock_font_constructor, mock_sysfont_constructor, mock_print = mock_pygame_essentials
    # Configure the custom font constructor mock to raise pygame.error
    # Ensure pygame.error is the one expected by the code under test
    mock_font_constructor.side_effect = pygame.error("Pygame font error for test")

    error_font_name = "error_font.ttf"
    UIManager(font_name=error_font_name)

    # Assertions
    assert mock_font_constructor.called  # Custom font constructor was attempted

    # SysFont should be used as a fallback for all three fonts
    assert mock_sysfont_constructor.call_count == 3
    mock_sysfont_constructor.assert_any_call("arial", 36)  # Check one fallback call

    # Verify that a warning message was printed
    mock_print.assert_called_once_with(
        f"Warning: Font '{error_font_name}' not found or error loading. Using system 'arial'."
    )


def test_init_valid_custom_font_with_custom_size_and_color(mock_pygame_essentials):
    # Test initialization with a valid custom font, custom size, and custom color
    mock_font_constructor, mock_sysfont_constructor, _ = mock_pygame_essentials
    custom_font_name = "another_custom.ttf"
    custom_size = 20
    custom_color = (50, 150, 200)  # A custom color

    ui_manager = UIManager(font_name=custom_font_name, font_size=custom_size, text_color=custom_color)

    # Assertions
    # Custom font constructor used; default_font gets custom_size, others get fixed sizes with custom font
    assert mock_font_constructor.call_count == 3
    mock_font_constructor.assert_any_call(custom_font_name, custom_size)  # For default_font
    mock_font_constructor.assert_any_call(custom_font_name, 48)  # For medium_font
    mock_font_constructor.assert_any_call(custom_font_name, 72)  # For large_font

    assert not mock_sysfont_constructor.called  # SysFont constructor not used

    assert ui_manager.text_color == custom_color  # Custom color should be set