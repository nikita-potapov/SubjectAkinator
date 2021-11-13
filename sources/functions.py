from PyQt5.QtWidgets import QTableWidgetItem


def update_table(table, data, headers=None):
    if not data:
        table.clearContents()
        table.setRowCount(0)
        return
    # Заполним размеры таблицы
    table.setColumnCount(len(data[0]))
    table.setRowCount(0)
    if headers is not None:
        table.setHorizontalHeaderLabels(headers)

    # Заполняем таблицу элементами
    for i, row in enumerate(data):
        table.setRowCount(
            table.rowCount() + 1)
        for j, elem in enumerate(row):
            table.setItem(
                i, j, QTableWidgetItem(str(elem)))

    table.resizeColumnsToContents()
