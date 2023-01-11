/*
 *
 *    ______
 *   /_  __/___  ____ ___  ___  ____
 *    / / / __ \/ __ `__ \/ _ \/ __ \
 *   / / / /_/ / / / / / /  __/ /_/ /
 *  /_/  \____/_/ /_/ /_/\___/\____/
 *              video for sports enthusiasts...
 *
 *  2811 cw3 : twak
 */

#include <iostream>
#include <QApplication>
#include <QtMultimediaWidgets/QVideoWidget>
#include <QMediaPlaylist>
#include <string>
#include <vector>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QHBoxLayout>
#include <QtCore/QFileInfo>
#include <fstream>
#include <QtWidgets/QFileIconProvider>
#include <QDesktopServices>
#include <QImageReader>
#include <QPixmap>
#include <QMessageBox>
#include <QtCore/QDir>
#include <QtCore/QDirIterator>
#include <QSlider>
#include <QLineEdit>
#include <QFileDialog>
#include <QScrollArea>
#include <QLabel>
#include "the_player.h"
#include "the_button.h"
#include "the_window.h"
#include <cmath>
#include <algorithm>
#include "language.h"
#include <QToolBar>
#include <QToolButton>
#include <QMenu>
#include <QObject>
#include <QMediaMetaData>
#include <QComboBox>
#include <QShortcut>
#include "button_vector.h"
#include "loader.h"
#include <QProgressBar>
#include <QFont>
#include "colour_scheme.h"
#include <QWindow>
#include <QSizePolicy>
#include "expandedlayout.h"
#include <QSpacerItem>

using namespace std;

Language * activeLanguage;

QString filesizeToString(int bytes){
    QString filesize = "";


    if(bytes / (1024 * 1024 * 1024) > 0){
        double gb = bytes / (1024 * 1024 * 1024);
        filesize.append(QString::number(gb));
        filesize.append(" GB");
    } else if (bytes / (1024 * 1024) > 0) {
        double mb = bytes / (1024 * 1024);
        filesize.append(QString::number(mb));
        filesize.append(" MB");
    } else if (bytes / 1024 > 0) {
        double kb = bytes / 1024;
        filesize.append(QString::number(kb));
        filesize.append(" kB");
    } else {
       filesize.append(QString::number(bytes));
       filesize.append(" B");
    }

    return filesize;
}

QString intToStringTime(int time){
    QString duration = "";
    int hours = time / (1000 * 60 * 60);
    time -= hours * (1000 * 60 * 60);

    int mins = time / (1000 * 60);
    time -= mins * 1000 * 60;

    int seconds = time / 1000;

    if(hours < 10){
        duration.append("0");
    }
    duration.append(QString::number(hours));
    duration.append(":");
    if(mins < 10){
        duration.append("0");
    }
    duration.append(QString::number(mins));
    duration.append(":");
    if(seconds < 10){
        duration.append("0");
    }
    duration.append(QString::number(seconds));
    return duration;

}

// comparators for sorting
bool creationTimeComparator(const TheButtonInfo lhs, const TheButtonInfo rhs){
    return lhs.data.creationTime < rhs.data.creationTime;
}

bool durationComparator(const TheButtonInfo lhs, const TheButtonInfo rhs){
    return lhs.data.duration < rhs.data.duration;
}

bool filesizeComparator(const TheButtonInfo lhs, const TheButtonInfo rhs){
    return lhs.data.filesize < rhs.data.filesize;
}

// sort videos vector based upon attribute and order (if descend is true, in descending order)
void sortByMetadata(vector<TheButtonInfo>* videos, int attribute, int descend){
    if(attribute == 1){ //FILESIZE
        sort(videos->begin(), videos->end(), &filesizeComparator);

    }
    else if(attribute == 0){ //DURATION

        sort(videos->begin(), videos->end(), &durationComparator);

    }
    else if(attribute == 2){ //DATE
        sort(videos->begin(), videos->end(), &creationTimeComparator);

    }
    if(descend){
        reverse(videos->begin(), videos->end());
    }

}

void setActiveLanguage(Language * language){
    activeLanguage = language;
}

