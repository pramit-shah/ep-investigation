#!/usr/bin/env python3
"""
Comprehensive tests for massive storage, tampering detection, and secret communications.
"""

import os
import tempfile
import unittest
from massive_storage import (
    DataDeduplicator, CompressionManager, DistributedStorageManager,
    SmartDataCollector, MassiveStorageSystem
)
from file_tampering_detector import (
    FileIntegrityMonitor, MetadataAnalyzer, ContentAnalyzer,
    SteganographyDetector, FileTamperingDetector
)
from secret_communications import (
    EncryptionManager, SteganographyEngine, SecretChannelManager,
    AnonymousMessenger, CryptographicFlyerSystem
)


class TestMassiveStorage(unittest.TestCase):
    """Test massive storage system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def test_data_deduplication(self):
        """Test data deduplication."""
        dedup = DataDeduplicator(chunk_size=1024)
        
        # Create test file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("test data " * 1000)
        
        result = dedup.deduplicate_file(test_file, self.temp_dir)
        
        self.assertIn('file_path', result)
        self.assertGreater(result['total_chunks'], 0)
        self.assertGreaterEqual(result['deduplication_ratio'], 0)
    
    def test_dedup_reconstruct(self):
        """Test file reconstruction from chunks."""
        dedup = DataDeduplicator()
        
        test_file = os.path.join(self.temp_dir, 'original.txt')
        with open(test_file, 'w') as f:
            f.write("reconstruct test")
        
        dedup.deduplicate_file(test_file, self.temp_dir)
        
        output_file = os.path.join(self.temp_dir, 'reconstructed.txt')
        success = dedup.reconstruct_file(test_file, output_file)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_file))
    
    def test_dedup_stats(self):
        """Test deduplication statistics."""
        dedup = DataDeduplicator()
        stats = dedup.get_stats()
        
        self.assertIn('total_chunks', stats)
        self.assertIn('total_files', stats)
    
    def test_compression_zlib(self):
        """Test zlib compression."""
        comp = CompressionManager('zlib')
        
        test_file = os.path.join(self.temp_dir, 'compress.txt')
        with open(test_file, 'w') as f:
            f.write("compress me " * 100)
        
        result = comp.compress_file(test_file)
        
        self.assertIn('compression_ratio', result)
        self.assertGreater(result['compression_ratio'], 1.0)
    
    def test_compression_gzip(self):
        """Test gzip compression."""
        comp = CompressionManager('gzip')
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("test " * 50)
        
        result = comp.compress_file(test_file, algorithm='gzip')
        self.assertNotIn('error', result)
    
    def test_compression_decompress(self):
        """Test compression and decompression."""
        comp = CompressionManager()
        
        test_file = os.path.join(self.temp_dir, 'original.txt')
        compressed = os.path.join(self.temp_dir, 'compressed')
        decompressed = os.path.join(self.temp_dir, 'decompressed.txt')
        
        with open(test_file, 'w') as f:
            f.write("test data")
        
        comp.compress_file(test_file, compressed)
        success = comp.decompress_file(compressed, decompressed)
        
        self.assertTrue(success)
        
        with open(decompressed, 'r') as f:
            self.assertEqual(f.read(), "test data")
    
    def test_distributed_storage(self):
        """Test distributed storage."""
        loc1 = os.path.join(self.temp_dir, 'loc1')
        loc2 = os.path.join(self.temp_dir, 'loc2')
        
        dist = DistributedStorageManager([loc1, loc2], replication_factor=2)
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("distributed")
        
        result = dist.store_file(test_file)
        
        self.assertIn('file_id', result)
        self.assertGreaterEqual(result['replication_achieved'], 1)
    
    def test_distributed_retrieve(self):
        """Test file retrieval from distributed storage."""
        loc = os.path.join(self.temp_dir, 'storage')
        dist = DistributedStorageManager([loc])
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("retrieve me")
        
        result = dist.store_file(test_file)
        file_id = result['file_id']
        
        output = os.path.join(self.temp_dir, 'retrieved.txt')
        success = dist.retrieve_file(file_id, output)
        
        self.assertTrue(success)
    
    def test_distributed_verify(self):
        """Test replication verification."""
        loc = os.path.join(self.temp_dir, 'storage')
        dist = DistributedStorageManager([loc])
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("verify")
        
        result = dist.store_file(test_file)
        verification = dist.verify_replication(result['file_id'])
        
        self.assertIn('health', verification)
    
    def test_smart_collector_categorize(self):
        """Test file categorization."""
        collector = SmartDataCollector(self.temp_dir)
        
        self.assertEqual(collector.categorize_file('test.pdf'), 'documents')
        self.assertEqual(collector.categorize_file('photo.jpg'), 'images')
        self.assertEqual(collector.categorize_file('video.mp4'), 'videos')
    
    def test_smart_collector_metadata(self):
        """Test metadata extraction."""
        collector = SmartDataCollector(self.temp_dir)
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("metadata")
        
        metadata = collector.extract_metadata(test_file)
        
        self.assertIn('filename', metadata)
        self.assertIn('sha256', metadata)
        self.assertIn('category', metadata)
    
    def test_smart_collector_organize(self):
        """Test file collection and organization."""
        collector = SmartDataCollector(os.path.join(self.temp_dir, 'organized'))
        
        # Create test files
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("organize")
        
        stats = collector.collect_and_organize(test_file)
        
        self.assertIn('total', stats)
        self.assertGreater(stats['total'], 0)
    
    def test_massive_storage_init(self):
        """Test massive storage system initialization."""
        storage = MassiveStorageSystem(self.temp_dir, max_size_tb=1.0)
        
        self.assertEqual(storage.base_path, self.temp_dir)
        self.assertIsNotNone(storage.deduplicator)
    
    def test_massive_storage_store_file(self):
        """Test storing file in massive storage."""
        storage = MassiveStorageSystem(self.temp_dir)
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("store me " * 100)
        
        result = storage.store_file(test_file, compress=True, deduplicate=False)
        
        self.assertIn('file_id', result)
        self.assertIn('steps', result)
    
    def test_massive_storage_stats(self):
        """Test storage statistics."""
        storage = MassiveStorageSystem(self.temp_dir, max_size_tb=10.0)
        stats = storage.get_storage_stats()
        
        self.assertIn('total_files', stats)
        self.assertIn('max_size_tb', stats)
        self.assertEqual(stats['max_size_tb'], 10.0)


class TestFileTampering(unittest.TestCase):
    """Test file tampering detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def test_integrity_compute_hashes(self):
        """Test hash computation."""
        monitor = FileIntegrityMonitor()
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("integrity test")
        
        hashes = monitor.compute_hashes(test_file)
        
        self.assertIn('sha256', hashes)
        self.assertIn('sha512', hashes)
        self.assertIn('md5', hashes)
    
    def test_integrity_baseline(self):
        """Test baseline creation."""
        monitor = FileIntegrityMonitor()
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("baseline")
        
        baseline = monitor.create_baseline(test_file)
        
        self.assertIn('hashes', baseline)
        self.assertIn('size', baseline)
    
    def test_integrity_verify(self):
        """Test integrity verification."""
        monitor = FileIntegrityMonitor()
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("verify")
        
        monitor.create_baseline(test_file)
        result = monitor.verify_integrity(test_file)
        
        self.assertFalse(result['tampered'])
    
    def test_metadata_timestamps(self):
        """Test timestamp analysis."""
        analyzer = MetadataAnalyzer()
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("timestamp")
        
        analysis = analyzer.analyze_timestamps(test_file)
        
        self.assertIn('modified_time', analysis)
        self.assertIn('anomalies', analysis)
    
    def test_metadata_exif(self):
        """Test EXIF analysis."""
        analyzer = MetadataAnalyzer()
        
        test_file = os.path.join(self.temp_dir, 'test.jpg')
        with open(test_file, 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF')  # JPEG header
        
        analysis = analyzer.analyze_exif(test_file)
        
        self.assertIn('has_exif', analysis)
    
    def test_content_file_signature(self):
        """Test file signature verification."""
        analyzer = ContentAnalyzer()
        
        test_file = os.path.join(self.temp_dir, 'test.pdf')
        with open(test_file, 'wb') as f:
            f.write(b'%PDF-1.4')
        
        result = analyzer.verify_file_signature(test_file)
        
        self.assertTrue(result['matches'])
    
    def test_content_tampering_patterns(self):
        """Test tampering pattern detection."""
        analyzer = ContentAnalyzer()
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("normal content")
        
        result = analyzer.detect_tampering_patterns(test_file)
        
        self.assertIn('null_bytes', result)
        self.assertIn('suspicious', result)
    
    def test_stego_lsb_detection(self):
        """Test LSB steganography detection."""
        detector = SteganographyDetector()
        
        test_file = os.path.join(self.temp_dir, 'test.png')
        with open(test_file, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n' + os.urandom(1000))
        
        result = detector.detect_lsb_steganography(test_file)
        
        self.assertIn('method', result)
    
    def test_stego_statistical(self):
        """Test statistical analysis."""
        detector = SteganographyDetector()
        
        test_file = os.path.join(self.temp_dir, 'test.bin')
        with open(test_file, 'wb') as f:
            f.write(os.urandom(10000))
        
        result = detector.statistical_analysis(test_file)
        
        self.assertIn('entropy', result)
    
    def test_tampering_detector_baseline(self):
        """Test comprehensive baseline."""
        detector = FileTamperingDetector()
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("baseline test")
        
        baseline = detector.create_baseline(test_file)
        
        self.assertIn('integrity', baseline)
        self.assertIn('metadata', baseline)
    
    def test_tampering_detector_check(self):
        """Test comprehensive tampering check."""
        detector = FileTamperingDetector()
        
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("check test")
        
        detector.create_baseline(test_file)
        result = detector.comprehensive_check(test_file)
        
        self.assertIn('tampered', result)
        self.assertIn('checks', result)
    
    def test_tampering_detector_batch(self):
        """Test batch checking."""
        detector = FileTamperingDetector()
        
        files = []
        for i in range(3):
            test_file = os.path.join(self.temp_dir, f'test{i}.txt')
            with open(test_file, 'w') as f:
                f.write(f"file {i}")
            files.append(test_file)
        
        results = detector.batch_check(files)
        
        self.assertEqual(results['total_files'], 3)


class TestSecretCommunications(unittest.TestCase):
    """Test secret communications."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def test_encryption_symmetric_key(self):
        """Test symmetric key generation."""
        enc = EncryptionManager()
        key_id = enc.generate_symmetric_key()
        
        self.assertIsNotNone(key_id)
        self.assertIn(key_id, enc.symmetric_keys)
    
    def test_encryption_rsa_keypair(self):
        """Test RSA keypair generation."""
        enc = EncryptionManager()
        key_id = enc.generate_rsa_keypair(key_size=2048)
        
        self.assertIn(key_id, enc.rsa_keys)
    
    def test_encryption_aes(self):
        """Test AES encryption/decryption."""
        enc = EncryptionManager()
        key_id = enc.generate_symmetric_key()
        
        data = b"secret message"
        encrypted = enc.encrypt_aes(data, key_id)
        decrypted = enc.decrypt_aes(encrypted, key_id)
        
        self.assertEqual(data, decrypted)
    
    def test_encryption_rsa(self):
        """Test RSA encryption/decryption."""
        enc = EncryptionManager()
        key_id = enc.generate_rsa_keypair(key_size=2048)
        
        data = b"short message"
        encrypted = enc.encrypt_rsa(data, key_id)
        decrypted = enc.decrypt_rsa(encrypted, key_id)
        
        self.assertEqual(data, decrypted)
    
    def test_encryption_hybrid(self):
        """Test hybrid encryption."""
        enc = EncryptionManager()
        key_id = enc.generate_rsa_keypair(key_size=2048)
        
        data = b"long message " * 100
        enc_key, enc_data = enc.hybrid_encrypt(data, key_id)
        decrypted = enc.hybrid_decrypt(enc_key, enc_data, key_id)
        
        self.assertEqual(data, decrypted)
    
    def test_stego_hide_extract(self):
        """Test steganography hide and extract."""
        stego = SteganographyEngine()
        
        image_path = os.path.join(self.temp_dir, 'cover.bin')
        output_path = os.path.join(self.temp_dir, 'stego.bin')
        
        with open(image_path, 'wb') as f:
            f.write(os.urandom(10000))
        
        message = "Hidden data"
        result = stego.hide_in_image(image_path, message, output_path)
        
        if result.get('success'):
            extracted = stego.extract_from_image(output_path)
            self.assertEqual(extracted, message)
    
    def test_stego_audio(self):
        """Test audio steganography placeholder."""
        stego = SteganographyEngine()
        result = stego.hide_in_audio('test.wav', 'message', 'output.wav')
        
        self.assertIn('info', result)
    
    def test_channel_create(self):
        """Test channel creation."""
        mgr = SecretChannelManager()
        channel = mgr.create_channel("test-channel", "aes-256")
        
        self.assertIn('id', channel)
        self.assertEqual(channel['name'], "test-channel")
    
    def test_channel_send_receive(self):
        """Test sending and receiving messages."""
        mgr = SecretChannelManager()
        channel = mgr.create_channel("chat", "aes-256")
        
        mgr.send_message(channel['id'], "Hello", "user1")
        messages = mgr.receive_messages(channel['id'])
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['content'], "Hello")
    
    def test_anonymous_messenger(self):
        """Test anonymous messaging."""
        messenger = AnonymousMessenger()
        
        result = messenger.send_anonymous("recipient1", "Anonymous tip", hops=3)
        
        self.assertEqual(result['status'], 'sent')
        self.assertTrue(result['untraceable'])
    
    def test_anonymous_receive(self):
        """Test receiving anonymous messages."""
        messenger = AnonymousMessenger()
        
        messenger.send_anonymous("user1", "Message 1")
        messenger.send_anonymous("user1", "Message 2")
        
        messages = messenger.receive_anonymous("user1")
        
        self.assertEqual(len(messages), 2)
    
    def test_flyer_create(self):
        """Test flyer creation."""
        flyer_sys = CryptographicFlyerSystem()
        
        flyer = flyer_sys.create_flyer(
            "Report",
            "Content here",
            ["user1@example.com"]
        )
        
        self.assertIn('id', flyer)
        self.assertEqual(flyer['title'], "Report")
    
    def test_flyer_distribute(self):
        """Test flyer distribution."""
        flyer_sys = CryptographicFlyerSystem()
        
        flyer = flyer_sys.create_flyer("Test", "Content", ["user1"])
        result = flyer_sys.distribute_anonymously(flyer['id'], 'email')
        
        self.assertEqual(result['status'], 'distributed')
        self.assertTrue(result['anonymous'])


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
