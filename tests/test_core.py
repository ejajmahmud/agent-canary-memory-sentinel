"""Tests for CanaryMemorySentinel."""
import unittest
from agent_canary_memory_sentinel.core import CanaryMemorySentinel

class TestCanaryMemorySentinel(unittest.TestCase):
    def setUp(self):
        self.sentinel = CanaryMemorySentinel()

    def test_canary_intact(self):
        c = self.sentinel.plant_canary("scratchpad")
        mem = f"Some text {c} more text"
        res = self.sentinel.inspect_memory(mem)
        self.assertTrue(res["intact"])
        self.assertEqual(res["found_canaries"], 1)

    def test_canary_tampered(self):
        c = self.sentinel.plant_canary("scratchpad")
        cid = list(self.sentinel.active_canaries.keys())[0]
        tampered_mem = f"Some text <!-- CANARY:{cid}:corrupted_token --> more text"
        res = self.sentinel.inspect_memory(tampered_mem)
        self.assertFalse(res["intact"])
        self.assertIn(cid, res["tampered_canaries"])
