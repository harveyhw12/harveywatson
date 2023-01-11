#ifndef LOADER_H
#define LOADER_H

using namespace std;

#include <QMediaPlayer>
#include "button_vector.h"

// container to load the videos into the mediaplayer and extract the metadata
class MediaLoader: public QMediaPlayer{
    Q_OBJECT

    QUrl* url;
    ButtonVector* out;

public:
    MediaLoader(QUrl* u, ButtonVector* o): QMediaPlayer() {
        url = u;
        out = o;
        connect(this, &QMediaPlayer::mediaStatusChanged, this, &MediaLoader::onLoad);
    }

private slots:
    void onLoad(QMediaPlayer::MediaStatus status);

};

#endif // LOADER_H
