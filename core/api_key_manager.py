#!/usr/bin/env python3
"""
API Key Manager - Persistent Encrypted Storage
Solves the recurring API key loss problem

Features:
- Encrypted storage of API keys
- Automatic backup and recovery
- Validation of keys
- Integration with bootstrap

Usage:
    python3 api_key_manager.py save      # Save current environment keys
    python3 api_key_manager.py load      # Load keys into environment
    python3 api_key_manager.py validate  # Test all keys
    python3 api_key_manager.py update APOLLO_API_KEY new_value
"""

import os
import sys
import json
import base64
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple
from cryptography.fernet import Fernet


class APIKeyManager:
    """Manages API keys with encrypted persistent storage"""
    
    # Keys to manage
    MANAGED_KEYS = [
        'OPENAI_API_KEY',
        'OPENAI_API_BASE',
        'APOLLO_API_KEY',
        # Add more as needed
    ]
    
    def __init__(self):
        """Initialize API Key Manager"""
        self.home = Path.home()
        self.secrets_file = self.home / '.manus_secrets.enc'
        self.backup_dir = self.home / '.manus_secrets_backup'
        self.backup_dir.mkdir(exist_ok=True)
        self.audit_log = self.home / '.manus_secrets_audit.jsonl'
        
        # Generate encryption key from sandbox-specific data
        self.encryption_key = self._generate_encryption_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _generate_encryption_key(self) -> bytes:
        """
        Generate encryption key from sandbox-specific identifier using PBKDF2
        
        Uses PBKDF2-HMAC-SHA256 with 100,000 iterations (NIST recommendation)
        to derive a strong encryption key from sandbox-specific data.
        
        Returns:
            Encryption key bytes
        """
        # Use hostname + user as seed (sandbox-specific)
        import socket
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        seed = f"{socket.gethostname()}-{os.getuid()}-manus-secrets"
        
        # Fixed salt (acceptable for this use case as seed is already unique per sandbox)
        salt = b'manus-secrets-salt-v1'
        
        # Use PBKDF2 with 100,000 iterations (NIST SP 800-132 recommendation)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes = 256 bits
            salt=salt,
            iterations=100000,
        )
        
        key_material = kdf.derive(seed.encode())
        
        # Encode for Fernet (base64)
        return base64.urlsafe_b64encode(key_material)
    
    def _log_access(self, operation: str, success: bool, **metadata):
        """
        Log access to secrets for audit trail
        
        Args:
            operation: Operation performed (save, load, update, validate, etc.)
            success: Whether operation succeeded
            **metadata: Additional metadata to log
        """
        import socket
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'success': success,
            'user': os.getenv('USER', 'unknown'),
            'hostname': socket.gethostname(),
            **metadata
        }
        
        try:
            # Append to audit log
            with open(self.audit_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            # Set permissions on first write
            if self.audit_log.stat().st_size == len(json.dumps(log_entry)) + 1:
                os.chmod(self.audit_log, 0o600)
        except Exception:
            # Don't fail operation if logging fails
            pass
    
    def save_keys(self, keys: Optional[Dict[str, str]] = None) -> Tuple[bool, str]:
        """
        Save API keys to encrypted file
        
        Args:
            keys: Dict of key names to values (if None, read from environment)
            
        Returns:
            (success, message)
        """
        try:
            # Get keys from environment if not provided
            if keys is None:
                keys = {}
                for key_name in self.MANAGED_KEYS:
                    value = os.environ.get(key_name)
                    if value:
                        keys[key_name] = value
            
            if not keys:
                return (False, "No keys to save")
            
            # Add metadata
            data = {
                'keys': keys,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            # Serialize to JSON
            json_data = json.dumps(data)
            
            # Encrypt
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            # Write to file
            self.secrets_file.write_bytes(encrypted_data)
            
            # Set restrictive permissions
            os.chmod(self.secrets_file, 0o600)
            
            # Log successful save
            self._log_access('save', True, keys_saved=len(keys), key_names=list(keys.keys()))
            
            return (True, f"Saved {len(keys)} keys to {self.secrets_file}")
        
        except Exception as e:
            # Log failed save
            self._log_access('save', False, error=str(e))
            return (False, f"Error saving keys: {e}")
    
    def load_keys(self) -> Tuple[bool, Dict[str, str], str]:
        """
        Load API keys from encrypted file
        
        Returns:
            (success, keys_dict, message)
        """
        try:
            if not self.secrets_file.exists():
                return (False, {}, "No saved keys found")
            
            # Read encrypted file
            encrypted_data = self.secrets_file.read_bytes()
            
            # Decrypt
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Parse JSON
            data = json.loads(decrypted_data.decode())
            
            keys = data.get('keys', {})
            timestamp = data.get('timestamp', 'unknown')
            
            # Log successful load
            self._log_access('load', True, keys_loaded=len(keys), key_names=list(keys.keys()))
            
            return (True, keys, f"Loaded {len(keys)} keys (saved: {timestamp})")
        
        except Exception as e:
            # Log failed load
            self._log_access('load', False, error=str(e))
            return (False, {}, f"Error loading keys: {e}")
    
    def load_keys_to_environment(self) -> Tuple[bool, str]:
        """
        Load keys from file and set as environment variables
        
        Returns:
            (success, message)
        """
        success, keys, msg = self.load_keys()
        
        if not success:
            return (False, msg)
        
        # Set environment variables
        for key_name, value in keys.items():
            os.environ[key_name] = value
        
        return (True, f"Loaded {len(keys)} keys into environment")
    
    def update_key(self, key_name: str, value: str) -> Tuple[bool, str]:
        """
        Update a specific API key
        
        Args:
            key_name: Name of the key (e.g., 'APOLLO_API_KEY')
            value: New value
            
        Returns:
            (success, message)
        """
        # Load existing keys
        success, keys, _ = self.load_keys()
        
        if not success:
            keys = {}
        
        # Update key
        keys[key_name] = value
        
        # Save
        return self.save_keys(keys)
    
    def validate_keys(self) -> Dict[str, Dict[str, any]]:
        """
        Validate all saved API keys
        
        Returns:
            Dict of key_name -> {valid: bool, message: str}
        """
        results = {}
        
        # Load keys
        success, keys, msg = self.load_keys()
        
        if not success:
            return {'error': {'valid': False, 'message': msg}}
        
        # Validate each key
        for key_name, value in keys.items():
            if key_name == 'OPENAI_API_KEY':
                results[key_name] = self._validate_openai_key(value)
            elif key_name == 'APOLLO_API_KEY':
                results[key_name] = self._validate_apollo_key(value)
            else:
                results[key_name] = {'valid': True, 'message': 'No validation available'}
        
        return results
    
    def _validate_openai_key(self, api_key: str) -> Dict[str, any]:
        """Validate OpenAI API key"""
        try:
            import requests
            
            response = requests.get(
                'https://api.openai.com/v1/models',
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=10
            )
            
            if response.status_code == 200:
                return {'valid': True, 'message': 'OpenAI API key is valid'}
            elif response.status_code == 401:
                return {'valid': False, 'message': 'OpenAI API key is invalid'}
            else:
                return {'valid': False, 'message': f'OpenAI API returned status {response.status_code}'}
        
        except Exception as e:
            return {'valid': False, 'message': f'Error validating OpenAI key: {e}'}
    
    def _validate_apollo_key(self, api_key: str) -> Dict[str, any]:
        """Validate Apollo API key"""
        try:
            import requests
            
            response = requests.get(
                'https://api.apollo.io/v1/auth/health',
                headers={'X-Api-Key': api_key},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('healthy') and data.get('is_logged_in'):
                    return {'valid': True, 'message': 'Apollo API key is valid'}
                else:
                    return {'valid': False, 'message': 'Apollo API key is invalid or not logged in'}
            else:
                return {'valid': False, 'message': f'Apollo API returned status {response.status_code}'}
        
        except Exception as e:
            return {'valid': False, 'message': f'Error validating Apollo key: {e}'}
    
    def backup_keys(self) -> Tuple[bool, str]:
        """
        Create a timestamped backup of current keys
        
        Returns:
            (success, message)
        """
        try:
            if not self.secrets_file.exists():
                return (False, "No keys to backup")
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'secrets_backup_{timestamp}.enc'
            
            # Copy encrypted file
            import shutil
            shutil.copy2(self.secrets_file, backup_file)
            
            # Set permissions
            os.chmod(backup_file, 0o600)
            
            return (True, f"Backup created: {backup_file}")
        
        except Exception as e:
            return (False, f"Error creating backup: {e}")
    
    def restore_from_backup(self, backup_file: str) -> Tuple[bool, str]:
        """
        Restore keys from a backup file
        
        Args:
            backup_file: Path to backup file
            
        Returns:
            (success, message)
        """
        try:
            backup_path = Path(backup_file)
            
            if not backup_path.exists():
                return (False, f"Backup file not found: {backup_file}")
            
            # Copy backup to secrets file
            import shutil
            shutil.copy2(backup_path, self.secrets_file)
            
            # Set permissions
            os.chmod(self.secrets_file, 0o600)
            
            return (True, f"Restored from backup: {backup_file}")
        
        except Exception as e:
            return (False, f"Error restoring from backup: {e}")
    
    def list_backups(self) -> list:
        """
        List all available backups
        
        Returns:
            List of backup file paths
        """
        backups = sorted(self.backup_dir.glob('secrets_backup_*.enc'), reverse=True)
        return [str(b) for b in backups]


def main():
    """CLI interface"""
    manager = APIKeyManager()
    
    if len(sys.argv) < 2:
        print("Usage: python3 api_key_manager.py <command> [args]")
        print()
        print("Commands:")
        print("  save                    - Save current environment keys")
        print("  load                    - Load keys into environment")
        print("  validate                - Validate all saved keys")
        print("  update <key> <value>    - Update a specific key")
        print("  backup                  - Create a backup")
        print("  restore <backup_file>   - Restore from backup")
        print("  list-backups            - List all backups")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'save':
        success, msg = manager.save_keys()
        print(msg)
        sys.exit(0 if success else 1)
    
    elif command == 'load':
        success, msg = manager.load_keys_to_environment()
        print(msg)
        
        if success:
            # Print export commands for shell sourcing
            _, keys, _ = manager.load_keys()
            for key_name, value in keys.items():
                print(f"export {key_name}='{value}'")
        
        sys.exit(0 if success else 1)
    
    elif command == 'validate':
        results = manager.validate_keys()
        
        print("="*70)
        print("API KEY VALIDATION")
        print("="*70)
        print()
        
        all_valid = True
        for key_name, result in results.items():
            status = "✅" if result['valid'] else "❌"
            print(f"{status} {key_name}: {result['message']}")
            if not result['valid']:
                all_valid = False
        
        print()
        sys.exit(0 if all_valid else 1)
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Usage: python3 api_key_manager.py update <key> <value>")
            sys.exit(1)
        
        key_name = sys.argv[2]
        value = sys.argv[3]
        
        success, msg = manager.update_key(key_name, value)
        print(msg)
        sys.exit(0 if success else 1)
    
    elif command == 'backup':
        success, msg = manager.backup_keys()
        print(msg)
        sys.exit(0 if success else 1)
    
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Usage: python3 api_key_manager.py restore <backup_file>")
            sys.exit(1)
        
        backup_file = sys.argv[2]
        success, msg = manager.restore_from_backup(backup_file)
        print(msg)
        sys.exit(0 if success else 1)
    
    elif command == 'list-backups':
        backups = manager.list_backups()
        
        if backups:
            print("Available backups:")
            for backup in backups:
                print(f"  - {backup}")
        else:
            print("No backups found")
        
        sys.exit(0)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
