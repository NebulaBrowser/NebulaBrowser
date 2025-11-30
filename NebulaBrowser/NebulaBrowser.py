import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QAction,
    QToolBar, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QProgressBar, QPushButton, QFrame
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEnginePage
)
from PyQt5.QtCore import QUrl, QStandardPaths, QFileInfo
from PyQt5.QtGui import QPalette, QColor, QDesktopServices


class BrowserTab(QWebEngineView):
    def __init__(self, profile, parent_window):
        super().__init__()
        self._parent_window = parent_window
        page = QWebEnginePage(profile, self)
        self.setPage(page)
        self.page().fullScreenRequested.connect(self.handle_fullscreen)

    def handle_fullscreen(self, request):
        url = self.url().toString().lower()
        if request.toggleOn():
            self._parent_window.enter_fullscreen_mode()
        else:
            self._parent_window.exit_fullscreen_mode()
        request.accept()

    def createWindow(self, _type):
        return self._parent_window.create_tab_from_popup()


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NebulaBrowser 1.0.0")
        self.setGeometry(200, 120, 1300, 850)

        self.is_fullscreen = False

        self.profile = QWebEngineProfile("NebulaProfile", self)
        self.profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)

        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
        self.profile.setHttpAcceptLanguage("en-US,en;q=0.9")

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)

        self.downloads_bar = QFrame()
        self.downloads_bar.setVisible(False)
        self.downloads_layout = QVBoxLayout(self.downloads_bar)
        self.downloads_layout.setContentsMargins(6, 4, 6, 4)
        self.downloads_layout.setSpacing(4)

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_layout.addWidget(self.tabs)
        central_layout.addWidget(self.downloads_bar)
        self.setCentralWidget(central)

        self.create_toolbar()
        self.apply_dark_theme()

        self.profile.downloadRequested.connect(self.handle_download_requested)

        self.add_tab("https://www.google.com")

    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        back = QAction("←", self)
        back.triggered.connect(lambda: self.current_tab().back())
        self.toolbar.addAction(back)

        fwd = QAction("→", self)
        fwd.triggered.connect(lambda: self.current_tab().forward())
        self.toolbar.addAction(fwd)

        reload = QAction("⟳", self)
        reload.triggered.connect(lambda: self.current_tab().reload())
        self.toolbar.addAction(reload)

        newtab = QAction("+", self)
        newtab.triggered.connect(lambda: self.add_tab("https://www.google.com"))
        self.toolbar.addAction(newtab)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_bar)

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.Text, QColor(230, 230, 230))
        palette.setColor(QPalette.Button, QColor(40, 40, 40))
        palette.setColor(QPalette.ButtonText, QColor(240, 240, 240))
        QApplication.instance().setPalette(palette)

        self.toolbar.setStyleSheet(
            """
            QToolBar {
                background-color: #1e1e1e;
                border: none;
            }
            QToolButton {
                color: white;
                font-size: 18px;
                padding: 6px 10px;
            }
            QToolButton:hover {
                background-color: #333333;
            }
            """
        )
        self.url_bar.setStyleSheet(
            """
            background-color: #2d2d2d;
            color: white;
            padding: 6px;
            border-radius: 5px;
            border: 1px solid #444444;
            """
        )
        self.downloads_bar.setStyleSheet(
            """
            QFrame {
                background-color: #202020;
                border-top: 1px solid #444444;
            }
            QLabel {
                color: white;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 4px;
                text-align: center;
                background-color: #303030;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
            }
            QPushButton {
                background-color: #383838;
                color: white;
                border-radius: 4px;
                padding: 3px 8px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            """
        )

    def add_tab(self, url):
        browser = BrowserTab(self.profile, self)
        browser.setUrl(QUrl(url))
        browser.urlChanged.connect(self.update_tab_title)
        idx = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(idx)

    def create_tab_from_popup(self):
        new_tab = BrowserTab(self.profile, self)
        new_tab.urlChanged.connect(self.update_tab_title)
        idx = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(idx)
        return new_tab

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def current_tab(self):
        return self.tabs.currentWidget()

    def update_tab_title(self, qurl):
        idx = self.tabs.indexOf(self.sender())
        if idx != -1:
            self.tabs.setTabText(idx, qurl.toString()[:20])
        if self.sender() is self.current_tab():
            self.url_bar.setText(qurl.toString())

    def update_url_bar(self, _index):
        tab = self.current_tab()
        if tab:
            self.url_bar.setText(tab.url().toString())

    def load_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        if not url.startswith("http"):
            url = "https://" + url
        self.current_tab().setUrl(QUrl(url))

    def enter_fullscreen_mode(self):
        if getattr(self, "is_fullscreen", False):
            return
        self.is_fullscreen = True
        self._saved_toolbar_visible = self.toolbar.isVisible()
        self._saved_tabbar_visible = self.tabs.tabBar().isVisible()
        self.toolbar.hide()
        self.tabs.tabBar().hide()
        self.showFullScreen()

    def exit_fullscreen_mode(self):
        if not getattr(self, "is_fullscreen", False):
            return
        self.is_fullscreen = False
        self.showNormal()
        if getattr(self, "_saved_toolbar_visible", True):
            self.toolbar.show()
        if getattr(self, "_saved_tabbar_visible", True):
            self.tabs.tabBar().show()

    def handle_download_requested(self, item):
        downloads_dir = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        if downloads_dir:
            info = QFileInfo(item.path())
            target = downloads_dir + "/" + info.fileName()
            item.setPath(target)
        item.accept()
        self.add_download_item(item)

    def add_download_item(self, item):
        self.downloads_bar.setVisible(True)

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(4, 2, 4, 2)
        row_layout.setSpacing(8)

        name_label = QLabel(item.downloadFileName())
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(0)
        open_button = QPushButton("Open")
        open_button.setEnabled(False)

        row_layout.addWidget(name_label)
        row_layout.addWidget(progress, 1)
        row_layout.addWidget(open_button)

        self.downloads_layout.addWidget(row)

        def on_progress(received, total):
            if total > 0:
                progress.setValue(int(received * 100 / total))

        def on_finished():
            progress.setValue(100)
            open_button.setEnabled(True)

        def on_open():
            QDesktopServices.openUrl(QUrl.fromLocalFile(item.path()))

        item.downloadProgress.connect(on_progress)
        item.finished.connect(on_finished)
        open_button.clicked.connect(on_open)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())