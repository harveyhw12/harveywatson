#ifndef COLOUR_SCHEME_H
#define COLOUR_SCHEME_H

#include <QObject>
#include <QString>
#include <QApplication>
#include <QFont>
#include <QFileInfo>

// colour scheme class used to change styling of app(lication)
class ColourScheme: public QObject{
    Q_OBJECT

private:
    QString activeColourScheme;

public:
    ColourScheme(QApplication * app): QObject(){
        activeColourScheme = "light";
        setLightMode(app);
    }

    QString getCurrentColourScheme(){
        return activeColourScheme;
    }

    void setActiveColourScheme(QString scheme){
        activeColourScheme = scheme;
    }

    void setLightMode(QApplication * app){
        setActiveColourScheme("light");

        //"QMenu::item::selected {background-color: #696662;}"

        QFont segoeUI = QFont("Segoe UI");
        app->setStyleSheet("QWidget { background-color: #CFC9C2 ; color: black;} "
                           "QToolBar {background-color : #A8A49E;}"
                           "QToolButton {background-color : #A8A49E;}"
                           "QToolButton:hover {background-color : #696662; border : none; padding: 0px 5px 0px 5px;}"
                           "QMenu {background-color: #A8A49E;}"
                           "QMenu::item::selected {background-color: #696662;}"
                           "QWindow {background-color: #E8E1D9;}"
                           "QComboBox {background-color : #A8A49E; border : none; border-radius : 3px;}"
                           "QComboBox:hover {background-color : #696662;}"
                           "QLineEdit { border-radius : 8px; padding : 3px 6px 3px 6px; background-color: white;}"
                           "QPushButton {background-color: #A8A49E; border : none;}"
                           "QPushButton {  padding: 3px 6px 3px 6px; border-radius : 8px;}"
                           "QPushButton:hover {background-color: #696662;}"
                           "QPushButton:menu-indicator:pressed {background-color: black;}"
                           "ThePlayer {background-color : transparent;}"
                           "TheButton {border : none;}");
        app->setFont(segoeUI);
    }

    void setHighContrastMode(QApplication * app){
        setActiveColourScheme("high contrast");
        QFont f = QFont("Segoe UI");
        app->setStyleSheet("QWidget { background-color: #000000 ; color: white;} "
                           "QToolBar {background-color : black;}"
                           "QToolButton {background-color : black;}"
                           "QToolButton:hover {background-color : blue; border : none; padding: 0px 5px 0px 5px;}"
                           "QMenu {background-color: black;}"
                           "QMenu::item::selected {background-color: blue;}"
                           "QWindow {background-color: #E8E1D9;}"
                           "QComboBox {background-color : #000000; border : 2px solid white; border-radius : 3px;}"
                           "QComboBox:hover {background-color : blue;}"
                           "QComboBox::item::hover { background-color : white;}"
                           "QComboBox QAbstractItemView {background-color : blue;}"
                           "QLineEdit { border-radius : 8px; padding : 3px 6px 3px 6px; background-color: white; color : blue;}"
                           "QPushButton {background-color: #000000; padding: 3px 6px 3px 6px; border-radius : 8px;}"
                           "QPushButton:hover {background-color: blue;}"
                           "QPushButton:menu-indicator:pressed {background-color: black;}"
                           "QSlider::groove:horizontal { border: 1px solid #bbb; background: white; height: 10px; border-radius: 4px; }"
                           "QSlider::sub-page:horizontal { background: blue; border: 1px solid #777; height: 10px; border-radius: 4px;}"
                           "QSlider::handle:horizontal { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ccc); border: 1px solid #777; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}"
                           "QSlider::handle:horizontal:hover {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #fff, stop:1 #ddd);border: 1px solid #444;border-radius: 4px;}"
                           "TheButton {border : none;}");
        app->setFont(f);
    }

    void setDarkMode(QApplication * app){
        setActiveColourScheme("dark");
        QFont f = QFont("Segoe UI");
        app->setStyleSheet("QWidget { background-color: #333333 ; color: white}"
                           "QMenu {background-color: #333333;}"
                           "QComboBox {background-color : #646B6E; border : none}"
                           "QPushButton {background-color: #646B6E; border : none;}"
                           "QPushButton {  padding: 3px 6px 3px 6px; border-radius : 8px;}"
                           "QPushButton:hover {background-color: #7C8589;}"
                           "QMenu::item::selected {background-color: #696662;}"
                           "QLineEdit { border-radius : 8px; padding : 3px 6px 3px 6px; background-color: #646B6E;}"
                           "QComboBox {background-color : #646B6E; border : none; border-radius : 8px; padding : 3px 0px 3px 0px;}");
        app->setFont(f);
    }



};

#endif // COLOUR_SCHEME_H
