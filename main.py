###########################
## Youtube Mp3 Converter ##
##  by Alexander Müller  ##
###########################
version = '0.9-RC1'

#imports
from configparser import ConfigParser
import PySimpleGUIQt as sg
import yt_dlp
import threading
from pathlib import Path
import re

#read config from settings.ini
settings_path = str(Path.home())+'\\AppData\\Local\\Youtube Mp3 Converter\settings.ini'                
config_object = ConfigParser()
config_object.read(settings_path)
settings = config_object['SETTINGS']
language = settings['language']
theme = settings['theme']
sg.theme(theme)

#gets the users music directory and assigns it to a string variable
default_dir = str(Path.home())+'\\Music\\'


#PySimpleGUIQt window initial layout 
layout = [[sg.Menu([
            ['Theme', ['Default', 'Dark', 'YT']],
            ['Language',['English', 'German', 'Italian']],
            ['Quality',['320kbit', '256kbit', '192kbit', '128kbit', '92kbit', '64kbit']],
            ])],
        
        [sg.Text()],            
        
        [sg.Text(size=(20,1)), 
        sg.InputText(size=(70,1),key='INPUT_URL'),
        sg.Checkbox('keepvid', key='KEEPVIDEO', size=(10,1))],
        
        [sg.FolderBrowse(initial_folder=default_dir,size=(30,1),target=('-FOLDER-')), 
        sg.InputText(default_dir, size=(70,1),key='-FOLDER-')],            
        
        [sg.Button(size=(50,1)), 
        sg.Button(size=(50,1))],
                    
        [sg.ProgressBar(max_value=10, orientation='h', size=(None, 20), key='PROGRESS',visible=False)],
        
        [sg.Text(size=(100,2), key='OUTPUT', visible=False)]        
        ]

#creates window object
window = sg.Window('YoutubeMp3Converter '+version, layout)

#initializes global variables
folder = ''
dl_qual = '320'


##################
#GUI Localization#
##################

#Textfield, Button, Checkbox texts
english_text1 = 'Enter a URL or search term and klick on "Download" to download a Song.\nSupports all sites that youtube_dl supports.'
english_text2 = 'Enter URL/search term here:'
english_text3 = 'Keep Video'
english_text4 = 'Select Folder'
english_text5 = 'Download'
english_text6 = 'Exit'

german_text1 = 'Gib eine URL oder einen Suchbegríff ein und klicke auf "Herunterladen" um ein Lied herunterzuladen.\nUnterstützt alle Seiten die von youtube_dl unterstützt werden.'
german_text2 = 'Gib hier die URL/den Suchbegriff ein:'
german_text3 = 'Video speichern'
german_text4 = 'Ordner auswählen'
german_text5 = 'Herunterladen'
german_text6 = 'Verlassen'

italian_text1 = 'Immettere un URL o un termine di ricerca e cliccare su "Download" per scaricare una canzone.\nSupporta tutti i siti che youtube_dl supporta.'
italian_text2 = 'Inserisci qui l\'URL/termine di ricerca:'
italian_text3 = 'Mantieni video'
italian_text4 = 'Seleziona la cartella'
italian_text5 = 'Scaricare'
italian_text6 = 'Uscita'

        
###############        
###FUNCTIONS###
###############        
def language_text(language, postion):   
    '''returns status text in selected language and position'''
    if language == 'english':
        
        if postion == 0: #§ = title, $ = percentage, & = eta            
            return str(f'Downloading: § \n$ \ntime remaining: &')
        if postion == 1:
            return 'Converting...'
        if postion == 2: #§ = location
             return str(f'Done!\nSaved to: §\nIf you like this App, consider donating to paypal.me/aTTaX420. Thank you for using my App!')
        if postion == 3:
            return 'Please enter a URL or search term!'
        if postion == 4:
            return 'Looking up Songs, please wait...'
       
    if language == 'german':
        if postion == 0: #§ = title, $ = percentage, & = eta  
            return str(f'Lade herunter: § \n$ \nVerbleibende Zeit: &')
        if postion == 1:
            return 'Konvertieren...'
        if postion == 2: #§ = location
            return str(f'Fertig!\nGespeichert in: §\nWenn dir die App gefällt, kannst du gerne spenden an: paypal.me/aTTaX420. Vielen Dank, dass du meine App benutzt!')
        if postion == 3:
            return 'Bitte eine URL oder einen Suchbegriff eingeben!'            
        if postion == 4:
            return 'Suche nach Liedern, bitte warten...'
    
    if language == 'italian':
        if postion == 0: #§ = title, $ = percentage, & = eta  
            return str(f'Download: § \n$ \ntempo rimanente: &')
        if postion == 1:
            return 'Conversione...'
        if postion == 2: #§ = location
            return str(f'Fatto!\nSalvato in: §\nSe ti piace questa applicazione, considera di fare una donazione a paypal.me/aTTaX420. Grazie per aver usato la mia App!\nTraduzione in italiano a cura di: GioJoe89')
        if postion == 3:
            return 'Inserire un URL o un termine di ricerca!'            
        if postion == 4:
            return 'Ricerca di canzoni, attendere prego...'


