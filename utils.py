"""
Enhanced utility functions for the Hybrid Quantum AI Chatbot
Provides file management, logging, and system utilities
"""

import os
import time
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def timestamp(format_type: str = "standard") -> str:
    """
    Generate timestamp in various formats.
    
    Args:
        format_type: Type of timestamp format
                    - "standard": YYYY-MM-DD HH:MM:SS
                    - "iso": ISO 8601 format
                    - "filename": Safe for filenames
                    - "unix": Unix timestamp
    
    Returns:
        Formatted timestamp string
    """
    now = datetime.now(timezone.utc)
    
    formats = {
        "standard": "%Y-%m-%d %H:%M:%S",
        "iso": "%Y-%m-%dT%H:%M:%S.%fZ",
        "filename": "%Y%m%d_%H%M%S",
        "unix": str(int(now.timestamp()))
    }
    
    if format_type in formats:
        if format_type == "unix":
            return formats[format_type]
        return now.strftime(formats[format_type])
    else:
        logger.warning(f"Unknown timestamp format: {format_type}, using standard")
        return now.strftime(formats["standard"])

def ensure_static_dir(base_path: str = "static") -> str:
    """
    Ensure that the static directory exists with proper subdirectories.
    
    Args:
        base_path: Base directory path
    
    Returns:
        Path to the created directory
    """
    try:
        # Create main static directory
        static_path = Path(base_path)
        static_path.mkdir(exist_ok=True)
        
        # Create subdirectories for different content types
        subdirs = ["circuits", "plots", "exports", "temp"]
        
        for subdir in subdirs:
            subdir_path = static_path / subdir
            subdir_path.mkdir(exist_ok=True)
        
        # Create .gitkeep files to ensure directories are tracked
        gitkeep_content = "# This file ensures the directory is tracked by git\n"
        for subdir in subdirs:
            gitkeep_path = static_path / subdir / ".gitkeep"
            if not gitkeep_path.exists():
                gitkeep_path.write_text(gitkeep_content)
        
        logger.info(f"Static directory structure ensured at: {static_path.absolute()}")
        return str(static_path)
        
    except Exception as e:
        logger.error(f"Failed to create static directory: {e}")
        # Fallback to current directory
        return "."

