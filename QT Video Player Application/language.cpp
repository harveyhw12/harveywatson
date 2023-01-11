#include "language.h"

Language::Language(){
    // default to english
    triggerEnglish();
}

// sets the members of language object to appropriate language text
void Language::triggerEnglish(){
    language = "🇬🇧 English";
    help = "Help";
    fullscreen = "Fullscreen";
    no_videos = "No videos found.";
    exit_fullscreen = "Exit Fullscreen";
    colour_scheme = "Colour scheme";
    dark_mode = "Dark Mode";
    volume = "Volume";
    light_mode = "Light Mode";
    high_contrast_mode = "High Contrast Mode";
    helpMessage = "Fullscreen: F11\n"
                  "Exit Fullscreen: Esc\n"
                  "Mute: M\n"
                  "Play/Pause Video: Spacebar\n"
                  "Left Arrow: Previous Video\n"
                  "Right Arrow: Next Video\n";
    import = "Import";
    play = "Play";
    pause = "Pause";
    back = "Back";
    share = "Share";
    search = "Search";
    sort = "Sort";
    ascending = "Ascending";
    descending = "Descending";
    show_more = "Show More";
    date = "Date";
    duration = "Duration";
    filename = "Filename";
    filesize = "File size";
    tags = "Tags";
    metadata = "Metadata";
}


void Language::triggerRussian(){
    language = "🇷🇺 Русский";
    colour_scheme = "цветовая схема";
    dark_mode = "Темный режим";
    light_mode = "Легкий режим";
    volume = "Громкость";
    high_contrast_mode = "Режим высокой контрастности";
    help = "Помогите";
    no_videos = " Видео не найдено.";
    helpMessage = "полноэкранный: F11\n"
                  "выйти из полноэкранного режима: Esc\n"
                  "немой: M\n"
                  "переключить воспроизведение / паузу: пробел\n"
                  "стрелка влево: предыдущее видео\n"
                  "стрелка вправо: следующее видео\n";
    import = "Импортировать";
    play = "Смотреть";
    pause = "Пауза";
    back = "Назад";
    share = "Поделиться";
    search = "Поиск";
    sort = "Сортировать";
    ascending = "Восходящий";
    descending = "Нисходящий";
    show_more = "Показать Больше";
    date = "Дата";
    duration = "Длина";
    filename = "Имя Файла";
    filesize = "Размер Файла";
    tags = "Теги";
    metadata = "метаданные";
}

void Language::triggerGerman(){
    language = "🇩🇪 Deutsch";
    colour_scheme = "Farbschema";
    dark_mode = "Dunkler Modus";
    light_mode = "Lichtmodus";
    no_videos = "Keine Videos gefunden.";
    volume = "Lautstärke";
    high_contrast_mode = "Kontrastreicher Modus";
    import = "Importieren";
    help = "Hilfe";
    helpMessage = "Vollbild: F11\n"
                  "Vollbild beenden: Esc\n"
                  "Stummschalten: M\n"
                  "Wiedergabe/Pause Umschalten: Leertaste\n"
                  "Pfeil nach links: vorheriges Video\n"
                  "Pfeil nach rechts: nächstes Video\n";
    play = "Wiedergabe";
    pause = "Pause";
    back = "Zurück";
    share = "Teilen";
    search = "Suchen";
    sort = "Sortieren";
    ascending = "Aufsteigend";
    descending = "Absteigend";
    show_more = "Mehr Ansehen";
    date = "Datum";
    duration = "Lange";
    filename = "Dateiname";
    filesize = "Datengröße";
    tags = "Schlagwörter";
    metadata = "Metadaten";
}

void Language::triggerFrench(){
    language = "🇫🇷 Française";
    colour_scheme = "Jeu de couleurs";
    light_mode = "Mode Lumière";
    dark_mode = "Mode Sombre";
    high_contrast_mode = "Mode contraste élevé";
    help = "Aide";
    volume = "Volume";
    no_videos = "Aucune vidéo trouvée.";
    helpMessage = "Plein écran: F11\n"
                  "Quitter le Plein écran: Esc\n"
                  "Couper le Son: M\n"
                  "Basculer Lecture / Pause: Barre d'espace\n"
                  "flèche gauche: vidéo précédente\n"
                  "flèche droite: vidéo suivante\n";
    import = "Importer";
    play = "Lire";
    pause = "Pause";
    back = "Retour";
    share = "Partager";
    search = "Suchen";
    sort = "Rechercher";
    ascending = "Ascendante";
    descending = "Desscendante";
    show_more = "Plus";
    date = "Date";
    duration = "Durée";
    filename = "Nom du fichier";
    filesize = "Taille du fichier";
    tags = "Étiquette";
    metadata = "Métadonnées";
}