def reopen_window():
    '''this function is needed to change language on GUI elements and to change the theme
    it contains a layout for every language and reopens the window with the selected theme and language'''
    
    global window    
    window.close()
    
    if language == 'english':
        layout = [
            [sg.Menu([['Theme', ['Default', 'Dark', 'YT']], 
                      ['Language', ['English', 'German', 'Italian']], 
                      ['Quality', ['320kbit/s', '256kbit/s', '192kbit/s', '128kbit/s', '92kbit/s', '64kbit/s']]
                      ])],
            
            [sg.Text(english_text1)],            
            
            [sg.Text(english_text2,size=(20,1)), 
            sg.InputText(size=(70,1),key='INPUT_URL'),
            sg.Checkbox( text= english_text3, key='KEEPVIDEO', size=(10,1))],
            
            [sg.FolderBrowse(button_text=english_text4,initial_folder=default_dir,size=(30,1),target=('-FOLDER-')), 
            sg.InputText(default_dir, size=(70,1),key='-FOLDER-')],            
            
            [sg.Button(english_text5, size=(50,1)), 
            sg.Button(english_text6,size=(50,1))],
                        
            [sg.ProgressBar(max_value=10, orientation='h', size=(None, 20), key='PROGRESS',visible=False)],
            
            [sg.Text(size=(100,2), key='OUTPUT', visible=False)]        
            ]
        
    if language == 'german':
        layout = [
            [sg.Menu([['Erscheinungsbild', ['Standard', 'Dunkel', 'YT']], 
                      ['Sprache', ['Englisch', 'Deutsch', 'Italienisch']], 
                      ['Qualität', ['320kbit/s', '256kbit/s', '192kbit/s', '128kbit/s', '92kbit/s', '64kbit/s']]
                      ])],
            
            [sg.Text(german_text1)],            
            
            [sg.Text(german_text2,size=(25,1)), 
            sg.InputText(size=(70,1),key='INPUT_URL'),
            sg.Checkbox( text= german_text3, key='KEEPVIDEO', size=(15,1))],
                        
            [sg.FolderBrowse(button_text=german_text4,initial_folder=default_dir,size=(30,1),target=('-FOLDER-')), 
            sg.InputText(default_dir, size=(70,1),key='-FOLDER-')], 
                       
            [sg.Button(german_text5, size=(50,1)), 
            sg.Button(german_text6,size=(50,1))],            
            
            [sg.ProgressBar(max_value=10, orientation='h', size=(None, 20), key='PROGRESS',visible=False)],
            
            [sg.Text(size=(100,2), key='OUTPUT', visible=False)]        
            ]
    
    if language == 'italian':
        layout = [
            [sg.Menu([['Tema', ['Standard', 'Scura', 'YT']], 
                      ['Lingua', ['Inglese', 'Tedesco', 'Italiano']], 
                      ['Qualità', ['320kbit/s', '256kbit/s', '192kbit/s', '128kbit/s', '92kbit/s', '64kbit/s']]
                      ])],
            
            [sg.Text(italian_text1)],            
            
            [sg.Text(italian_text2,size=(25,1)), 
            sg.InputText(size=(70,1),key='INPUT_URL'),
            sg.Checkbox( text= italian_text3, key='KEEPVIDEO', size=(15,1))],
                        
            [sg.FolderBrowse(button_text=italian_text4,initial_folder=default_dir,size=(30,1),target=('-FOLDER-')), 
            sg.InputText(default_dir, size=(70,1),key='-FOLDER-')], 
                       
            [sg.Button(italian_text5, size=(50,1)), 
            sg.Button(italian_text6,size=(50,1))],            
            
            [sg.ProgressBar(max_value=10, orientation='h', size=(None, 20), key='PROGRESS',visible=False)],
            
            [sg.Text(size=(100,2), key='OUTPUT', visible=False)]        
            ]
            
    window = sg.Window('YoutubeMp3Converter '+version, layout)


def my_hook(d):
    '''hook to get status updates form yt_dlp lib'''
    
    global window
    global language
        
 
    def update_status():        
        '''updates OUTPUT textfield with download information(name, percentage, eta) while yt_slp lib is downloading
        NEEDS TO RUN IN A SEPERATE THREAD OR GUI WILL FREEZE!!!!'''
        
        global title               
        
        #removes ANSI color codes from yt_dlp status strings and assigns variables
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        title = ansi_escape.sub('',d['filename'])
        percentage = ansi_escape.sub('', d['_percent_str'])
        eta = ansi_escape.sub('',d['_eta_str'])

        #LANGPOS 0 Download Status
        message = language_text(language, 0)        
        message = message.replace('§', title)
        message = message.replace('$', percentage)
        message = message.replace('&', eta)

        #updates OUTPUT textfield                     
        window['OUTPUT'].update(value=message)


    if d['status'] == 'downloading': 
        #updates progress bar, creates a thread object for the update_status function and runs it to prevent GUI freezing.
        window['PROGRESS'].update_bar(3)
        t2 = threading.Thread(target=update_status, daemon=True)
        t2.start()

    if d['status'] == 'finished':
        #updates progress bar and OUTPUT textfield when done downloading
        window['PROGRESS'].update_bar(7)
        
        #LANGPOS 1 Converting message
        message = language_text(language, 1)
        window['OUTPUT'].update(value=message)
        

