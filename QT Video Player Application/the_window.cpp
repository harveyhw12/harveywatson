#include "the_window.h"
#include "the_button.h"
 #include <QDebug>


void TheWindow::setGeometry(const QRect& rect) {
    QWidget::setGeometry(rect);
    grid->setGeometry(rect.x(), rect.y(), rect.width()+155, rect.height());
}

void TheWindow::setGrid(QWidget *g){
    grid = g;
}

int TheWindow::getColumnCount(){
    return (this->width() / 250);
}

// functions for changing the view
void TheWindow::openExpanded(){
    if(expandedView == false){ // if it's not expanded, open
        expandedView = true;
        layout->setCurrentIndex(1);
    }
}

void TheWindow::closeExpanded(){
        if(expandedView == true){ // if it's expanded, close
            expandedView = false;
    }
        layout->setCurrentIndex(0);
}

void TheWindow::openWelcome(){
    if(welcomeView == false){
        welcomeView = true;
        layout->setCurrentIndex(2);
    }
}

void TheWindow::closeWelcome(){
    if(welcomeView == true){
        welcomeView = false;
        layout->setCurrentIndex(0);
    }
}

void TheWindow::setSortType(int sortIndex){
    sort_mode = sortIndex;
    qDebug() << sort_mode;
}

void TheWindow::setAscType(int ascIndex){
    asc = ascIndex;
    qDebug() << asc;
}



int TheWindow::getSortType(){
    return sort_mode;
}


int TheWindow::getAscType(){
    return asc;
}


