#ifndef THE_WINDOW_H
#define THE_WINDOW_H

#include <QWidget>
#include <QStackedLayout>
#include "the_button.h"

// custom window widget
class TheWindow: public QWidget {

public:
    // boolean for if the view is expanded
    bool expandedView;
    bool welcomeView;
    int sort_mode = 0;
    int asc = 0;

    // widgets for expanded and regular views
    QWidget* standard;
    QWidget* expanded;
    QWidget* welcome;

    QWidget* grid;

    // stacked layout to switch between the objects
    QStackedLayout* layout;

    // constructor with standard and expanded layouts
    TheWindow(QLayout *s, QLayout *e, QLayout *w) : QWidget() {

        // initialisation
        expandedView = false;
        welcomeView = false;
        layout = new QStackedLayout();

        setLayout(layout);

        standard = new QWidget(this);
        expanded = new QWidget(this);
        welcome = new QWidget(this);

        // start with standard (default) view
        standard->setLayout(s);
        expanded->setLayout(e);
        welcome->setLayout(w);

        // add widgets to layout
        layout->addWidget(standard);
        layout->addWidget(expanded);
        layout->addWidget(welcome);

        openWelcome();
    }

    void setGeometry(const QRect& rect);
    void setGrid(QWidget * g);
    int getColumnCount();


// slots for opening and closing the expanded menu
public slots:
    void openExpanded();
    void closeExpanded();
    void closeWelcome();
    void openWelcome();
    void setSortType(int sortIndex);
    void setAscType(int ascIndex);
    int getSortType();
    int getAscType();
};

#endif // THE_WINDOW_H