// used to re-render the widget representing a single video
TheButton* renderButton(int i, TheButtonInfo info, ThePlayer* player, QWidget* buttonWidget,
                        QGridLayout* gridLayout, QWidget* gridWidget, int columnCount){

    QVBoxLayout *video_results_layout = new QVBoxLayout();
    QWidget* video_results_widget = new QWidget();

    video_results_widget->setMaximumSize(210, 500);
    video_results_widget->setLayout(video_results_layout);

    TheButton *button = new TheButton(buttonWidget);
    video_results_widget->setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    button->connect(button, &TheButton::jumpTo, player, &ThePlayer::jumpTo); // when clicked, close the expanded view and tell the player to play.
    QString label_text = info.data.getFilename();
    QLabel *vid_duration = new QLabel(intToStringTime(info.data.getDuration()));
    QLabel *vid_name= new QLabel(label_text);
    QLabel *vid_size = new QLabel(filesizeToString(info.data.getFilesize()));
    QString tmp = info.data.getCreationTime().toString();
    QLabel *creationTime = new QLabel(info.data.getCreationTime().toString());
    video_results_layout->addWidget(button, Qt::AlignTop);
    video_results_layout->addWidget(vid_name, Qt::AlignTop);
    video_results_layout->addWidget(vid_duration, Qt::AlignTop);
    video_results_layout->addWidget(vid_size, Qt::AlignTop);
    video_results_layout->addWidget(creationTime, Qt::AlignTop);
    gridLayout->addWidget(video_results_widget, i/columnCount, i % columnCount,
                          Qt::AlignTop|Qt::AlignHCenter);

    return button;
}

// render all button videos in the expanded view
vector<TheButton*>* renderGridInit(vector<TheButtonInfo>* vids, ThePlayer* player,
                                   QWidget* buttonWidget, QGridLayout* gridLayout,
                                   QWidget* gridWidget, QWidget* window, int columnCount){
    vector<TheButton*>* buttons = new vector<TheButton*>();
    int* row_count = new int();
    *row_count = 0;

    // loop over ALL videos to display them in a list
    for ( int i = 0; i < vids->size(); i++ ) {
        TheButton* button = renderButton(i, vids->at(i), player, buttonWidget, gridLayout,
                                         gridWidget, columnCount);
        buttons->push_back(button);
        button->init(&(vids->at(i)));
    }

    gridWidget->setMaximumHeight(ceil(vids->size() / columnCount) * 500);
    gridWidget->setMaximumWidth(ceil(window->width()));

    for(int i=0; i < columnCount; i++){
        gridLayout->setColumnMinimumWidth(i, 200);
        gridLayout->setColumnStretch(i, 1);
    }

    for(int i=0; i < ceil(buttons->size()/columnCount); i++){
        gridLayout->setRowMinimumHeight(i, 200);
        gridLayout->setRowStretch(i, 0);
    }
    return buttons;
}

// called when searching or sorting to re-render the grid with a newly-inputted vector of videos
void renderGrid(vector<TheButtonInfo>* vids, ThePlayer* player, QWidget* buttonWidget,
                QGridLayout* gridLayout, QWidget* gridWidget, QWidget* window, int columnCount){

    // delete existing buttons
    QLayoutItem * item;
    while ( ( item = gridWidget->layout()->takeAt( 0 ) ) != NULL )
    {
        delete item->widget();
    }


    int* row_count = new int();
    *row_count = 0;

    // loop over ALL videos to display them in a list
    for ( int i = 0; i < vids->size(); i++ ) {
        TheButton* button = renderButton(i, vids->at(i), player,
                                         buttonWidget,gridLayout, gridWidget, columnCount);
        button->init(&(vids->at(i)));
    }

}

// search through vector of videos using search string
vector<TheButtonInfo>* searchVideos(vector<TheButtonInfo>* the_buttons, QString search_string){

    vector<TheButtonInfo>* search_results = new vector<TheButtonInfo>();
    int length_of_search = search_string.length();
    //access metadata
    //iterate through videos
    for (TheButtonInfo i: *the_buttons){
        //check the filename
        if (search_string == (i.data.getFilename()).left(length_of_search)){
            //add the button to the vector list
            search_results->push_back(i);
        }

    }
    return search_results;
}

void createColorSchemeMenu(QMenu * colorSchemeMenu, Language * actLang, QAction* lightModeAction,
                           QAction *darkModeAction, QAction*highContrastModeAction, QToolBar * tb,
                           ColourScheme * activeColour, QLabel * bgImage, QPixmap bgImagePixDark,
                           QPixmap bgImagePixLight, QApplication * app){
    colorSchemeMenu->addAction(lightModeAction);
    colorSchemeMenu->addAction(darkModeAction);
    colorSchemeMenu->addAction(highContrastModeAction);

    tb->addAction(colorSchemeMenu->menuAction());

    colorSchemeMenu->connect(colorSchemeMenu,&QMenu::triggered, [=](QAction* action) mutable{
        if(action->text() == actLang->dark_mode){
            activeColour->setDarkMode(app);
            colorSchemeMenu->setTitle(actLang->dark_mode);
            bgImage->setPixmap(bgImagePixDark);


        }
        else if(action->text() == actLang->high_contrast_mode){
            activeColour->setHighContrastMode(app);
            colorSchemeMenu->setTitle(actLang->high_contrast_mode);
            bgImage->setPixmap(bgImagePixDark);

        }
        else{
            activeColour->setLightMode(app);
            colorSchemeMenu->setTitle(actLang->light_mode);
            bgImage->setPixmap(bgImagePixLight);
        }
    });
}

