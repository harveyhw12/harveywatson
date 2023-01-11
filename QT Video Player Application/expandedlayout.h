#ifndef EXPANDEDLAYOUT_H
#define EXPANDEDLAYOUT_H

#include <QVBoxLayout>
#include <QWidget>
#include <functional>

// class for custom layout to show widgets once "Show More" button clicked
class ExpandedLayout : public QVBoxLayout
{
public:
    // widget to contain a grid layout for the videos
    QWidget * grid;
    // used to redraw the grid
    std::function<void()> reset_grid_func;

    ExpandedLayout(QWidget * g);

    //void setGrid(QWidget * g);
    int getColumnCount();
    void setGeometry(const QRect& rect);
    void setGridFunc(std::function<void()> resetGrid);
};

#endif // EXPANDEDLAYOUT_H
