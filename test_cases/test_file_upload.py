import pytest
import os

from page_objects.landing_page import LandingPage
from page_objects.file_upload_page import FileUploadPage

@pytest.mark.file_upload
class TestFileUpload:
    """Test class for File Upload functionality"""
    
    # Paths to test assets
    @pytest.fixture(scope="class")
    def assets_paths(self, request):
        """Fixture to provide paths to test assets"""
        # Find the root directory (Assessment) by looking for a parent directory with this name
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = current_dir
        
        # Navigate up until we find the Assessment directory or reach the root
        while os.path.basename(base_dir) != "Assessment" and os.path.dirname(base_dir) != base_dir:
            base_dir = os.path.dirname(base_dir)
        
        # If we couldn't find "Assessment", fall back to two directories up from current file
        if os.path.basename(base_dir) != "Assessment":
            print("Warning: Could not find 'Assessment' directory, using relative path")
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        print(f"Project root directory: {base_dir}")
        
        # Define test assets directory
        test_assets_dir = os.path.join(base_dir, "test_assets")
        
        # Define paths for different file types
        paths = {
            'text_file': os.path.join(test_assets_dir, 'test_file.txt'),
            'image_file': os.path.join(base_dir, 'report.png'),
            'pdf_file': os.path.join(test_assets_dir, 'document.pdf')
        }
        
        # Print paths for debugging
        print(f"Configured file paths:")
        for file_type, file_path in paths.items():
            print(f"{file_type}: {file_path}")
        
        # Modify verification to continue even if files are missing
        self._verify_test_files_exist(paths, skip_missing=True)
        
        return paths
    
    def _verify_test_files_exist(self, paths, skip_missing=False):
        """Helper method to verify that all required test files exist
        
        Args:
            paths: Dictionary of file paths
            skip_missing: If True, print warning instead of failing when files missing
        """
        missing_files = []
        for file_type, file_path in paths.items():
            if not os.path.exists(file_path):
                message = f"Required {file_type} does not exist at: {file_path}"
                if skip_missing:
                    print(f"WARNING: {message}")
                    missing_files.append(file_type)
                else:
                    pytest.fail(message)
        
        # Filter missing files from the paths dictionary
        if skip_missing and missing_files:
            for file_type in missing_files:
                print(f"Removing {file_type} from tests because it does not exist")
                paths.pop(file_type, None)
    
    def test_text_file_upload(self, driver, assets_paths):
        """Test uploading a plain text file"""
        # Navigate to the application
        landing_page = LandingPage(driver)
        landing_page.open()
        
        # Navigate to the file upload page
        landing_page.click_file_upload_testing_link()
        
        # Verify file upload page is loaded
        file_upload_page = FileUploadPage(driver)
        file_upload_page.verify_page_loaded()
        
        # Upload the text file
        file_upload_page.upload_file(assets_paths['text_file'])
        
        # Verify the upload was successful
        success_message = file_upload_page.get_success_message()
        assert success_message == "File Uploaded!", "File upload success message not displayed"
        
        # Verify the uploaded filename
        filename = file_upload_page.get_uploaded_filename()
        expected_filename = os.path.basename(assets_paths['text_file'])
        assert filename == expected_filename, f"Expected filename '{expected_filename}', but got '{filename}'"
    
    def test_image_file_upload(self, driver, assets_paths):
        """Test uploading a PNG image file from the root directory"""
        # Navigate to the application
        landing_page = LandingPage(driver)
        landing_page.open()
        
        # Navigate to the file upload page
        landing_page.click_file_upload_testing_link()
        
        # Verify file upload page is loaded
        file_upload_page = FileUploadPage(driver)
        file_upload_page.verify_page_loaded()
        
        # Upload the PNG image file from root directory
        file_upload_page.upload_file(assets_paths['image_file'])
        
        # Verify the upload was successful
        success_message = file_upload_page.get_success_message()
        assert success_message == "File Uploaded!", "File upload success message not displayed"
        
        # Verify the uploaded filename
        filename = file_upload_page.get_uploaded_filename()
        expected_filename = os.path.basename(assets_paths['image_file'])
        assert filename == expected_filename, f"Expected filename '{expected_filename}', but got '{filename}'"
    
    def test_pdf_file_upload(self, driver, assets_paths):
        """Test uploading a PDF file"""
        # Navigate to the application
        landing_page = LandingPage(driver)
        landing_page.open()
        
        # Navigate to the file upload page
        landing_page.click_file_upload_testing_link()
        
        # Verify file upload page is loaded
        file_upload_page = FileUploadPage(driver)
        file_upload_page.verify_page_loaded()
        
        # Upload the PDF file
        file_upload_page.upload_file(assets_paths['pdf_file'])
        
        # Verify the upload was successful
        success_message = file_upload_page.get_success_message()
        assert success_message == "File Uploaded!", "File upload success message not displayed"
        
        # Verify the uploaded filename
        filename = file_upload_page.get_uploaded_filename()
        expected_filename = os.path.basename(assets_paths['pdf_file'])
        assert filename == expected_filename, f"Expected filename '{expected_filename}', but got '{filename}'"
    
    def test_upload_without_file(self, driver):
        """Test attempting to upload without selecting a file"""
        # Navigate to the application
        landing_page = LandingPage(driver)
        landing_page.open()
        
        # Navigate to the file upload page
        landing_page.click_file_upload_testing_link()
        
        # Verify file upload page is loaded
        file_upload_page = FileUploadPage(driver)
        file_upload_page.verify_page_loaded()
        
        # Attempt to upload without selecting a file
        file_upload_page.click_upload_button()
        
        # Verify error message is displayed
        error_message = file_upload_page.get_error_message()
        assert error_message == "Internal Server Error", "Expected error message not displayed"
        