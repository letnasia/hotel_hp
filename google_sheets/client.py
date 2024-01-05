import gspread
import os

CREDENTIALS_PATH = os.path.join(
    # os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    os.path.dirname(os.path.abspath(__file__)),
    "credentials.json"
)


class GoogleSheetsCredentials:
    gc = None

    def __init__(self):
        self.credentials_path = CREDENTIALS_PATH

    def __enter__(self):
        if not self.gc:
            self.gc = gspread.service_account(filename=self.credentials_path)

        return self.gc

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def read_from_sheet(file):
    with GoogleSheetsCredentials() as gc:
        sh = gc.open(file)
        worksheet = sh.sheet1
        return worksheet.get_all_values()


def write_to_sheet(file, data):
    with GoogleSheetsCredentials() as gc:
        sh = gc.open(file)
        worksheet = sh.sheet1
        worksheet.append_rows(data)


if __name__ == "__main__":
    data = read_from_sheet()
    print(data)