def download(url, window):
    '''proesses search term or link, then downloads the video, extracts audio and converts it to mp3
    NEEDS TO RUN IN A SEPERATE THREAD OR GUI WILL FREEZE!!!!'''

    global folder    
    global values, event   
    global language
    
    #yt_dlp options
    keepvideo = values['KEEPVIDEO']
    ydl_opts = {
    "outtmpl": folder,
    "noplaylist": False,
    "default_search": "auto",
    'format' : 'bestaudio',
    'postprocessors' : [{
        'key' : 'FFmpegExtractAudio',
        'preferredcodec' : 'mp3',
        'preferredquality' : dl_qual}],
    'prefer_ffmpeg' : True,
    'keepvideo' : keepvideo,
    'progress_hooks': [my_hook]
    }
    
    if url != '':
        window['PROGRESS'].update_bar(2)
        
        #creates an instance of YoutubeDL as ydl
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        #runs the download function ydl object
        ydl.download(url)

        #updates progress bar and OUTPUT textfield when done converting.
        location = values['-FOLDER-']
        
        #LANGPOS 2 Saved to message
        message = language_text(language, 2)
        message = message.replace('§', location)

        window['PROGRESS'].update_bar(10)
        window['PROGRESS'].update(visible = False)
        
    else:
        #LANGPOS 3 Enter URL message
        message = language_text(language, 3)
        window['PROGRESS'].update_bar(0)
        
    window['OUTPUT'].update(value=message)   
    
    
def run():
    '''Main loop'''
        
    global window
    global folder
    global event, values
    global language
    global dl_qual
        
    reopen_window()
    while True:
        #get events and values from window        
        event, values = window.read()
        url = []

        
        ####################
        ###EVENT HANDLERS###
        ####################
        if event == '320kbit/s':
            dl_qual = '320'            
        if event == '256kbit/s':
            dl_qual = '256'            
        if event == '192kbit/s':
            dl_qual = '192'            
        if event == '128kbit/s':
            dl_qual = '128'            
        if event == '92kbit/s':
            dl_qual = '92' 
        if event == '64kbit/s':
            dl_qual = '64' 
        
        ###THEMES###    
        if event == 'Default' or event == 'Standard':
            sg.theme('Default1')
            settings['theme'] = 'Default1'
            with open(settings_path, 'w') as conf:
                config_object.write(conf)
            reopen_window()
            
        if event == 'Dark' or event == 'Dunkel':
            sg.theme('DarkAmber')
            settings['theme'] = 'DarkAmber'
            with open(settings_path, 'w') as conf:
                config_object.write(conf)
            reopen_window()
            
        if event == 'YT':
            sg.theme('DarkRed1')
            settings['theme'] = 'DarkRed1'
            with open(settings_path, 'w') as conf:
                config_object.write(conf)
            reopen_window()
            
        ####EXIT###
        if event == sg.WINDOW_CLOSED or event == 'Exit' or event == 'Verlassen':
            break
                
        ###LANGUAGE###
        if event == 'Englisch' or event== 'Inglese':
            language = 'english'
            settings['language'] = 'english'
            with open(settings_path, 'w') as conf:
                config_object.write(conf)
            reopen_window()            
        
        if event == 'German' or event == 'Tedesco':
            language = 'german'
            settings['language'] = 'german'
            with open(settings_path, 'w') as conf:
                config_object.write(conf)
            reopen_window()
        
        if event == 'Italian' or event == 'Italienisch':
            language = 'italian'
            settings['language'] = 'italian'
            with open(settings_path, 'w') as conf:
                config_object.write(conf)
            reopen_window()
        
        
        ###DOWNLOAD###
        if event == 'Download' or event == 'Herunterladen':
            window['OUTPUT'].update(visible = True)
            window['PROGRESS'].update(visible = True)
            folder = values['-FOLDER-']  
            folder = folder+'/'          

            if folder != None:
                folder = str(f'{folder}%(title)s.%(ext)s')

            if folder == '':
                folder = '%(title)s.%(ext)s'
            
            else:
                #LANGPOS 4 Looking up songs message
                message = language_text(language, 4)
                
            window['OUTPUT'].update(value=message)         

            #assigns link/search term entered into the first textfield to the url list on index 0
            url.insert(0, str(window['INPUT_URL'].get()))

            #neccessary to update OUTPUT textfield
            url.insert(1, window)

            #creates a thread object for the download function and runs it to prevent GUI freezing.
            t1 = threading.Thread(target=download,args=url, daemon=True)
            t1.start()

            window.Refresh()

    #exits program when mainloop is stopped
    window.close()
    

if __name__ == '__main__':
    #creates main thread object and runs it
    t_main = threading.Thread(target=run)
    t_main.start()
    
