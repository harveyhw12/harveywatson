#ifndef VIDEOMETADATA_H
#define VIDEOMETADATA_H

#include <QString>
#include <QDateTime>

// class to store video metadata read by loader.cpp, all buttons have a metadata object attribute
class VideoMetadata
{
public:
    QString filename;
    QDateTime creationTime;
    int framerate;
    int duration;
    QString title;
    QString subtitle;
    QString author;
    int resolution[2];
    double location[2];
    int filesize;


    VideoMetadata();

    void setFilename(QString name);
    void setCreationTime(QDateTime time);
    void setFramerate(int framerate);
    void setDuration(int dur);
    void setTitle(QString title);
    void setSubtitle(QString subtitle);
    void setAuthor(QString author);
    void setResolution(int width, int height);
    void setLocation(double longtitude, double latitude);
    void setFilesize(int filesize);

    QString getFilename();
    QDateTime getCreationTime();
    int getFramerate();
    int getDuration();
    QString getTitle();
    QString getSubtitle();
    QString getAuthor();
    int* getResolution();
    double* getLocation();
    int getFilesize();



};


#endif // VIDEOMETADATA_H
