from dataStructures.tables import Table

test_data_2 = {"string": "string3ds", "isBegin": False}
test_data_1 = {"string": "string", "isBegin": False}
tab = Table(table_name="My Table")
tab.insert_row(test_data_2)
tab.insert_row(test_data_2)
tab.insert_row(test_data_2)
tab.insert_row(test_data_2)

tab.print_good(lower=0, upper=1)
