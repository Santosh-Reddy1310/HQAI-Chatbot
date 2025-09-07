"""
Streamlit Secrets Configuration Reader
Handles reading configuration from both Streamlit secrets and environment variables
"""

import os
import streamlit as st
from typing import Any, Optional

def get_config_value(key: str, default: Any = None, section: Optional[str] = None) -> Any:
    """
    Get configuration value from Streamlit secrets or environment variables.
    
    Args:
        key: Configuration key name
        default: Default value if not found
        section: TOML section name (for Streamlit secrets)
    
    Returns:
        Configuration value or default
    """
    try:
        # Try Streamlit secrets first
        if hasattr(st, 'secrets'):
            if section:
                # Access nested section: st.secrets[section][key]
                if section in st.secrets and key in st.secrets[section]:
                    return st.secrets[section][key]
            else:
                # Direct access: st.secrets[key] or st.secrets.env_vars[key]
                if key in st.secrets:
                    return st.secrets[key]
                elif "env_vars" in st.secrets and key in st.secrets["env_vars"]:
                    return st.secrets["env_vars"][key]
    except Exception:
        pass  # Fall back to environment variables
    
    # Fall back to environment variables
    env_value = os.getenv(key, default)
    
    # Convert string booleans to actual booleans
    if isinstance(env_value, str):
        if env_value.lower() in ['true', '1', 'yes', 'on']:
            return True
        elif env_value.lower() in ['false', '0', 'no', 'off']:
            return False
        elif env_value.isdigit():
            return int(env_value)
        elif env_value.replace('.', '').isdigit():
            return float(env_value)
    
    return env_value

def get_llm_config() -> dict:
    """Get LLM configuration from secrets or environment"""
    return {
        'provider': get_config_value('provider', 'openrouter', 'llm') or 
                   get_config_value('LLM_PROVIDER', 'openrouter'),
        'openrouter_key': get_config_value('openrouter_api_key', section='llm') or 
                         get_config_value('OPENROUTER_API_KEY'),
        'gemini_key': get_config_value('gemini_api_key', section='llm') or 
                     get_config_value('GEMINI_API_KEY'),
        'groq_key': get_config_value('groq_api_key', section='llm') or 
                   get_config_value('GROQ_API_KEY'),
        'max_tokens': get_config_value('default_max_tokens', 512, 'llm.settings') or 
                     get_config_value('DEFAULT_MAX_TOKENS', 512),
        'temperature': get_config_value('default_temperature', 0.7, 'llm.settings') or 
                      get_config_value('DEFAULT_TEMPERATURE', 0.7),
        'timeout': get_config_value('request_timeout', 30, 'llm.settings') or 
                  get_config_value('REQUEST_TIMEOUT', 30),
        'max_retries': get_config_value('max_retries', 3, 'llm.settings') or 
                      get_config_value('MAX_RETRIES', 3)
    }

def get_quantum_config() -> dict:
    """Get quantum computing configuration"""
    return {
        'max_qubits': get_config_value('max_qubits', 12, 'quantum') or 
                     get_config_value('QUANTUM_MAX_QUBITS', 12),
        'default_shots': get_config_value('default_shots', 1024, 'quantum') or 
                        get_config_value('QUANTUM_DEFAULT_SHOTS', 1024),
        'enable_visualization': get_config_value('enable_visualization', True, 'quantum') or 
                               get_config_value('QUANTUM_ENABLE_VISUALIZATION', True)
    }

def get_app_config() -> dict:
    """Get application configuration"""
    return {
        'debug': get_config_value('debug', False, 'app') or 
                get_config_value('APP_DEBUG', False),
        'log_level': get_config_value('log_level', 'INFO', 'app') or 
                    get_config_value('APP_LOG_LEVEL', 'INFO'),
        'title': get_config_value('title', 'Hybrid Quantum AI Chatbot', 'app') or 
                get_config_value('APP_TITLE', 'Hybrid Quantum AI Chatbot'),
        'theme': get_config_value('theme', 'light', 'app') or 
                get_config_value('THEME', 'light')
    }

def get_ui_config() -> dict:
    """Get UI configuration"""
    return {
        'show_quantum_stats': get_config_value('show_quantum_stats', True, 'ui') or 
                             get_config_value('SHOW_QUANTUM_STATS', True),
        'show_error_log': get_config_value('show_error_log', False, 'ui') or 
                         get_config_value('SHOW_ERROR_LOG', False)
    }

def get_performance_config() -> dict:
    """Get performance configuration"""
    return {
        'max_history_length': get_config_value('max_history_length', 50, 'performance') or 
                             get_config_value('MAX_HISTORY_LENGTH', 50),
        'enable_caching': get_config_value('enable_response_caching', False, 'performance') or 
                         get_config_value('ENABLE_RESPONSE_CACHING', False),
        'cache_ttl': get_config_value('cache_ttl_minutes', 30, 'performance') or 
                    get_config_value('CACHE_TTL_MINUTES', 30)
    }

# Global configuration objects
LLM_CONFIG = get_llm_config()
QUANTUM_CONFIG = get_quantum_config()
APP_CONFIG = get_app_config()
UI_CONFIG = get_ui_config()
PERFORMANCE_CONFIG = get_performance_config()

# Backward compatibility - maintain the same interface
LLM_PROVIDER = LLM_CONFIG['provider']
OPENROUTER_KEY = LLM_CONFIG['openrouter_key']
GEMINI_KEY = LLM_CONFIG['gemini_key']
GROQ_KEY = LLM_CONFIG['groq_key']