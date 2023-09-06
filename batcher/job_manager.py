import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from job_manager_ui import Ui_MainWindow  # Import the generated UI class

class JobManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.jobs = []
        self.current_job_index = 0

        self.pushButtonAddJob.clicked.connect(self.add_job)
        self.pushButtonRemoveJob.clicked.connect(self.remove_selected_job)
        self.pushButtonStartExecution.clicked.connect(self.start_execution)

        self.lineEditIterableInput.setText("[1, 2, 3]")
        self.textEditJobInput.setText("print(item)")

    def add_job(self):
        code = self.textEditJobInput.toPlainText()
        self.jobs.append({"code": code, "status": "Pending"})
        self.textEditJobInput.clear()
        self.update_job_list()

    def remove_selected_job(self):
        selected_item = self.listWidgetJobs.currentItem()
        if selected_item:
            selected_index = self.listWidgetJobs.row(selected_item)
            self.jobs.pop(selected_index)
            self.update_job_list()

    def start_execution(self):
        self.clear_results()
        iterable_script = self.lineEditIterableInput.text()
        iterable = []
        try:
            self.plainTextEditResults.appendPlainText(f"collecting iterable: {iterable_script}")
            # exec(f'iterable = {iterable_script}', globals(), locals())
            iterable = eval(iterable_script, globals(), locals())
            self.plainTextEditResults.appendPlainText(f"collected iterable: {iterable}")
        except Exception as e:
            self.plainTextEditResults.appendPlainText(f"Error parsing iterable input: {e}")
            return

        if not isinstance(iterable, (list, tuple)):
            self.plainTextEditResults.appendPlainText("Iterable must be a list or tuple.")
            return

        self.current_job_index = 0
        for item in iterable:
            for job in self.jobs:
                code = job["code"]
                try:
                    self.plainTextEditResults.appendPlainText(f"starting job {self.current_job_index + 1}")
                    exec(code, globals(), locals())
                    job["status"] = "Done"
                except Exception as e:
                    job["status"] = "Error"
                    self.plainTextEditResults.appendPlainText(f"Error executing job: {e}")
            self.update_job_list()

        self.plainTextEditResults.appendPlainText("All jobs processed.")

    def clear_results(self):
        self.plainTextEditResults.clear()

    def update_job_list(self):
        self.listWidgetJobs.clear()
        for index, job in enumerate(self.jobs):
            status = job["status"]
            item_text = f"Job {index + 1}: {status}"
            item = QListWidgetItem(item_text)
            if status == "Running":
                item.setForeground(Qt.blue)
            elif status == "Done":
                item.setForeground(Qt.green)
            elif status == "Error":
                item.setForeground(Qt.red)
            self.listWidgetJobs.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JobManager()
    window.show()
    sys.exit(app.exec_())