def safe_filename(filename: str, max_length: int = 100) -> str:
    """
    Create a safe filename by removing/replacing problematic characters.
    
    Args:
        filename: Original filename
        max_length: Maximum length for the filename
    
    Returns:
        Safe filename string
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    safe_name = filename
    
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Replace multiple consecutive underscores with single underscore
    while '__' in safe_name:
        safe_name = safe_name.replace('__', '_')
    
    # Remove leading/trailing underscores and dots
    safe_name = safe_name.strip('_.')
    
    # Ensure it's not empty
    if not safe_name:
        safe_name = f"file_{timestamp('filename')}"
    
    # Truncate if too long, but preserve file extension
    if len(safe_name) > max_length:
        name_part, ext = os.path.splitext(safe_name)
        available_length = max_length - len(ext)
        safe_name = name_part[:available_length] + ext
    
    return safe_name

def generate_session_id() -> str:
    """
    Generate a unique session ID for tracking user sessions.
    
    Returns:
        Unique session identifier
    """
    # Combine timestamp and random data for uniqueness
    session_data = f"{time.time()}_{os.urandom(16).hex()}"
    session_hash = hashlib.sha256(session_data.encode()).hexdigest()
    return session_hash[:16]  # Return first 16 characters

class FileManager:
    """Enhanced file management for the application"""
    
    def __init__(self, base_dir: str = "static"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
    def save_json(self, data: Dict[Any, Any], filename: str, 
                  subdir: str = "exports") -> str:
        """
        Save data as JSON file.
        
        Args:
            data: Data to save
            filename: Name of the file
            subdir: Subdirectory within base_dir
        
        Returns:
            Path to saved file
        """
        try:
            file_path = self.base_dir / subdir / safe_filename(filename)
            file_path.parent.mkdir(exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON data saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save JSON file: {e}")
            raise

    def save_text(self, content: str, filename: str, 
                  subdir: str = "exports") -> str:
        """
        Save text content to file.
        
        Args:
            content: Text content to save
            filename: Name of the file
            subdir: Subdirectory within base_dir
        
        Returns:
            Path to saved file
        """
        try:
            file_path = self.base_dir / subdir / safe_filename(filename)
            file_path.parent.mkdir(exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Text content saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save text file: {e}")
            raise

    def list_files(self, subdir: str = "", pattern: str = "*") -> List[str]:
        """
        List files in a directory.
        
        Args:
            subdir: Subdirectory to search in
            pattern: File pattern to match
        
        Returns:
            List of file paths
        """
        try:
            search_dir = self.base_dir / subdir if subdir else self.base_dir
            
            if search_dir.exists():
                files = list(search_dir.glob(pattern))
                return [str(f.relative_to(self.base_dir)) for f in files if f.is_file()]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []

    def cleanup_old_files(self, subdir: str = "temp", max_age_hours: int = 24):
        """
        Clean up old files from a directory.
        
        Args:
            subdir: Subdirectory to clean
            max_age_hours: Maximum age of files to keep (in hours)
        """
        try:
            cleanup_dir = self.base_dir / subdir
            if not cleanup_dir.exists():
                return
            
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            cleaned_count = 0
            for file_path in cleanup_dir.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age_seconds:
                        file_path.unlink()
                        cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old files from {cleanup_dir}")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old files: {e}")

class ConfigManager:
    """Configuration management for the application"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return {}
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        default_config = {
            "app": {
                "title": "Hybrid Quantum AI Chatbot",
                "version": "1.0.0",
                "debug": False
            },
            "llm": {
                "default_provider": "openrouter",
                "max_tokens": 512,
                "temperature": 0.7,
                "timeout": 30
            },
            "quantum": {
                "max_qubits": 12,
                "default_shots": 1024,
                "enable_visualization": True
            },
            "ui": {
                "theme": "light",
                "show_quantum_stats": True,
                "auto_save_conversations": False
            }
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            logger.info(f"Default configuration created: {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to create default config: {e}")
        
        return default_config
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value (e.g., "llm.max_tokens")
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        try:
            keys = key_path.split('.')
            value = self.config
            
            for key in keys:
                value = value[key]
            
            return value
            
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value
            value: Value to set
        
        Returns:
            True if successful, False otherwise
        """
        try:
            keys = key_path.split('.')
            config_ref = self.config
            
            # Navigate to parent of target key
            for key in keys[:-1]:
                if key not in config_ref:
                    config_ref[key] = {}
                config_ref = config_ref[key]
            
            # Set the value
            config_ref[keys[-1]] = value
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Configuration updated: {key_path} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set configuration: {e}")
            return False

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_system_info() -> Dict[str, Any]:
    """
    Get system information for debugging and monitoring.
    
    Returns:
        Dictionary with system information
    """
    try:
        import platform
        import psutil
        
        return {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "python_version": platform.python_version()
            },
            "memory": {
                "total": format_file_size(psutil.virtual_memory().total),
                "available": format_file_size(psutil.virtual_memory().available),
                "used_percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": format_file_size(psutil.disk_usage('/').total),
                "free": format_file_size(psutil.disk_usage('/').free),
                "used_percent": psutil.disk_usage('/').percent
            },
            "timestamp": timestamp("iso")
        }
        
    except ImportError:
        # Fallback if psutil is not available
        import platform
        return {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "python_version": platform.python_version()
            },
            "timestamp": timestamp("iso"),
            "note": "Full system info requires 'psutil' package"
        }

# Global instances for easy access
file_manager = FileManager()
config_manager = ConfigManager()