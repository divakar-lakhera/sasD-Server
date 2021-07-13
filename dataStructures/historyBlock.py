"""
    historyBlock.py
    - Maintains history of each rows
    - Insert: inserts and update history
    Author: Divakar Lakhera
"""
import copy
import datetime
import logging


class historyBlock:
    def __init__(self):
        self.data = {0: {"isBegin": True}}
        self.top = 0
        self.current = {"isBegin": True}
        self.adjustment_factor = 0
        self.creation_time = self.get_time_internal()
        self.last_commit_time = ""
        self.is_locked = False

    def get_time_internal(self) -> str:
        timex = datetime.datetime.now()
        return timex.strftime("%Y-%m-%d %H:%M:%S")

    def get_diff_map(self, data) -> dict:
        keys = set(data.keys())
        keys_current = set(self.current.keys())
        changes = {"+": [], "-": [], "*": [], "p": []}
        #  + add  - remove
        new_keys = keys.difference(keys_current)
        removed_keys = keys_current.difference(keys)
        new_updates = []
        # keys that need update
        for key in keys:
            if key not in new_keys and key not in removed_keys and data[key] != self.current[key]:
                new_updates.append(key)
        for key in new_keys:
            changes["+"].append({key: data[key]})

        for key in removed_keys:
            changes["-"].append(key)
            changes["p"].append({key: self.current[key]})

        for key in new_updates:
            changes["*"].append({key: data[key]})
            changes["p"].append({key: self.current[key]})

        return changes

    def apply_diff(self, diff):
        # Remove
        for key in diff["-"]:
            self.current.pop(key)
        # Add new [{} ,{}]
        for element in diff["+"]:
            self.current[list(element.keys())[0]] = list(element.values())[0]
        # Update
        for element in diff["*"]:
            self.current[list(element.keys())[0]] = list(element.values())[0]

    def revert_diff(self, diff):
        # Remove will be add
        # Add will be remove
        # Revert back to previous values
        logging.info("dd :{}".format(diff))
        for entry in diff["+"]:
            self.current.pop(list(entry.keys())[0])
        for entry in diff["p"]:
            key = list(entry.keys())[0]
            value = list(entry.values())[0]
            self.current[key] = value
        return

    def insert(self, data) -> str:
        # Does ShallowCopy increase speed ?
        error = ""
        has_error = False
        try:
            self.is_locked = True
            # wait ?
            diffs = self.get_diff_map(data)
            self.data[self.top + 1] = copy.deepcopy(diffs)
            self.apply_diff(diffs)
            del diffs
            self.top += 1
            self.last_commit_time = self.get_time_internal()
            self.is_locked = False
        except Exception as e:
            logging.critical("Insert Failed: {}".format(e))
            error = "{}".format(e)
            has_error = True
        finally:
            if has_error:
                return error
            return "OK"

    def rollback(self, times):
        error = ""
        has_error = False
        removed = 0
        try:
            self.is_locked = True
            current_top = self.top
            new_top = max(0, (self.top - times))
            for i in range(current_top, new_top, -1):
                self.revert_diff(self.data[i])
                removed += 1

        except Exception as e:
            logging.critical("Rollback Failed: {}".format(e))
            error = "{}".format(e)
            has_error = True
        finally:
            self.top -= removed
            if has_error:
                return error
            return "OK"
