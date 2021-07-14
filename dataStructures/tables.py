from dataStructures.historyBlock import historyBlock
import logging
import copy


class Table:
    def __init__(self, table_name="None"):
        self.rows = 0
        # Will add keys as per requirements
        # TODO : Add support for rules
        self.rules = {"PRIMARY_KEY": ""}
        dummy_row = historyBlock()
        dummy_row.top = -1
        self.data = {0: dummy_row}
        self.is_locked = False
        self.table_name = table_name
        self.top = 1

    def insert_row(self, data):
        is_ok = True
        error = ""
        self.is_locked = True
        try:
            newRow = historyBlock()
            newRow.insert(data)
            self.data[self.top + 1] = copy.deepcopy(newRow)
            self.top += 1
            del newRow
        except Exception as e:
            logging.critical("Table_insert_row: {}".format(e))
            is_ok = False
            error = "{}".format(e)
        finally:
            self.is_locked = False
            if is_ok:
                return "OK"
            return error

    def update_row(self, row_id, new_data):
        is_ok = True
        error = ""
        self.is_locked = True
        try:
            self.data[row_id].insert(new_data)
        except Exception as e:
            logging.critical("Table_update_row: {}".format(e))
            is_ok = False
            error = "{}".format(e)
        finally:
            self.is_locked = False
            if is_ok:
                return "OK"
            return error

    def delete_row(self, row_id):
        is_ok = True
        error = ""
        self.is_locked = True
        try:
            self.data.pop(row_id)
        except Exception as e:
            logging.critical("Table_delete_row: {}".format(e))
            is_ok = False
            error = "{}".format(e)
        finally:
            self.is_locked = False
            if is_ok:
                return "OK"
            return error

    def get_row_ids(self) -> list:
        return list(self.data.keys())

    def get_row_ids_range(self, low_bound, high_bound) -> list:
        return self.get_row_ids()[low_bound:high_bound]

    def rollback_row(self, row_id, times):
        is_ok = True
        error = ""
        self.is_locked = True
        try:
            self.data[row_id].rollback(times)
        except Exception as e:
            logging.critical("Table_rollback_row: {}".format(e))
            is_ok = False
            error = "{}".format(e)
        finally:
            self.is_locked = False
            if is_ok:
                return "OK"
            return error

    def get_row_blob(self, row_id) -> historyBlock:
        is_ok = True
        error = ""
        self.is_locked = True
        badblock = historyBlock()
        badblock.top = -1
        try:
            datax = self.data[row_id]
            return datax
        except Exception as e:
            logging.critical("Table_rollback_row: {}".format(e))
            is_ok = False
            error = "{}".format(e)
        finally:
            self.is_locked = False
            if is_ok:
                return datax
            return badblock

    def print_good(self, lower=0, upper=-1):
        if upper >= 0:
            keys = self.get_row_ids_range(lower, upper)
        else:
            keys = self.get_row_ids()
        print("{}".format(self.table_name))
        for i in keys:
            if self.data[i].top < 0:
                continue
            self.data[i].print_good()
