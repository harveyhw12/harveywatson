//
// Created by twak on 11/11/2019.
//

#include "the_player.h"
#include <QMediaMetaData>
#include <QDebug>

using namespace std;

// all buttons have been setup, store pointers here
void ThePlayer::setContent(std::vector<TheButton*>* b, std::vector<TheButtonInfo>* i) {
    buttons = b;
    infos = i;
    //jumpTo(buttons -> at(0) -> info);
}

void ThePlayer::playStateChanged (QMediaPlayer::State ms) {
    switch (ms) {
        case QMediaPlayer::State::StoppedState:
              // set video to start and reload it
              setPosition(0);
              play();
              pause();
            break;
        case QMediaPlayer::State::PlayingState:
            emit onVideoPlay();
            break;
    default:
        break;
    }
}

TheButtonInfo* ThePlayer::getCurrentlyPlaying(){
    return currentlyPlaying;
}


void ThePlayer::moveVideoOnRight(){
    // if not playing, do nothing
    // else
    int index = -1;
    for (int i =0; i < infos->size(); i++){
        if(infos->at(i).url == currentlyPlaying->url){
            // index found
            index = i;

            // if i is last video, do nothing
            break;
        }
    }
    if(index != -1){
        if(index == infos->size() - 1){
            index = -1;
        }
        emit jumpTo(&infos->at(index+1));
    }
}


void ThePlayer::moveVideoOnLeft(){
    // if not playing, do nothing
    // else
    int index = -1;
    for (int i =0; i < infos->size(); i++){
        if(infos->at(i).url == currentlyPlaying->url){
            // index found
            index = i - 1;

            // if i is last video, do nothing
            break;
        }
    }
    if(index == -1){
        index = infos->size() - 1;
    }
    emit jumpTo(&infos->at(index));

}


void ThePlayer::mediaChanged(QMediaPlayer::MediaStatus status){
    if(status == QMediaPlayer::MediaStatus::BufferedMedia){
        qDebug() << availableMetaData();
        qDebug() << metaData(QMediaMetaData::Year);
        qDebug() << duration();
        qDebug() << this->currentMedia().canonicalUrl().toString();

    }
}

// definition of slots

// play the video represented by button
void ThePlayer::jumpTo (TheButtonInfo* button) {
    setMedia( * button -> url);
    currentlyPlaying = button;
    emit mediaInfoChanged(button);
    play();
}

void ThePlayer::muteMedia(){
    if(isMuted() == false){
        ThePlayer::setMuted(true);
    }
    else{
        ThePlayer::setMuted(false);
    }
}

void ThePlayer::pressPlay() {
    play();
}

void ThePlayer::pressPause() {
    pause();
}

void ThePlayer::updateSpeed(int speedIndex){
    float speed;
    if(speedIndex == 0){
        speed = 0.5;
    }
    else if(speedIndex == 2){
        speed = 1.5;
    }
    else if(speedIndex == 3){
        speed = 2.0;
    }
    else{
        speed = 1.0;
    }
    setPlaybackRate(speed);
}


void ThePlayer::changeVolume(int volume){
    setVolume(volume);
}
