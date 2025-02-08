from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QRadialGradient, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, QPoint, QRectF, QPropertyAnimation, QEasingCurve
import sys
import time
import math

class AnalogClock(QMainWindow):
    def __init__(self):
        super().__init__()
        # QFontDatabase.addApplicationFont("Tangerine-Regular.ttf")
        QFontDatabase.addApplicationFont("GreatVibes-Regular.ttf")
        self.opacity = 1.0
        self.hover = False
        self.dragging = False
        self.screen = QDesktopWidget().screenGeometry()        
        self.initUI()        

    def initUI(self):
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Analog Clock')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)
        
        # Animáció beállítása
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(300)  # 300 ms
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)        

    def enterEvent(self, event):
        self.hover = True
        self.animation.setStartValue(self.windowOpacity())
        self.animation.setEndValue(0.1)  # Majdnem átlátszó
        self.animation.start()

    def leaveEvent(self, event):
        self.hover = False
        self.animation.setStartValue(self.windowOpacity())
        self.animation.setEndValue(1.0)  # Teljesen látható
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Középpont és sugár
        center = QPoint(self.width() // 2, self.height() // 2)
        radius = min(self.width(), self.height()) // 2 - 20

        # Külső árnyék
        painter.setPen(Qt.NoPen)
        for i in range(10):
            opacity = 100 - i * 10
            painter.setBrush(QColor(0, 0, 0, opacity))
            painter.drawEllipse(center, radius + 5 - i, radius + 5 - i)

        # Óra háttere
        gradient = QRadialGradient(center, radius)
        gradient.setColorAt(0, QColor(240, 240, 240))
        gradient.setColorAt(0.8, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(220, 220, 220))
        
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(180, 180, 180), 2))
        painter.drawEllipse(center, radius, radius)

        # Díszítő kör
        painter.setPen(QPen(QColor(160, 160, 160), 1))
        painter.drawEllipse(center, radius - 10, radius - 10)

        # "Sonnet" felirat kalligrafikus betűtípussal
        painter.setPen(QColor(60, 60, 100))
        # fancy_font = QFont("Tangerine", 42)
        fancy_font = QFont("GreatVibes", 36)
        painter.setFont(fancy_font)
        text_rect = QRectF(center.x() - radius/2, center.y() + radius/4, radius, radius/3)
        painter.drawText(text_rect, Qt.AlignCenter, "Sonnet")

        # Óraszámok normál betűtípussal
        normal_font = QFont()
        normal_font.setPointSize(12)
        normal_font.setBold(True)
        painter.setFont(normal_font)

        for i in range(60):
            angle = i * 6
            if i % 5 == 0:
                num = i // 5 if i > 0 else 12
                num_angle = math.radians(angle - 90)
                num_x = center.x() + (radius - 35) * math.cos(num_angle)
                num_y = center.y() + (radius - 35) * math.sin(num_angle)
                painter.setPen(QColor(60, 60, 60))
                painter.drawText(QRectF(num_x - 15, num_y - 15, 30, 30), 
                               Qt.AlignCenter, str(num))
                
                painter.setPen(QPen(QColor(60, 60, 60), 3))
                x1 = center.x() + (radius - 15) * math.cos(math.radians(angle - 90))
                y1 = center.y() + (radius - 15) * math.sin(math.radians(angle - 90))
                x2 = center.x() + radius * math.cos(math.radians(angle - 90))
                y2 = center.y() + radius * math.sin(math.radians(angle - 90))
            else:
                painter.setPen(QPen(QColor(120, 120, 120), 1))
                x1 = center.x() + (radius - 5) * math.cos(math.radians(angle - 90))
                y1 = center.y() + (radius - 5) * math.sin(math.radians(angle - 90))
                x2 = center.x() + radius * math.cos(math.radians(angle - 90))
                y2 = center.y() + radius * math.sin(math.radians(angle - 90))
            
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Aktuális idő
        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        # Órák mutatója
        hour_angle = hours * 30 + minutes * 0.5 - 90
        hour_hand = QPen(QColor(40, 40, 40), 4, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(hour_hand)
        hour_x = center.x() + radius * 0.5 * math.cos(math.radians(hour_angle))
        hour_y = center.y() + radius * 0.5 * math.sin(math.radians(hour_angle))
        painter.drawLine(center, QPoint(int(hour_x), int(hour_y)))

        # Percek mutatója
        min_angle = minutes * 6 + seconds * 0.1 - 90
        min_hand = QPen(QColor(60, 60, 60), 3, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(min_hand)
        min_x = center.x() + radius * 0.7 * math.cos(math.radians(min_angle))
        min_y = center.y() + radius * 0.7 * math.sin(math.radians(min_angle))
        painter.drawLine(center, QPoint(int(min_x), int(min_y)))

        # Másodperc mutatója
        sec_angle = seconds * 6 - 90
        painter.setPen(QPen(QColor(200, 0, 0), 1, Qt.SolidLine, Qt.RoundCap))
        sec_x = center.x() + radius * 0.85 * math.cos(math.radians(sec_angle))
        sec_y = center.y() + radius * 0.85 * math.sin(math.radians(sec_angle))
        painter.drawLine(center, QPoint(int(sec_x), int(sec_y)))

        # Középpont
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(200, 0, 0))
        painter.drawEllipse(center, 5, 5)
        painter.setBrush(QColor(60, 60, 60))
        painter.drawEllipse(center, 3, 3)

    def jumpToOtherSide(self):
        current_x = self.x()
        screen_width = self.screen.width()
        
        if current_x < screen_width / 2:
            new_x = screen_width - self.width() - 10
        else:
            new_x = 10
        
        # Animáció az ugráshoz
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(200)  # 200ms
        self.anim.setStartValue(self.geometry())
        new_geometry = self.geometry()
        new_geometry.moveLeft(new_x)
        self.anim.setEndValue(new_geometry)
        self.anim.start()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.dragStart = event.globalPos()
        self.dragging = False
        # Átlátszóság beállítása
        self.animation.setStartValue(self.windowOpacity())
        self.animation.setEndValue(0.5)
        self.animation.start()

    def mouseReleaseEvent(self, event):
        if not self.dragging:
            self.jumpToOtherSide()

        self.dragging = False
        
        # Átlátszóság visszaállítása
        if self.hover:
            self.animation.setStartValue(self.windowOpacity())
            self.animation.setEndValue(0.1)
            self.animation.start()

    def mouseMoveEvent(self, event):
        # Ha az egér elmozdult több mint 5 pixelt, akkor húzásnak számít
        if (event.globalPos() - self.dragStart).manhattanLength() > 5:
            self.dragging = True
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def contextMenuEvent(self, event):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = AnalogClock()
    clock.show()
    sys.exit(app.exec_())
