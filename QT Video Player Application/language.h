#ifndef LANGUAGETEXT_H
#define LANGUAGETEXT_H

#include <QString>
#include <QStringList>
#include <QObject>
#include <vector>

// language class to change system language
class Language : public QObject {
public:
    // setters trigger the language
    void triggerEnglish();
    void triggerGerman();
    void triggerFrench();
    void triggerSpanish();
    void triggerRussian();
    void triggerTurkish();
    void triggerDutch();

    QString english = "🇬🇧 English";
    QString french = "🇫🇷 Française";
    QString russian = "🇷🇺 Русский";
    QString german = "🇩🇪 Deutsch";
    QString spanish = "🇪🇸 Español";
    QString dutch = "🇳🇱 Nederlands";
    QString turkish = "🇹🇷 Türk";

    QString language, colour_scheme, dark_mode, light_mode, high_contrast_mode, play, pause,
    back, share, search, sort, ascending, descending, show_more, date, duration, filename,
    filesize, tags, import, help, fullscreen, exit_fullscreen, mute, toggle_play_pause, helpMessage,
    metadata, no_videos, volume;

    Language();

private slots:
    void setLang(QString lang);
};

#endif // LANGUAGETEXT_H
