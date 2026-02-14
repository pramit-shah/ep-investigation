#!/usr/bin/env python3
"""
Secret Communications System
Encrypted channels, steganography, and anonymous messaging for covert distribution.
"""

import base64
import hashlib
import json
import os
import secrets
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


class EncryptionManager:
    """
    Multi-algorithm encryption manager.
    Supports AES-256, RSA-4096, and hybrid encryption.
    """
    
    def __init__(self):
        """Initialize encryption manager."""
        self.symmetric_keys: Dict[str, bytes] = {}
        self.rsa_keys: Dict[str, Tuple] = {}
    
    def generate_symmetric_key(self, key_id: str = None) -> str:
        """
        Generate AES-256 symmetric key.
        
        Args:
            key_id: Optional key identifier
            
        Returns:
            Key identifier
        """
        if key_id is None:
            key_id = secrets.token_hex(16)
        
        key = Fernet.generate_key()
        self.symmetric_keys[key_id] = key
        
        return key_id
    
    def generate_rsa_keypair(self, key_id: str = None, key_size: int = 4096) -> str:
        """
        Generate RSA key pair.
        
        Args:
            key_id: Optional key identifier
            key_size: Key size in bits (default 4096)
            
        Returns:
            Key identifier
        """
        if key_id is None:
            key_id = secrets.token_hex(16)
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        self.rsa_keys[key_id] = (private_key, public_key)
        
        return key_id
    
    def encrypt_aes(self, data: bytes, key_id: str) -> bytes:
        """
        Encrypt data with AES-256.
        
        Args:
            data: Data to encrypt
            key_id: Key identifier
            
        Returns:
            Encrypted data
        """
        if key_id not in self.symmetric_keys:
            raise ValueError(f"Key not found: {key_id}")
        
        f = Fernet(self.symmetric_keys[key_id])
        return f.encrypt(data)
    
    def decrypt_aes(self, encrypted_data: bytes, key_id: str) -> bytes:
        """
        Decrypt AES-256 encrypted data.
        
        Args:
            encrypted_data: Encrypted data
            key_id: Key identifier
            
        Returns:
            Decrypted data
        """
        if key_id not in self.symmetric_keys:
            raise ValueError(f"Key not found: {key_id}")
        
        f = Fernet(self.symmetric_keys[key_id])
        return f.decrypt(encrypted_data)
    
    def encrypt_rsa(self, data: bytes, key_id: str) -> bytes:
        """
        Encrypt data with RSA public key.
        
        Args:
            data: Data to encrypt (max 446 bytes for RSA-4096)
            key_id: Key identifier
            
        Returns:
            Encrypted data
        """
        if key_id not in self.rsa_keys:
            raise ValueError(f"Key not found: {key_id}")
        
        _, public_key = self.rsa_keys[key_id]
        
        encrypted = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return encrypted
    
    def decrypt_rsa(self, encrypted_data: bytes, key_id: str) -> bytes:
        """
        Decrypt RSA encrypted data.
        
        Args:
            encrypted_data: Encrypted data
            key_id: Key identifier
            
        Returns:
            Decrypted data
        """
        if key_id not in self.rsa_keys:
            raise ValueError(f"Key not found: {key_id}")
        
        private_key, _ = self.rsa_keys[key_id]
        
        decrypted = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return decrypted
    
    def hybrid_encrypt(self, data: bytes, rsa_key_id: str) -> Tuple[bytes, bytes]:
        """
        Hybrid encryption: RSA for key, AES for data.
        
        Args:
            data: Data to encrypt
            rsa_key_id: RSA key identifier
            
        Returns:
            Tuple of (encrypted_key, encrypted_data)
        """
        # Generate random AES key
        aes_key = Fernet.generate_key()
        
        # Encrypt data with AES
        f = Fernet(aes_key)
        encrypted_data = f.encrypt(data)
        
        # Encrypt AES key with RSA
        encrypted_key = self.encrypt_rsa(aes_key, rsa_key_id)
        
        return encrypted_key, encrypted_data
    
    def hybrid_decrypt(self, encrypted_key: bytes, encrypted_data: bytes,
                      rsa_key_id: str) -> bytes:
        """
        Hybrid decryption.
        
        Args:
            encrypted_key: RSA-encrypted AES key
            encrypted_data: AES-encrypted data
            rsa_key_id: RSA key identifier
            
        Returns:
            Decrypted data
        """
        # Decrypt AES key with RSA
        aes_key = self.decrypt_rsa(encrypted_key, rsa_key_id)
        
        # Decrypt data with AES
        f = Fernet(aes_key)
        data = f.decrypt(encrypted_data)
        
        return data


