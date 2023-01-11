#include "expandedlayout.h"

ExpandedLayout::ExpandedLayout(QWidget * g)
{
    grid = g;
}

// used to redraw buttons on search
void ExpandedLayout::setGeometry(const QRect& rect) {
    QVBoxLayout::setGeometry(rect);
    grid->setGeometry(rect.x(), rect.y(), rect.width()+155, rect.height());
    reset_grid_func();
}

// resets the grid layout
void ExpandedLayout::setGridFunc(std::function<void()> resetGrid){
    reset_grid_func = resetGrid;
}
