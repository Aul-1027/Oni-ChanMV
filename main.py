from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QScrollArea, QTextEdit)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys
import os
import xml.etree.ElementTree as ET
import re

def format_description(text):
    if text is None:
        return 'N/A'
    
    # text = re.sub(r'\s+', ' ', text)
    # text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)
    # text = re.sub(r'\s*\n\s*', '\n\n', text)
    # text = re.sub(r'\n{3,}', '\n\n', text)
    # text = text.strip()
    
    return text

class CustomTextEdit(QTextEdit):
    def wheelEvent(self, event):
        # イベントを常に受け取り、親への伝播を防ぐ
        scrollbar = self.verticalScrollBar()
        current_value = scrollbar.value()
        scroll_unit = event.angleDelta().y()
        
        # スクロール後の値を計算
        new_value = current_value - (scroll_unit / 120) * scrollbar.singleStep()
        
        # 値を範囲内に収める
        new_value = max(scrollbar.minimum(), min(new_value, scrollbar.maximum()))
        
        # スクロール位置を設定
        scrollbar.setValue(int(new_value))
        
        # イベントを消費（親へ伝播させない）
        event.accept()

class ModViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oni-ChanMV")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: palette(window);
                color: palette(windowText);
            }
            QLabel {
                color: palette(windowText);
            }
            QTextEdit {
                background-color: palette(base);
                color: palette(text);
                border: 1px solid palette(mid);
                border-radius: 5px;
            }
            QScrollArea {
                background-color: palette(window);
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        
        base_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\2135150"
        
        for folder in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder)
            if os.path.isdir(folder_path):
                mod_widget = QWidget()
                mod_layout = QHBoxLayout(mod_widget)
                mod_layout.setContentsMargins(5, 5, 5, 5)
                
                info_layout = QVBoxLayout()
                info_layout.setSpacing(5)
                
                xml_path = os.path.join(folder_path, "package.xml")
                if os.path.exists(xml_path):
                    try:
                        tree = ET.parse(xml_path)
                        root = tree.getroot()
                        
                        fields = [
                            ('Title', 'title'),
                            ('ID', 'id'),
                            ('Author', 'author'),
                            ('Load Priority', 'loadPriority'),
                            ('Version', 'version')
                        ]
                        
                        for label, tag in fields:
                            field_layout = QHBoxLayout()
                            field_layout.setSpacing(5)
                            
                            label_text = QLabel(f"<b>{label}:</b>")
                            label_text.setStyleSheet("font-size: 10pt;")
                            label_text.setFixedWidth(80)
                            field_layout.addWidget(label_text)
                            
                            value_text = QLabel(root.find(tag).text if root.find(tag) is not None else 'N/A')
                            value_text.setWordWrap(True)
                            value_text.setStyleSheet("font-size: 10pt;")
                            field_layout.addWidget(value_text)
                            
                            info_layout.addLayout(field_layout)
                        
                        desc_layout = QVBoxLayout()
                        desc_label = QLabel("<b>Description:</b>")
                        desc_label.setStyleSheet("font-size: 10pt;")
                        desc_layout.addWidget(desc_label)
                        
                        desc_text = CustomTextEdit()
                        desc_text.setReadOnly(True)
                        desc_text.setMinimumHeight(100)
                        desc_text.setMaximumHeight(150)
                        desc_text.setStyleSheet("""
                            QTextEdit {
                                padding: 5px;
                                font-size: 10pt;
                            }
                        """)
                        
                        description = root.find('description').text if root.find('description') is not None else 'N/A'
                        formatted_description = format_description(description)
                        desc_text.setText(formatted_description)
                        
                        desc_layout.addWidget(desc_text)
                        info_layout.addLayout(desc_layout)
                        
                    except ET.ParseError:
                        info_layout.addWidget(QLabel("Error reading package.xml"))
                
                mod_layout.addLayout(info_layout)
                
                preview_path = os.path.join(folder_path, "preview.jpg")
                if os.path.exists(preview_path):
                    preview_label = QLabel()
                    pixmap = QPixmap(preview_path)
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    preview_label.setPixmap(scaled_pixmap)
                    preview_label.setStyleSheet("padding: 5px;")
                    mod_layout.addWidget(preview_label)
                
                separator = QWidget()
                separator.setFixedHeight(1)
                separator.setStyleSheet("""
                    background-color: palette(mid);
                    margin: 5px 0px;
                """)
                
                scroll_layout.addWidget(mod_widget)
                scroll_layout.addWidget(separator)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

def main():
    app = QApplication(sys.argv)
    viewer = ModViewer()
    viewer.show()
    return app.exec()

if __name__ == "__main__":
    main()