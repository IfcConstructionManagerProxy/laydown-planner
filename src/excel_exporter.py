import pandas as pd

class ExcelExporter:
    def __init__(self, placement_data):
        self.placement_data = placement_data

    def export_to_excel(self, filename):
        with pd.ExcelWriter(filename) as writer:
            for sheet_name, data in self.placement_data.items():
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

# Sample usage:
# placement_data = {
#     'Sheet1': [{'Column1': 'Data1', 'Column2': 'Data2'}],
#     'Sheet2': [{'ColumnA': 'DataA', 'ColumnB': 'DataB'}]
# }
# exporter = ExcelExporter(placement_data)
# exporter.export_to_excel('output.xlsx')
