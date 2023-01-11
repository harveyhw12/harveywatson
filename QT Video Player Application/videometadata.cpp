#include "videometadata.h"

VideoMetadata::VideoMetadata()
{

}

void VideoMetadata::setFilename(QString name){
    filename = name;
}

void VideoMetadata::setCreationTime(QDateTime time){
    creationTime = time;
}

void VideoMetadata::setFramerate(int rate){
    framerate = rate;
}

void VideoMetadata::setDuration(int dur){
    duration = dur;
}

void VideoMetadata::setTitle(QString titl){
    title = titl;
}

void VideoMetadata::setSubtitle(QString subtitl){
    subtitle = subtitl;
}

void VideoMetadata::setAuthor(QString auth){
    author = auth;
}

void VideoMetadata::setResolution(int w, int h){
    resolution[0] = w;
    resolution[1] = h;
}

void VideoMetadata::setLocation(double longt, double lat){
    location[0] = longt;
    location[1] = lat;
}

void VideoMetadata::setFilesize(int size){
    filesize = size;
}

QString VideoMetadata::getFilename(){
    return filename;
}

QDateTime VideoMetadata::getCreationTime(){
    return creationTime;
}

int VideoMetadata::getFramerate(){
    return framerate;
}

int VideoMetadata::getDuration(){
    return duration;
}

QString VideoMetadata::getTitle(){
    return title;
}

QString VideoMetadata::getSubtitle(){
    return subtitle;
}

QString VideoMetadata::getAuthor(){
    return author;
}

int*  VideoMetadata::getResolution(){
    return resolution;
}

double* VideoMetadata::getLocation(){
    return location;
}

int VideoMetadata::getFilesize(){
    return filesize;
}
