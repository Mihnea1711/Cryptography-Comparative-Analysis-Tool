import sys
import traceback
from typing import Optional

from PySide2.QtWidgets import QApplication

from business.service.keygen import KeygenService
from business.service.performance import ApplicationService
from persistence.database.sqlite.sqlite import SQLiteAgent
from presentation.ui import StartPage

if __name__ == "__main__":
    # establish conn to database and init agent
    sqlite_agent: Optional[SQLiteAgent] = None
    try:
        sqlite_agent = SQLiteAgent()

        app_service = ApplicationService(sqlite_agent)
        key_gen_service = KeygenService(sqlite_agent)

        app = QApplication(sys.argv)

        widget = StartPage(app_service, key_gen_service)
        widget.show()

        sys.exit(app.exec_())

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if sqlite_agent:
            sqlite_agent.close_connection()
