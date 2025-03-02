import os
import shutil
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'cache_cleanup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def is_system_critical(path):
    """Check if the path is in system-critical locations."""
    critical_paths = [
        r"C:\Windows\System32",
        r"C:\Windows\SysWOW64",
        r"C:\Program Files",
        r"C:\Program Files (x86)"
    ]
    return any(path.startswith(critical_path) for critical_path in critical_paths)

def clean_cache_folders(drive="C:"):
    """
    Recursively find and delete Cache/cache folders from the specified drive.
    """
    total_cleaned = 0
    total_size_freed = 0

    logging.info(f"Starting cache cleanup on drive {drive}")

    for root, dirs, _ in os.walk(drive, topdown=True):
        # Remove system critical paths from dirs to prevent recursion into them
        dirs[:] = [d for d in dirs if not is_system_critical(os.path.join(root, d))]
        
        for dir_name in dirs[:]:  # Create a copy of the list to modify during iteration
            if dir_name.lower() == "cache":
                full_path = os.path.join(root, dir_name)
                
                try:
                    # Get folder size before deletion
                    folder_size = sum(
                        os.path.getsize(os.path.join(dirpath, filename))
                        for dirpath, _, filenames in os.walk(full_path)
                        for filename in filenames
                    )
                    
                    # Try to remove the folder
                    shutil.rmtree(full_path)
                    
                    total_cleaned += 1
                    total_size_freed += folder_size
                    logging.info(f"Successfully deleted: {full_path}")
                    logging.info(f"Freed space: {folder_size / (1024*1024):.2f} MB")
                    
                    # Remove the directory from dirs to prevent further recursion
                    dirs.remove(dir_name)
                    
                except PermissionError:
                    logging.warning(f"Permission denied: {full_path}")
                except Exception as e:
                    logging.error(f"Error deleting {full_path}: {str(e)}")

    # Log summary
    logging.info("Cleanup completed!")
    logging.info(f"Total folders cleaned: {total_cleaned}")
    logging.info(f"Total space freed: {total_size_freed / (1024*1024):.2f} MB")
    
    return total_cleaned, total_size_freed

if __name__ == "__main__":
    try:
        clean_cache_folders()
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