void Language::triggerSpanish(){
    language = "🇪🇸 Español";
    metadata = "metadatos";
    colour_scheme = "Esquema de color";
    dark_mode = "Modo oscuro";
    light_mode = "Modo de luz";
    no_videos = "No se encontraron vídeos.";
    volume = "Volumen";
    high_contrast_mode = "Modo de alto contraste";
    help = "Ayuda";
    helpMessage = "Pantalla Completa: F11\n"
                  "Salir de Pantalla Complete: Esc\n"
                  "Silencioso: M\n"
                  "Alternar Reproduccion/Pausa: Barra Espaciadora\n"
                  "flecha izquierda: video anterior\n"
                  "flecha derecha: siguiente video\n";
    import = "Importar";
    play = "Botón de reproducción";
    pause = "Pausa";
    back = "Regresa";
    share = "Compartir";
    search = "Buscar";
    sort = "Ordenar";
    ascending = "Ascendente";
    descending = "Descendente";
    show_more = "Más";
    date = "Fecha";
    duration = "Duración";
    filename = "El nombre de archivo";
    filesize = "Tamaño del archivo";
    tags = "Etiquetas";
}

void Language::triggerTurkish(){
    language = "🇹🇷 Türk";
    metadata = "meta veriler";
    colour_scheme = "Renk şeması";
    light_mode = "Işık Modu";
    dark_mode = "Karanlık Mod";
    volume = "Ses";
    no_videos = "Video bulunamadı.";
    high_contrast_mode = "Yüksek Kontrast Modu";
    help = "yardım";
    helpMessage = "tam ekran: F11\n"
                  "tam ekrandan çık: Esc\n"
                  "sesi kapat: M\n"
                  "oynat / duraklat değiştir: boşluk çubuğu\n"
                  "sol ok: önceki video\n"
                  "sağ ok: sonraki video\n";
    import = "İthalat";
    play = "Oynat";
    pause = "Duraklat";
    back = "Dönü";
    share = "Paylaş";
    search = "Suchen";
    sort = "Ayırmak";
    ascending = "Yükselen";
    descending = "Azalan";
    show_more = "Daha Fazla Göster";
    date = "Tarih";
    duration = "Süre";
    filename = "Dosya adı";
    filesize = "Dosya boyutu";
    tags = "Etiket";
}

void Language::triggerDutch(){
    language = "🇳🇱 Nederlands";
    metadata = "metadata";
    colour_scheme = "Kleuren schema";
    dark_mode = "Donkere Modus";
    light_mode = "Lichte modus";
    no_videos = "Geen video's gevonden.";
    volume = "Volume";
    high_contrast_mode = "Modus met hoog contrast";
    help = "Help";
    helpMessage = "Volledig Scherm: F11\n"
                  "Volledig Scherm afsluiten: Esc\n"
                  "Dempen: M\n"
                  "Schakelen Tussen Afspelen / Pauzeren: Spatiebalk\n"
                  "pijl naar links: vorige video\n"
                  "pijl naar rechts: volgende video\n";
    import = "Importeren";
    play = "Afspelen";
    pause = "Pauzeren";
    back = "Terug";
    share = "Delen";
    search = "Zoeken";
    sort = "Sorteren";
    ascending = "Oplopende";
    descending = "Aflopende";
    show_more = "Meer Weergeven";
    date = "Datum";
    duration = "Duur";
    filename = "Bestandsnaam";
    filesize = "Bestandsgrootte";
    tags = "Labels";
}

void Language::setLang(QString lang){
    if(lang == spanish){
        triggerSpanish();
    }
    else if(lang == german){
        triggerGerman();
    }
    else if(lang == dutch){
        triggerDutch();
    }
    else if(lang == russian){
        triggerRussian();
    }
    else if(lang == turkish){
        triggerTurkish();
    }
    else{
        // default to english if error signal received
        triggerEnglish();
    }
}
