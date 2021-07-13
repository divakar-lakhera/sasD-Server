from os import terminal_size
import unittest
from dataStructures.historyBlock import historyBlock

test_data_1 = {
    "string": "string",
    "string_num": 123,
    "string_set": {1, 2, 3},
    "string_dict": {1: 2, 2: 3},
    "string_list": [1, 2, 3, 4],
    123: "string",
    1234: [0, 1],
}
test_data_2 = {"string": "string", "isBegin": False}


class historyBlockTest(unittest.TestCase):
    def test_diff(self):
        test_block = historyBlock()
        diff_1 = test_block.get_diff_map(test_data_1)
        diff_2 = test_block.get_diff_map(test_data_2)
        for entry in diff_1["+"]:
            key = list(entry.keys())[0]
            value = list(entry.values())[0]
            assert test_data_1[key] == value
        assert diff_1["-"][0] == "isBegin"
        assert diff_2["*"][0] == {"isBegin": False}
        return

    def test_block_init(self):
        testBlock = historyBlock()
        node = testBlock.current
        assert node["isBegin"] == True
        assert testBlock.top == 0
        return

    def test_apply_diff_remove_insert(self):
        testBlock = historyBlock()
        testBlock.insert(test_data_1)
        node_new = testBlock.current
        poss = test_data_1.keys()
        vals = test_data_1.values()
        for k in node_new.keys():
            assert k in poss
        for v in node_new.values():
            assert v in vals
        assert "isBegin" not in node_new.keys()
        return

    def test_apply_diff_update_insert(self):
        testBlock = historyBlock()
        testBlock.insert(test_data_2)
        node_new = testBlock.current
        poss = test_data_2.keys()
        vals = test_data_2.values()
        assert "isBegin" in node_new.keys()
        assert node_new["isBegin"] == False
        assert "string" in node_new.keys()
        return

    def test_rollback(self):
        testBlock = historyBlock()
        testBlock.insert(test_data_1)
        testBlock.rollback(1)
        assert testBlock.top == 0
        assert testBlock.current == {"isBegin": True}
        testBlock.insert(test_data_2)
        assert testBlock.current == test_data_2
        testBlock.rollback(1)
        assert testBlock.current == {"isBegin": True}
        testBlock.insert(test_data_1)
        testBlock.insert(test_data_2)
        assert testBlock.current == test_data_2
        testBlock.rollback(1)
        assert testBlock.current == test_data_1
        return
