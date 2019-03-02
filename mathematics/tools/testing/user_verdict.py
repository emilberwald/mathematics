import multiprocessing
import pathlib
import webbrowser

from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QTextBrowser,
    QDialogButtonBox,
    QVBoxLayout,
    QMessageBox,
    QWidget,
)


class GUITextVerdict(QDialog):
    def __init__(self, title, question, return_list):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.buttonbox = QDialogButtonBox(
            QDialogButtonBox.Yes | QDialogButtonBox.No, parent=self
        )
        self.textbox = QTextBrowser(parent=self)
        self.setModal(True)
        self.title = title
        self.question = question
        self.return_list = return_list
        self.initUI()

    def initUI(self):
        self.textbox.setPlainText(self.question)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.buttonbox)

        self.setLayout(self.layout)
        self.setWindowTitle(self.title)


def gui_textverdict(title, question, return_list):
    _qapp = QApplication([])
    guiverdict = GUITextVerdict(title, question, return_list)
    verdict = guiverdict.exec()
    if verdict == QDialog.Accepted:
        return_list.append(True)
    else:
        return_list.append(False)


def gui_mediaverdict(title, media_file, return_list):
    media_file = pathlib.Path(media_file)
    if not media_file.is_file():
        raise ValueError()
    webbrowser.open_new(media_file)
    _qapp = QApplication([])
    verdict = QMessageBox.question(
        parent=QWidget(),
        title=title,
        text="Does it look nice?",
        button0=QMessageBox.Yes | QMessageBox.No,
        button1=QMessageBox.No,
    )
    if verdict == QMessageBox.Yes:
        return_list.append(True)
    else:
        return_list.append(False)


def get_textverdict(title, question, timeout=10):
    manager = multiprocessing.Manager()
    return_list = manager.list()
    verdict_process = multiprocessing.Process(
        name="verdict_process",
        target=gui_textverdict,
        args=(title, question, return_list),
    )
    verdict_process.start()
    verdict_process.join(timeout)
    return True in return_list


def get_mediaverdict(title, media_file, timeout=10):
    manager = multiprocessing.Manager()
    return_list = manager.list()
    verdict_process = multiprocessing.Process(
        name="verdict_process",
        target=gui_mediaverdict,
        args=(title, media_file, return_list),
    )
    verdict_process.start()
    verdict_process.join(timeout)
    return True in return_list