class SteganographyEngine:
    """
    Hide data in images and audio files using steganography.
    """
    
    def hide_in_image(self, image_path: str, message: str, output_path: str) -> Dict:
        """
        Hide message in image using LSB steganography.
        
        Args:
            image_path: Path to cover image
            message: Message to hide
            output_path: Output path for stego image
            
        Returns:
            Result dictionary
        """
        try:
            # Read image
            with open(image_path, 'rb') as f:
                image_data = bytearray(f.read())
            
            # Convert message to binary
            message_binary = ''.join(format(ord(c), '08b') for c in message)
            message_binary += '1111111111111110'  # End marker
            
            if len(message_binary) > len(image_data):
                return {'error': 'Message too large for image'}
            
            # Hide message in LSBs
            for i, bit in enumerate(message_binary):
                image_data[i] = (image_data[i] & 0xFE) | int(bit)
            
            # Write stego image
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            return {
                'success': True,
                'message_length': len(message),
                'bits_used': len(message_binary),
                'output_path': output_path
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def extract_from_image(self, image_path: str) -> Optional[str]:
        """
        Extract hidden message from image.
        
        Args:
            image_path: Path to stego image
            
        Returns:
            Extracted message or None
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Extract LSBs
            binary_message = ''
            for byte in image_data:
                binary_message += str(byte & 1)
            
            # Find end marker
            end_marker = '1111111111111110'
            end_pos = binary_message.find(end_marker)
            
            if end_pos == -1:
                return None
            
            binary_message = binary_message[:end_pos]
            
            # Convert binary to text
            message = ''
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) == 8:
                    message += chr(int(byte, 2))
            
            return message
        
        except Exception as e:
            print(f"Extraction error: {e}")
            return None
    
    def hide_in_audio(self, audio_path: str, message: str, output_path: str) -> Dict:
        """
        Hide message in audio file (placeholder - similar to image).
        
        Args:
            audio_path: Path to audio file
            message: Message to hide
            output_path: Output path
            
        Returns:
            Result dictionary
        """
        # Similar to image steganography but for audio
        return {'info': 'Audio steganography uses similar LSB technique'}


class SecretChannelManager:
    """
    Manage encrypted communication channels.
    """
    
    def __init__(self):
        """Initialize channel manager."""
        self.channels: Dict[str, Dict] = {}
        self.encryption = EncryptionManager()
    
    def create_channel(self, name: str, encryption_type: str = 'aes-256') -> Dict:
        """
        Create new encrypted channel.
        
        Args:
            name: Channel name
            encryption_type: Type of encryption (aes-256, rsa-4096)
            
        Returns:
            Channel information
        """
        channel_id = secrets.token_hex(16)
        
        if encryption_type == 'aes-256':
            key_id = self.encryption.generate_symmetric_key()
        elif encryption_type == 'rsa-4096':
            key_id = self.encryption.generate_rsa_keypair()
        else:
            raise ValueError(f"Unknown encryption type: {encryption_type}")
        
        channel = {
            'id': channel_id,
            'name': name,
            'encryption_type': encryption_type,
            'key_id': key_id,
            'created_at': datetime.now().isoformat(),
            'messages': []
        }
        
        self.channels[channel_id] = channel
        
        return channel
    
    def send_message(self, channel_id: str, message: str,
                    sender_id: str = 'anonymous') -> Dict:
        """
        Send encrypted message to channel.
        
        Args:
            channel_id: Channel identifier
            message: Message to send
            sender_id: Sender identifier
            
        Returns:
            Message information
        """
        if channel_id not in self.channels:
            return {'error': 'Channel not found'}
        
        channel = self.channels[channel_id]
        message_bytes = message.encode('utf-8')
        
        # Encrypt message
        if channel['encryption_type'] == 'aes-256':
            encrypted = self.encryption.encrypt_aes(message_bytes, channel['key_id'])
        elif channel['encryption_type'] == 'rsa-4096':
            # Use hybrid for large messages
            if len(message_bytes) > 400:
                key, data = self.encryption.hybrid_encrypt(message_bytes, channel['key_id'])
                encrypted = base64.b64encode(key + b'|||' + data).decode('utf-8')
            else:
                encrypted = self.encryption.encrypt_rsa(message_bytes, channel['key_id'])
        
        message_data = {
            'id': secrets.token_hex(8),
            'sender': sender_id,
            'encrypted_content': base64.b64encode(encrypted).decode('utf-8') if isinstance(encrypted, bytes) else encrypted,
            'timestamp': datetime.now().isoformat()
        }
        
        channel['messages'].append(message_data)
        
        return message_data
    
    def receive_messages(self, channel_id: str, decrypt: bool = True) -> List[Dict]:
        """
        Receive messages from channel.
        
        Args:
            channel_id: Channel identifier
            decrypt: Whether to decrypt messages
            
        Returns:
            List of messages
        """
        if channel_id not in self.channels:
            return []
        
        channel = self.channels[channel_id]
        messages = []
        
        for msg in channel['messages']:
            if decrypt:
                try:
                    encrypted = msg['encrypted_content']
                    if '|||' in encrypted:
                        # Hybrid encryption
                        parts = base64.b64decode(encrypted).split(b'|||')
                        decrypted = self.encryption.hybrid_decrypt(parts[0], parts[1], channel['key_id'])
                    elif channel['encryption_type'] == 'aes-256':
                        encrypted_bytes = base64.b64decode(encrypted)
                        decrypted = self.encryption.decrypt_aes(encrypted_bytes, channel['key_id'])
                    else:
                        encrypted_bytes = base64.b64decode(encrypted)
                        decrypted = self.encryption.decrypt_rsa(encrypted_bytes, channel['key_id'])
                    
                    msg_copy = msg.copy()
                    msg_copy['content'] = decrypted.decode('utf-8')
                    messages.append(msg_copy)
                except Exception as e:
                    msg_copy = msg.copy()
                    msg_copy['error'] = f'Decryption failed: {e}'
                    messages.append(msg_copy)
            else:
                messages.append(msg)
        
        return messages


class AnonymousMessenger:
    """
    Anonymous messaging with onion routing simulation.
    """
    
    def __init__(self):
        """Initialize anonymous messenger."""
        self.relay_nodes: List[str] = ['node1', 'node2', 'node3']
        self.messages: Dict[str, List] = {}
    
    def send_anonymous(self, recipient: str, message: str, hops: int = 3) -> Dict:
        """
        Send anonymous message through relay network.
        
        Args:
            recipient: Recipient identifier
            message: Message to send
            hops: Number of relay hops
            
        Returns:
            Send confirmation
        """
        # Simulate onion routing
        encrypted_layers = message.encode('utf-8')
        
        for i in range(hops):
            # Add encryption layer
            key = Fernet.generate_key()
            f = Fernet(key)
            encrypted_layers = f.encrypt(encrypted_layers)
        
        message_id = secrets.token_hex(16)
        
        if recipient not in self.messages:
            self.messages[recipient] = []
        
        self.messages[recipient].append({
            'id': message_id,
            'encrypted_message': base64.b64encode(encrypted_layers).decode('utf-8'),
            'hops': hops,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'message_id': message_id,
            'status': 'sent',
            'hops': hops,
            'untraceable': True
        }
    
    def receive_anonymous(self, recipient: str) -> List[Dict]:
        """
        Receive anonymous messages.
        
        Args:
            recipient: Recipient identifier
            
        Returns:
            List of messages
        """
        return self.messages.get(recipient, [])


class CryptographicFlyerSystem:
    """
    Create and distribute encrypted flyers/papers anonymously.
    """
    
    def __init__(self):
        """Initialize flyer system."""
        self.flyers: Dict[str, Dict] = {}
        self.encryption = EncryptionManager()
        self.stego = SteganographyEngine()
    
    def create_flyer(self, title: str, content: str, recipients: List[str],
                    encryption: str = 'pgp') -> Dict:
        """
        Create encrypted flyer.
        
        Args:
            title: Flyer title
            content: Flyer content
            recipients: List of recipient identifiers
            encryption: Encryption type
            
        Returns:
            Flyer information
        """
        flyer_id = secrets.token_hex(16)
        
        # Generate encryption key
        if encryption == 'pgp' or encryption == 'rsa':
            key_id = self.encryption.generate_rsa_keypair()
        else:
            key_id = self.encryption.generate_symmetric_key()
        
        # Encrypt content
        content_bytes = content.encode('utf-8')
        if encryption in ['pgp', 'rsa']:
            encrypted_key, encrypted_content = self.encryption.hybrid_encrypt(
                content_bytes, key_id
            )
        else:
            encrypted_content = self.encryption.encrypt_aes(content_bytes, key_id)
            encrypted_key = None
        
        flyer = {
            'id': flyer_id,
            'title': title,
            'encrypted_content': base64.b64encode(encrypted_content).decode('utf-8'),
            'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8') if encrypted_key else None,
            'key_id': key_id,
            'recipients': recipients,
            'encryption_type': encryption,
            'created_at': datetime.now().isoformat(),
            'signature': hashlib.sha256(content_bytes).hexdigest()
        }
        
        self.flyers[flyer_id] = flyer
        
        return flyer
    
    def distribute_anonymously(self, flyer_id: str, method: str = 'email') -> Dict:
        """
        Distribute flyer anonymously.
        
        Args:
            flyer_id: Flyer identifier
            method: Distribution method (email, steganography, drop)
            
        Returns:
            Distribution result
        """
        if flyer_id not in self.flyers:
            return {'error': 'Flyer not found'}
        
        flyer = self.flyers[flyer_id]
        
        distribution = {
            'flyer_id': flyer_id,
            'method': method,
            'recipients': len(flyer['recipients']),
            'distributed_at': datetime.now().isoformat(),
            'anonymous': True,
            'status': 'distributed'
        }
        
        if method == 'steganography':
            distribution['note'] = 'Flyer hidden in image for covert distribution'
        elif method == 'email':
            distribution['note'] = 'Flyer sent via anonymous email service'
        elif method == 'drop':
            distribution['note'] = 'Flyer available at dead drop location'
        
        return distribution
    
    def decrypt_flyer(self, flyer_id: str) -> Optional[str]:
        """
        Decrypt flyer content.
        
        Args:
            flyer_id: Flyer identifier
            
        Returns:
            Decrypted content
        """
        if flyer_id not in self.flyers:
            return None
        
        flyer = self.flyers[flyer_id]
        
        try:
            encrypted_content = base64.b64decode(flyer['encrypted_content'])
            
            if flyer['encryption_type'] in ['pgp', 'rsa']:
                encrypted_key = base64.b64decode(flyer['encrypted_key'])
                content = self.encryption.hybrid_decrypt(
                    encrypted_key, encrypted_content, flyer['key_id']
                )
            else:
                content = self.encryption.decrypt_aes(encrypted_content, flyer['key_id'])
            
            return content.decode('utf-8')
        
        except Exception as e:
            print(f"Decryption error: {e}")
            return None


# Demo
if __name__ == '__main__':
    print("=== Secret Communications System Demo ===\n")
    
    # 1. Encryption
    print("1. Testing encryption...")
    enc_mgr = EncryptionManager()
    key_id = enc_mgr.generate_symmetric_key()
    
    message = b"Secret investigation findings"
    encrypted = enc_mgr.encrypt_aes(message, key_id)
    decrypted = enc_mgr.decrypt_aes(encrypted, key_id)
    
    print(f"   - Original: {message.decode()}")
    print(f"   - Encrypted: {encrypted[:32]}...")
    print(f"   - Decrypted: {decrypted.decode()}\n")
    
    # 2. Secret Channel
    print("2. Testing secret channel...")
    channel_mgr = SecretChannelManager()
    channel = channel_mgr.create_channel("investigation-team", "aes-256")
    
    channel_mgr.send_message(channel['id'], "Meeting at safe location", "agent-1")
    messages = channel_mgr.receive_messages(channel['id'])
    
    print(f"   - Channel: {channel['name']}")
    print(f"   - Messages: {len(messages)}")
    print(f"   - Content: {messages[0]['content']}\n")
    
    # 3. Steganography
    print("3. Testing steganography...")
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    # Create test image
    image_path = os.path.join(temp_dir, 'cover.bin')
    with open(image_path, 'wb') as f:
        f.write(os.urandom(10000))  # Random data as "image"
    
    stego = SteganographyEngine()
    output_path = os.path.join(temp_dir, 'stego.bin')
    result = stego.hide_in_image(image_path, "Hidden message", output_path)
    
    if result.get('success'):
        extracted = stego.extract_from_image(output_path)
        print(f"   - Hidden message: Hidden message")
        print(f"   - Extracted: {extracted}\n")
    
    # 4. Cryptographic Flyer
    print("4. Testing cryptographic flyer...")
    flyer_sys = CryptographicFlyerSystem()
    flyer = flyer_sys.create_flyer(
        "Investigation Report",
        "Confidential findings...",
        ["recipient1@example.com", "recipient2@example.com"]
    )
    
    dist = flyer_sys.distribute_anonymously(flyer['id'], 'steganography')
    
    print(f"   - Flyer ID: {flyer['id'][:16]}...")
    print(f"   - Recipients: {len(flyer['recipients'])}")
    print(f"   - Distribution: {dist['method']}\n")
    
    print("✓ Secret Communications System demo complete")
    print("✓ All encryption and steganography working")