void createLanguageMenu(QMenu * languageMenu){

    QAction * english = new QAction("🇬🇧 English");
    QAction * spanish = new QAction("🇪🇸 Español");
    QAction * french = new QAction("🇫🇷 Française");
    QAction * german = new QAction("🇩🇪 Deutsch");
    QAction * turkish = new QAction("🇹🇷 Türk");
    QAction * dutch = new QAction("🇳🇱 Nederlands");
    QAction * russian = new QAction("🇷🇺 Русский");


    languageMenu->addAction(english);
    languageMenu->addAction(spanish);
    languageMenu->addAction(french);
    languageMenu->addAction(german);
    languageMenu->addAction(turkish);
    languageMenu->addAction(dutch);
    languageMenu->addAction(russian);
}

ButtonVector* getInfoIn (string loc) {

    ButtonVector *out = new ButtonVector();
    QDir dir(QString::fromStdString(loc));
    QDirIterator it(dir);



    int length = 0;
    while (it.hasNext()) { // for all files
        QString f = it.next();

            if (f.contains("."))

#if defined(_WIN32)
            if (f.contains(".wmv"))  { // windows
#else
            if (f.contains(".mp4") || f.contains("MOV"))  { // mac/linux
#endif
                // convert the file location to a generic url
                QUrl *url = new QUrl(QUrl::fromLocalFile( f ));
                length++;
                MediaLoader *loader = new MediaLoader(url, out);
                    loader->setMedia(*url);
                    out->addLoader(loader);

            }
    }
    out->setExpectedLength(length);
    return out;
}

int main(int argc, char *argv[]) {

    // initialise language to english
    Language * activeLanguage = new Language();
    activeLanguage->triggerEnglish();

    // create the Qt Application
    QApplication * app = new QApplication(argc, argv);
    app->setWindowIcon(QIcon(QFileInfo("../comp2811_cw3/tomeoicon.ico").absoluteFilePath()));

    // colour scheme initialised to light
    ColourScheme * activeColour = new ColourScheme(app);

    // collect all the videos in the folder
    ButtonVector * videos;

    QWidget* gridWidget = new QWidget();

    // main layout (containing video player and toolbar) is top
    QVBoxLayout *top = new QVBoxLayout();
    // layout for expanded view showing all videos
    ExpandedLayout *expandedLayout = new ExpandedLayout(gridWidget);
    // layout for playing intro video
    QVBoxLayout *welcomeLayout = new QVBoxLayout();
    // window to contain all layouts
    TheWindow *window = new TheWindow(top, expandedLayout, welcomeLayout);

    // get videos using argument
    if (argc == 2)
        videos = getInfoIn( string(argv[1]) );
    if (videos->size() == 0) {
        if(videos->getExpectedLength() == 0){
            const int result = QMessageBox::question(
                        NULL,
                        QString("Tomeo"),
                        QString("no videos found! download, unzip, and add command line "
                                "argument to \"quoted\" file location. Download videos from "
                                "Tom's OneDrive?"),
                        QMessageBox::Yes |
                        QMessageBox::No );

            switch( result )
            {
            case QMessageBox::Yes:
              QDesktopServices::openUrl(QUrl("https://leeds365-my.sharepoint.com/:u:/g/personal"
                                             "/scstke_leeds_ac_uk/EcGntcL-K3JOiaZF4T_uaA4BHn6USbq"
                                             "2E55kF_BTfdpPag?e=n1qfuN"));
                break;
            default:
                break;
            }
            exit(-1);
        }
        else{
            // play intro video on boot
            QMediaPlayer * introPlayer = new QMediaPlayer();
            QVideoWidget * videoWid = new QVideoWidget();
            welcomeLayout->addWidget(videoWid);
            welcomeLayout->setMargin(0);
            introPlayer->setVideoOutput(videoWid);

            QString introVideoPath;

            // choose appropriate file extension
#if defined(_WIN32)
            introVideoPath = QFileInfo("../comp2811_cw3/intro.wmv").absoluteFilePath(); // windows
#else
            // mac / linux
            introVideoPath = QFileInfo("../comp2811_cw3/intro.mp4").absoluteFilePath();
#endif
            introPlayer->setMedia(QUrl::fromLocalFile(introVideoPath));

            introPlayer->play();

            // once video has finished playing, videos will have loaded so program can begin
            introPlayer->connect(introPlayer, &QMediaPlayer::mediaStatusChanged, [=](){
                if(introPlayer->mediaStatus() == QMediaPlayer::EndOfMedia){
                    window->closeWelcome();
                }
            });
        }
    }

    // once videos are loaded, window can be shown
    window->connect(videos, &ButtonVector::completed, window, &TheWindow::show);

    // containers for video
    QWidget * videoAndMetadataWidget = new QWidget();
    QHBoxLayout * videoMetadataLayout = new QHBoxLayout();
    videoAndMetadataWidget->setLayout(videoMetadataLayout);

    QWidget *videoWrapper = new QWidget();
    QStackedLayout *videoLayout = new QStackedLayout();
    videoLayout->setStackingMode(QStackedLayout::StackAll);

    videoWrapper->setLayout(videoLayout);

    QVideoWidget *videoWidget = new QVideoWidget();
    QLabel * bgImage = new QLabel();
    bgImage->setAlignment(Qt::AlignCenter);

    QPushButton *metadataLabel = new QPushButton();
    metadataLabel->setText("fill this in");
    metadataLabel->setVisible(false);

    videoMetadataLayout->addWidget(videoWrapper);
    videoMetadataLayout->addWidget(metadataLabel);

    // get images for background when no video playing
    QPixmap bgImagePixLight(QFileInfo("../comp2811_cw3/logo.png").absoluteFilePath());
    QPixmap bgImagePixDark(QFileInfo("../comp2811_cw3/logo_dark.png").absoluteFilePath());
    bgImage->setPixmap(bgImagePixLight);

    QWidget *mediaOverlay = new QWidget();

    QVBoxLayout *mediaOverlayLayout = new QVBoxLayout();
    mediaOverlay->setLayout(mediaOverlayLayout);

    // toolbar for menu options
    QToolBar * tb = new QToolBar();

    // create menus
    QMenu * language_menu = new QMenu(activeLanguage->language);
    createLanguageMenu(language_menu);

    tb->addAction(language_menu->menuAction());

    QMenu * colorSchemeMenu = new QMenu(activeLanguage->light_mode);
    QAction * lightModeAction = new QAction(activeLanguage->light_mode);
    QAction * darkModeAction = new QAction(activeLanguage->dark_mode);
    QAction * highContrastModeAction = new QAction(activeLanguage->high_contrast_mode);

    createColorSchemeMenu(colorSchemeMenu, activeLanguage, lightModeAction, darkModeAction,
                          highContrastModeAction, tb, activeColour, bgImage, bgImagePixDark,
                          bgImagePixLight, app);


    QMenu * shareMenu = new QMenu(activeLanguage->share);
    QAction * youtubeAction = new QAction("YouTube");
    QAction * instagramAction = new QAction("Instagram");
    QAction * facebookAction = new QAction("Facebook");

    shareMenu->addAction(youtubeAction);
    shareMenu->addAction(instagramAction);
    shareMenu->addAction(facebookAction);

    shareMenu->connect(shareMenu, &QMenu::triggered, [=](QAction * action) mutable{
        if(action->text() == "YouTube"){
            QDesktopServices::openUrl(QUrl("https://www.youtube.com/upload"));
        }
        else if(action->text() == "Instagram"){
            QDesktopServices::openUrl(QUrl("https://www.instagram.com/"));
        }
        else if(action->text() == "Facebook"){
            QDesktopServices::openUrl(QUrl("https://www.facebook.com/"));
        }
    });

    // share and import buttons
    QToolButton *importButton = new QToolButton();
    importButton->setText(activeLanguage->import);
    importButton->connect(importButton, &QPushButton::released, [=](){
        QString fileToCopy = QFileDialog::getOpenFileName();
    });

    QToolButton *helpButton = new QToolButton();
    helpButton->setText(activeLanguage->help);

    QMessageBox * helpBox = new QMessageBox();
    helpBox->setText(activeLanguage->helpMessage);
    tb->addWidget(helpButton);

    helpButton->connect(helpButton, &QPushButton::released, [=](){
        helpBox->show();
    });

    QMenu * metadataMenu = new QMenu(activeLanguage->metadata);
    metadataMenu->setStyleSheet("QMenu::item:selected {background-color : transparent;}");

    QAction * videoTitle = new QAction("N/A");
    QAction * videoDuration = new QAction("N/A");
    QAction * videoFilesize = new QAction("N/A");
    QAction * videoDate = new QAction("N/A");

    metadataMenu->addAction(videoTitle);
    metadataMenu->addAction(videoDuration);
    metadataMenu->addAction(videoFilesize);
    metadataMenu->addAction(videoDate);

    // the QMediaPlayer which controls the playback
    ThePlayer *player = new ThePlayer;
    player->setVideoOutput(videoWidget);

    // connect to metadata drop down
    player->connect(player, &QMediaPlayer::stateChanged, [=]() mutable{
        TheButtonInfo * current_video = player->getCurrentlyPlaying();
        if(current_video != NULL){
            videoTitle->setText(current_video->data.getFilename());
            videoDuration->setText(intToStringTime(current_video->data.getDuration()));
            videoFilesize->setText(filesizeToString(current_video->data.getFilesize()));
            videoDate->setText(current_video->data.getCreationTime().toString());

        }
    });

    // set video widget height / width to scale keeping to the 16:9 ratio
    videoWidget->setGeometry(videoWidget->x(), videoWidget->y(),
                             videoWidget->width(), videoWidget->width() / 16 * 9);

    // define media controls widget/layout
    QWidget *mediaControls = new QWidget();
    mediaControls->setGeometry(videoWidget->x()+videoWidget->width()/2,
                               videoWidget->y(),
                               videoWidget->width(), videoWidget->width() / 16 * 9);

    QHBoxLayout *mediaControlLayouts = new QHBoxLayout();
    mediaControls->setLayout(mediaControlLayouts);

    // set maximum size of buttons (so they don't grow)
    mediaControls->setMaximumHeight(50);

    // define play button
    QPushButton *playButton = new QPushButton();
    playButton->setStyleSheet("border-radius : 6px; padding : 6px");
    QLabel * volumeLabel = new QLabel("Volume");
    // define volume slider horizontal width
    QSlider *volumeSlider = new QSlider(Qt::Horizontal);

    // set volume slider controls with default value
    volumeSlider->setTickPosition(QSlider::TicksBothSides);
    volumeSlider->setTickInterval(10);
    volumeSlider->setSingleStep(1);
    volumeSlider->setValue(50);

    QSlider *progressSlider = new QSlider(Qt::Horizontal);
    progressSlider->connect(progressSlider, &QSlider::sliderMoved, player, &ThePlayer::setPosition);
    player->connect(player, &ThePlayer::durationChanged, progressSlider, &QSlider::setMaximum);
    player->connect(player, &ThePlayer::positionChanged, progressSlider, &QSlider::setValue);

    // duration label and progress slider
    QLabel *durationLabel = new QLabel("00:00:00");
    player->connect(player, &ThePlayer::positionChanged, durationLabel, [=](int position){
        durationLabel->setText(intToStringTime(position));
    });

    // connect buttons using signals/slots
    playButton->connect(playButton, &QPushButton::released, player, [=](){
        if(player->state() == QMediaPlayer::State::PlayingState){
            playButton->setText(activeLanguage->play);
            player->pause();
        }
        else{
            playButton->setText(activeLanguage->pause);
            player->play();
        }
    });

    // if the video is paused and a new video is loaded, ensure the button reflects the new state
    player->connect(player, &QMediaPlayer::currentMediaChanged, playButton, [=](){
        playButton->setText(activeLanguage->pause);
    });

    // if the video finishes, set the button to pause mode
    player->connect(player, &QMediaPlayer::mediaStatusChanged, playButton, [=](){
        if(player->mediaStatus() == QMediaPlayer::EndOfMedia){
            playButton->setText(activeLanguage->play);
        }
    });

    // connect volume slider to change volume function
    volumeSlider->connect(volumeSlider, &QSlider::valueChanged, player, &ThePlayer::changeVolume);

    // VIDEO PLAYBACK SPEED
    QComboBox * speedBox = new QComboBox();
    speedBox->addItem("0.5x", QVariant(0.5));
    speedBox->addItem("1.0x", QVariant(1.0));
    speedBox->addItem("1.5x", QVariant(1.5));
    speedBox->addItem("2.0x", QVariant(2.0));
    speedBox->setCurrentIndex(1);

    QObject::connect(speedBox, QOverload<int>::of(&QComboBox::activated), player,
                     &ThePlayer::updateSpeed);
    QObject::connect(player, &ThePlayer::changeRate, player, &ThePlayer::setPlaybackRate);

    // add play button and progress slider to horizontal media controls layout
    mediaControlLayouts->addWidget(playButton);
    mediaControlLayouts->addWidget(progressSlider);
    mediaControlLayouts->addWidget(durationLabel);
    mediaControlLayouts->addWidget(speedBox);
    mediaControlLayouts->addWidget(volumeLabel);
    mediaControlLayouts->addWidget(volumeSlider);
    mediaControlLayouts->setAlignment(Qt::AlignBottom);

    videoLayout->addWidget(videoWidget);
    videoLayout->addWidget(bgImage);
    videoLayout->setCurrentWidget(bgImage);
    videoLayout->setAlignment(videoWidget, Qt::AlignCenter);

    // add actions to toolbar
    tb->addAction(shareMenu->menuAction());
    tb->addWidget(importButton);
    tb->addAction(metadataMenu->menuAction());

    // layout + widget for all widgets at bottom of screen
    QWidget * bottomMainLayoutWidget = new QWidget();
    QHBoxLayout * bottomMainLayout = new QHBoxLayout();
    bottomMainLayoutWidget->setLayout(bottomMainLayout);
    bottomMainLayout->setContentsMargins(10, 0, 10, 0);

    // layout for search button and videos (but not expand push button)
    QWidget * searchButtonsWidget = new QWidget();
    QVBoxLayout * searchAndButtonsLayout = new QVBoxLayout();
    searchButtonsWidget->setLayout(searchAndButtonsLayout);

    // videos arranged horizontally in a layout
    QHBoxLayout *displayedVideoLayout = new QHBoxLayout();
    displayedVideoLayout->setMargin(0);

    // buttonWidget used to contain video layout
    QWidget *buttonWidget = new QWidget();
    buttonWidget->setLayout(displayedVideoLayout);
    buttonWidget->setMaximumHeight(145);

    // create vector to contain buttons (i.e. video thumbnails) at bottom of main view
    vector<TheButton*> videosAtBottom;
    for(int i=0 ; i < 3; i++){
        // generate thumbnail buttons
        TheButton *button = new TheButton(buttonWidget);
        // when clicked, close the expanded view and tell the player to play.
        button->connect(button, &TheButton::jumpTo, player, &ThePlayer::jumpTo);
        displayedVideoLayout->addWidget(button);
        videosAtBottom.push_back(button);
    }
    // label for if no videos are found in search bar
    QLabel * noVideosFound = new QLabel(activeLanguage->no_videos);
    noVideosFound->setStyleSheet("padding : 50px 0px 50px 0px");
    displayedVideoLayout->addWidget(noVideosFound);
    noVideosFound->setVisible(false);


    // search bar
    QLineEdit * mainSearch = new QLineEdit();
    mainSearch->setPlaceholderText(activeLanguage->search);

    // connect search bar and get results, as well as redisplay them
    mainSearch->connect(mainSearch, &QLineEdit::textChanged, [=](QString query){
        vector<TheButtonInfo>* results = searchVideos(videos->getVideos(), query);

        int attribute = window->getSortType();
        int asc = window->getAscType();

        // sort the search results
        sortByMetadata(results, attribute, asc);

        if(results->size() != 0){
            noVideosFound->setVisible(false);
            // update button properties based upon returned video values
            for(int i = 0; i < 3; i++){
                if(i < results->size()){
                    videosAtBottom.at(i)->setVisible(true);
                    videosAtBottom.at(i)->init(&(results->at(i)));
                }
                if(i >= results->size()){
                    videosAtBottom.at(i)->setVisible(false);
                }
            }
        }
        else{
            for(int i = 0; i < 3; i++){
                videosAtBottom.at(i)->setVisible(false);
            }
            noVideosFound->setVisible(true);
        }


    });

    // search bar and video widget bundled into appropriate layout
    searchAndButtonsLayout->addWidget(mainSearch);
    searchAndButtonsLayout->addWidget(buttonWidget);

    // create expand view button
    QPushButton *expandView = new QPushButton(buttonWidget);
    //expandView->setSpacing(0);
    expandView->setMaximumHeight(145);

    // expand button added to main layout
    bottomMainLayout->addWidget(searchButtonsWidget);
    bottomMainLayout->addWidget(expandView);

    // when the video plays, make sure the expand window is closed
    player->connect(player, &ThePlayer::onVideoPlay, window, &TheWindow::closeExpanded);
    player->connect(player, &ThePlayer::onVideoPlay, videoLayout, [=](){
        videoLayout->setCurrentWidget(videoWidget);
    });
    // connect signals for 'show more' button
    // when clicked, open the expanded view.
    expandView->connect(expandView, &QPushButton::released, window, &TheWindow::openExpanded);
    // when clicked, pause the videos.
    expandView->connect(expandView, &QPushButton::released, player, &ThePlayer::pressPause);

    // add media control layouts to centre align
    top->addWidget(videoAndMetadataWidget, 1);
    top->addWidget(mediaControls);
    top->addWidget(bottomMainLayoutWidget, 0);
    top->setMenuBar(tb);
    top->setMargin(0);


    // create expanded scroll area
    QScrollArea* scrollArea = new QScrollArea(window);
    scrollArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    scrollArea->setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);

    // create expanded grid layout
    QGridLayout *grid = new QGridLayout();
    //expandedLayout->setGrid(gridWidget);

    // define geometry for scroll area
    scrollArea->setMinimumWidth(window->width());

    //configure the grid layout
    grid->setVerticalSpacing(0);

    // set scroll area widget / layout
    scrollArea->setWidget(gridWidget);
    gridWidget->setLayout(grid);

    // create a back button to the previous screen
    QPushButton *backButton = new QPushButton();
    backButton->connect(backButton, &QPushButton::released, window, &TheWindow::closeExpanded);

    // create a search button
    QPushButton *searchButton = new QPushButton();
    searchButton->setText(activeLanguage->search);


    //create a search box
    QLineEdit *textBox = new QLineEdit();
    textBox->setPlaceholderText(activeLanguage->search);
    // connection to search when search text changed
    textBox->connect(textBox, &QLineEdit::textChanged, [=](QString query){
        vector<TheButtonInfo>* results = searchVideos(videos->getVideos(), query);

        int attribute = window->getSortType();
        int asc = window->getAscType();

        sortByMetadata(results, attribute, asc);

        // rerender results
        renderGrid(results, player, buttonWidget, grid, gridWidget, window,
                   window->getColumnCount());
    });

    // for spacing back and search buttons at top of layout
    QSpacerItem * spacerBackSearch = new QSpacerItem(10, 5);
    QSpacerItem * spacerSearchSort = new QSpacerItem(10, 5);


    // create a sort button
    QPushButton *sortButton = new QPushButton();
    sortButton->setText(activeLanguage->sort);
    sortButton->connect(sortButton, &QPushButton::released, [=](){

        vector<TheButtonInfo>* results = searchVideos(videos->getVideos(), textBox->text());

        int attribute = window->getSortType();
        int asc = window->getAscType();

        sortByMetadata(results, attribute, asc);

        renderGrid(results, player, buttonWidget, grid, gridWidget, window,
                   window->getColumnCount());

    });

    // set render grid layout
    expandedLayout->setGridFunc([=](){
        if(videos->getVideos()->size() >= videos->getExpectedLength()){
            vector<TheButtonInfo>* results = searchVideos(videos->getVideos(), textBox->text());

            int attribute = window->getSortType();
            int asc = window->getAscType();

            sortByMetadata(results, attribute, asc);

            renderGrid(results, player, buttonWidget, grid, gridWidget, window,
                       window->getColumnCount());
        }
    });

    //Make a combo box
    QComboBox* sortAttributeCombo = new QComboBox();
    sortAttributeCombo->setStyleSheet("width : 80px;");
    sortAttributeCombo->addItem(activeLanguage->duration);
    sortAttributeCombo->addItem(activeLanguage->filesize);
    sortAttributeCombo->addItem(activeLanguage->date);
    sortAttributeCombo->setCurrentIndex(0);
    sortAttributeCombo->connect(sortAttributeCombo, QOverload<int>::of(&QComboBox::activated),
                                window, &TheWindow::setSortType);

    QComboBox* sortByCombo = new QComboBox();
    sortByCombo->setStyleSheet("width : 110px;");

    sortByCombo->addItem(activeLanguage->ascending);
    sortByCombo->addItem(activeLanguage->descending);
    sortByCombo->setCurrentIndex(0);
    sortByCombo->connect(sortByCombo, QOverload<int>::of(&QComboBox::activated), window,
                         &TheWindow::setAscType);

    // contain widgets at top of expanded view (e.g. back/search/sort)
    QHBoxLayout *menu_layout = new QHBoxLayout();
    QWidget* menu_widget = new QWidget();


    menu_widget->setLayout(menu_layout);

    menu_layout->setSpacing(5);

    // add widgets to expanded layout
    menu_layout->addWidget(backButton, 0, Qt::AlignLeft);
    menu_layout->addSpacerItem(spacerBackSearch);
    menu_layout->addWidget(textBox, 1);
    menu_layout->addSpacerItem(spacerSearchSort);
    menu_layout->addWidget(sortAttributeCombo, 0, Qt::AlignRight);
    menu_layout->addWidget(sortByCombo, 0, Qt::AlignRight);
    menu_layout->addWidget(sortButton, 0, Qt::AlignRight);

    expandedLayout->addWidget(menu_widget);
    expandedLayout->addWidget(scrollArea);
    expandedLayout->setMargin(0);


    // connect all objects with text to language menu
    language_menu->connect(language_menu,&QMenu::triggered, [=](QAction* action){
        if(action->text() == activeLanguage->english){
            activeLanguage->triggerEnglish();
        }
        else if(action->text() == activeLanguage->spanish){
            activeLanguage->triggerSpanish();
        }
        else if(action->text() == activeLanguage->russian){
            activeLanguage->triggerRussian();
        }
        else if(action->text() == activeLanguage->german){
            activeLanguage->triggerGerman();
        }
        else if(action->text() == activeLanguage->french){
            activeLanguage->triggerFrench();
        }
        else if(action->text() == activeLanguage->turkish){
            activeLanguage->triggerTurkish();
        }
        else if(action->text() == activeLanguage->dutch){
            activeLanguage->triggerDutch();
        }
        // reset text of all widgets upon language change
        playButton->setText(activeLanguage->play);
        shareMenu->setTitle(activeLanguage->share);
        language_menu->setTitle(activeLanguage->language);
        expandView->setText(activeLanguage->show_more);
        backButton->setText(activeLanguage->back);
        sortButton->setText(activeLanguage->sort);
        sortAttributeCombo->setItemText(0, activeLanguage->duration);
        sortAttributeCombo->setItemText(1, activeLanguage->filesize);
        sortAttributeCombo->setItemText(2, activeLanguage->date);
        sortByCombo->setItemText(0, activeLanguage->ascending);
        sortByCombo->setItemText(1, activeLanguage->descending);
        helpBox->setText(activeLanguage->helpMessage);
        helpButton->setText(activeLanguage->help);
        textBox->setPlaceholderText(activeLanguage->search);
        mainSearch->setPlaceholderText(activeLanguage->search);
        noVideosFound->setText(activeLanguage->no_videos);
        volumeLabel->setText(activeLanguage->volume);
        if(activeColour->getCurrentColourScheme() == "light"){
            colorSchemeMenu->setTitle(activeLanguage->light_mode);
        }
        else if(activeColour->getCurrentColourScheme() == "dark"){
            colorSchemeMenu->setTitle(activeLanguage->dark_mode);
        }
        else{
            colorSchemeMenu->setTitle(activeLanguage->high_contrast_mode);
        }
        lightModeAction->setText(activeLanguage->light_mode);
        highContrastModeAction->setText(activeLanguage->high_contrast_mode);
        darkModeAction->setText(activeLanguage->dark_mode);
        importButton->setText(activeLanguage->import);
    });

    // initialise text of widgets
    playButton->setText(activeLanguage->play);
    language_menu->setTitle(activeLanguage->language);
    expandView->setText(activeLanguage->show_more);
    helpButton->setText(activeLanguage->help);
    backButton->setText(activeLanguage->back);
    searchButton->setText(activeLanguage->search);
    sortButton->setText(activeLanguage->sort);
    sortAttributeCombo->setItemText(0, activeLanguage->duration);
    sortAttributeCombo->setItemText(1, activeLanguage->filesize);
    sortAttributeCombo->setItemText(2, activeLanguage->date);
    sortByCombo->setItemText(0, activeLanguage->ascending);
    sortByCombo->setItemText(1, activeLanguage->descending);

    // define shortcuts as appropriate
    QShortcut * spaceBar = new QShortcut(QKeySequence(Qt::Key_Space), window);
    QShortcut::connect(spaceBar, &QShortcut::activated, player, [=](){
        if(player->state() == QMediaPlayer::State::PlayingState){
            playButton->setText(activeLanguage->play);
            player->pause();
        }
        else{
            playButton->setText(activeLanguage->pause);
            player->play();
        }
    });

    // initialise video buttons using the imported metadata
    window->connect(videos, &ButtonVector::completed, [window, grid, gridWidget, player,
                    buttonWidget, videosAtBottom, expandView, bottomMainLayout, activeLanguage]
                    (vector<TheButtonInfo>* vids){
        for(int i = 0; i < 3; i++){
            videosAtBottom.at(i)->init(&(vids->at(i)));
       }

        vector<TheButton*>* buttons = renderGridInit(vids, player, buttonWidget, grid,
                                                     gridWidget, window, window->getColumnCount());

        // create expand view button
        expandView->setMaximumHeight(145);
        expandView->setText(activeLanguage->show_more);
        bottomMainLayout->addWidget(expandView);
        player->setContent(buttons, vids);
    });

    // define more shortcuts
    QShortcut * f11 = new QShortcut(QKeySequence(Qt::Key_F11), window);
    QShortcut::connect(f11, &QShortcut::activated, window, &TheWindow::showFullScreen);

    QShortcut * esc = new QShortcut(QKeySequence(Qt::Key_Escape), window);
    QShortcut::connect(esc, &QShortcut::activated, window, &TheWindow::showNormal);

    QShortcut * m = new QShortcut(QKeySequence(Qt::Key_M), window);
    QShortcut::connect(m, &QShortcut::activated, player, &ThePlayer::muteMedia);

    QShortcut * rightArrow = new QShortcut(QKeySequence(Qt::Key_Right), window);
    QShortcut::connect(rightArrow, &QShortcut::activated, [=](){
        if(player->getCurrentlyPlaying() != NULL){
            player->moveVideoOnRight();
        }
    });

    QShortcut * leftArrow = new QShortcut(QKeySequence(Qt::Key_Left), window);
    QShortcut::connect(leftArrow, &QShortcut::activated, [=](){
        if(player->getCurrentlyPlaying() != NULL){
            player->moveVideoOnLeft();
        }
    });

    // set window title / size
    window->setWindowTitle("Tomeo");
    window->setMinimumSize(800, 680);

    // wait for the app to terminate
    return app->exec();
}
