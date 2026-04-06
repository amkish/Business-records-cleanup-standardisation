
from pathlib import Path
import pandas as pd
from artifact_tool import Workbook, SpreadsheetFile

BASE = Path(__file__).resolve().parents[1]
CLEANED = BASE / "data" / "cleaned"
REPORTS = BASE / "reports"

HEADER_FORMAT = {
    "fill": "#1F4E78",
    "font": {"bold": True, "color": "#FFFFFF"},
    "horizontal_alignment": "center",
    "vertical_alignment": "center",
}

def write_df(sheet, cell, df):
    values = [list(df.columns)] + df.fillna('').values.tolist()
    end_col = len(df.columns)
    end_row = len(values)
    def col_letter(n):
        s = ""
        while n:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s
    end = f"{col_letter(end_col)}{end_row}"
    rng = sheet.get_range(f"{cell}:{end}")
    rng.values = values
    sheet.get_range(f"A1:{col_letter(end_col)}1").format = HEADER_FORMAT
    sheet.get_range(f"A1:{col_letter(end_col)}{end_row}").format.wrap_text = True
    sheet.get_range(f"A1:{col_letter(end_col)}{end_row}").format.autofit_columns()
    return end

def build_summary_sheet(sheet, summary_df):
    sheet.get_range("A1:B1").values = [["Metric", "Value"]]
    sheet.get_range("A1:B1").format = HEADER_FORMAT
    rows = summary_df.T.reset_index()
    rows.columns = ["Metric", "Value"]
    sheet.get_range(f"A2:B{len(rows)+1}").values = rows.values.tolist()
    sheet.get_range(f"A1:B{len(rows)+1}").format.autofit_columns()

def main():
    master = pd.read_csv(CLEANED / 'master_records.csv')
    issues = pd.read_csv(REPORTS / 'issue_log.csv')
    summary = pd.read_csv(REPORTS / 'data_quality_summary.csv')

    wb = Workbook.create()
    s1 = wb.worksheets.add("Master_Data")
    s2 = wb.worksheets.add("Issue_Log")
    s3 = wb.worksheets.add("Quality_Report")

    write_df(s1, "A1", master)
    write_df(s2, "A1", issues if not issues.empty else pd.DataFrame(columns=["No issues"]))
    build_summary_sheet(s3, summary)

    SpreadsheetFile.export_xlsx(wb).save(str(CLEANED / 'master_records.xlsx'))
    SpreadsheetFile.export_xlsx(wb).save(str(REPORTS / 'data_quality_report.xlsx'))
    print("Excel outputs written.")

if __name__ == '__main__':
    main()
