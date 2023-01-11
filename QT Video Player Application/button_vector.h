#ifndef BUTTON_VECTOR_H
#define BUTTON_VECTOR_H

#include <QObject>
#include <QWidget>
#include <vector>
#include "the_button.h"
#include <QMediaPlayer>

// container for buttons

using namespace std;

class ButtonVector: public QObject {
    Q_OBJECT

private:
    vector<TheButtonInfo>* videos;
    int expectedLength;
    vector<QMediaPlayer*>*  loaders;
public:

    ButtonVector(): QObject() {
        videos = new vector<TheButtonInfo>();
        loaders = new vector<QMediaPlayer*>();
        expectedLength = 0;
    }

    vector<TheButtonInfo>* getVideos(){
        return videos;
    }

    int getExpectedLength(){
        return expectedLength;
    }

    void setExpectedLength(int length){
        expectedLength = length;
    }

    void add(TheButtonInfo button){
        videos->push_back(button);
        emit updateProgress(videos->size());
        if(videos->size() == expectedLength){
            delete(loaders);
            emit completed(videos);
        }
    }

    void addLoader(QMediaPlayer* loader){
        loaders->push_back(loader);
    }

    int size(){
       return videos->size();
    }

    TheButtonInfo at(int index){
        return videos->at(index);
    }

    TheButtonInfo* atRef(int index){
        return const_cast<TheButtonInfo*>(&(videos->at(index)));
    }

signals:
    void updateProgress(int value);

    void completed(vector<TheButtonInfo>* buttons);
};

#endif // BUTTON_VECTOR_H
