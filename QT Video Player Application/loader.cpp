#include "loader.h"
#include <QMediaPlayer>
#include <QMediaMetaData>
#include <QImage>
#include <QPixmap>
#include <QIcon>
#include <QFile>
#include <QImageReader>
#include "the_button.h"

void MediaLoader::onLoad(QMediaPlayer::MediaStatus status){
    // once media is loaded the metadata can be extracted
    if(status == QMediaPlayer::MediaStatus::BufferedMedia || status == QMediaPlayer::MediaStatus::LoadedMedia){
        QStringList metadata = availableMetaData();

        VideoMetadata data = VideoMetadata();

        QFile *file = new QFile(url->toLocalFile());

        data.setFilename(url->fileName());
        data.setDuration(duration());
        data.setFilesize(file->size());
        if(metadata.size() > 0){
            if(metadata.contains("datetime")){
                QDateTime datetime = metaData(QMediaMetaData::DateTimeOriginal).value<QDateTime>();
                data.setCreationTime(datetime);
            }
            if(metadata.contains("Resolution")){
                QSize resolution = metaData(QMediaMetaData::Resolution).value<QSize>();
                data.setResolution(resolution.width(), resolution.height());
            }
        } else {
            data.setCreationTime(QDateTime::fromSecsSinceEpoch(0));
        }

        QString localUrl = url->toString().right(url->toString().length() - 7);
#if defined(_WIN32)
        localUrl.remove(0,1);
#endif
        // attempt to get thumbnail
        QString thumb = localUrl.left(localUrl.length() - 4) + ".png";

        if(QFile::exists(thumb)){
            QImageReader* imageReader = new QImageReader(thumb);
            QImage sprite = imageReader->read(); // read the thumbnail
            if(!sprite.isNull()){
                out->add(TheButtonInfo(url, QPixmap::fromImage(sprite), data)); // add to the output list
            } else
            {
               out->setExpectedLength(out->getExpectedLength() - 1);
            }
        } else
        {
            out->setExpectedLength      (out->getExpectedLength() - 1);
        }

    }
}
