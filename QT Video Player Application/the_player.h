//
// Created by twak on 11/11/2019.
//

#ifndef CW2_THE_PLAYER_H
#define CW2_THE_PLAYER_H


#include <QApplication>
#include <QMediaPlayer>
#include "the_button.h"
#include <vector>
#include <QTimer>

using namespace std;

// custom mediaplayer
class ThePlayer : public QMediaPlayer {

Q_OBJECT

private:
    vector<TheButtonInfo>* infos;
    vector<TheButton*>* buttons;
    TheButtonInfo* currentlyPlaying = NULL;
    QTimer* mTimer;
    long updateCount = 0;
    bool muted = false;

public:

    ThePlayer() : QMediaPlayer(NULL) {
        setVolume(50); // be slightly less annoying
        connect (this, SIGNAL (stateChanged(QMediaPlayer::State)), this, SLOT (playStateChanged(QMediaPlayer::State)) );
        connect (this, &QMediaPlayer::mediaStatusChanged, this, &ThePlayer::mediaChanged);
    }

    // all buttons have been setup, store pointers here
    void setContent(vector<TheButton*>* b, vector<TheButtonInfo>* i);
    //bool isMuted();
    TheButtonInfo* getCurrentlyPlaying();

private slots:
    void mediaChanged(QMediaPlayer::MediaStatus status);
    // change the image and video for one button every one second
    void playStateChanged (QMediaPlayer::State ms);



public slots:
    void muteMedia();
    // start playing this ButtonInfo
    void jumpTo (TheButtonInfo* button);

    // use this to play the video
   void pressPlay();

   // use this to pause the video
   void pressPause();

   // used to switch currently playing video for keyboard shortcuts
   void moveVideoOnRight();
   void moveVideoOnLeft();


   // use this to change the volume
   void changeVolume(int volume);

   void updateSpeed(int speedIndex);

signals:
   void onVideoPlay();
   void mediaInfoChanged(TheButtonInfo* info);
   void changeRate(qreal rate);
};

#endif //CW2_THE_PLAYER_H
