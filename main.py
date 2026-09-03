import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import yt_dlp
import threading
import os

PLAYLIST_FILE = "playlist_hp.txt"

class WinampHpWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(WinampHpWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 20
        self.playlist_urls = []
        
        # 1. Tampilan Layar Digital Utama Neon Hijau
        self.display_label = Label(
            text="*** WINAMP MOBILE v1.0 ***",
            font_size='18sp',
            size_hint_y=None,
            height=50,
            color=(0, 1, 0, 1)
        )
        self.add_widget(self.display_label)
        
        # 2. Kotak Input Tautan YouTube
        self.url_input = TextInput(
            text="https://youtu.be",
            multiline=False,
            size_hint_y=None,
            height=50,
            background_color=(0.15, 0.15, 0.18, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.add_widget(self.url_input)
        
        # 3. Tombol Tambah ke Antrean Playlist
        btn_add = Button(
            text="+ ADD TO PLAYLIST",
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.2, 0.25, 1),
            color=(0, 1, 0, 1)
        )
        btn_add.bind(on_press=self.add_to_playlist)
        self.add_widget(btn_add)
        
        # 4. Panel Tombol Kontrol Musik Utama
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=5)
        
        btn_play = Button(text="PLAY", color=(0, 1, 0, 1), background_color=(0.2, 0.2, 0.2, 1))
        btn_play.bind(on_press=self.play_music)
        control_layout.add_widget(btn_play)
        
        btn_pause = Button(text="PAUSE", color=(1, 1, 0, 1), background_color=(0.2, 0.2, 0.2, 1))
        control_layout.add_widget(btn_pause)
        
        btn_stop = Button(text="STOP", color=(1, 0, 0, 1), background_color=(0.2, 0.2, 0.2, 1))
        control_layout.add_widget(btn_stop)
        
        self.add_widget(control_layout)
        
        # 5. Informasi Status Kuantitas Lagu
        self.status_label = Label(
            text="Status: Siap",
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(self.status_label)
        
        self.load_saved_playlist()

    def add_to_playlist(self, instance):
        url = self.url_input.text.strip()
        if url:
            self.display_label.text = "LOADING AUDIO LINK..."
            threading.Thread(target=self.fetch_audio_link, args=(url,), daemon=True).start()
            self.url_input.text = ""

    def fetch_audio_link(self, url):
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Audio YouTube')
                self.playlist_urls.append(url)
                self.save_playlist_to_file()
                
                self.display_label.text = f"ADDED: {title[:25].upper()}"
                self.status_label.text = f"Total lagu di antrean: {len(self.playlist_urls)}"
        except Exception:
            self.display_label.text = "GAGAL MEMBACA LINK!"

    def play_music(self, instance):
        if self.playlist_urls:
            self.display_label.text = "MEMUTAR MUSIK..."
            self.status_label.text = "Mencoba memutar audio stream..."
        else:
            self.display_label.text = "PLAYLIST MASIH KOSONG!"

    def save_playlist_to_file(self):
        with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
            for url in self.playlist_urls:
                f.write(f"{url}\n")

    def load_saved_playlist(self):
        if os.path.exists(PLAYLIST_FILE):
            with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        self.playlist_urls.append(line.strip())
            if self.playlist_urls:
                self.status_label.text = f"Memuat {len(self.playlist_urls)} lagu tersimpan."

class WinampMobileApp(App):
    def build(self):
        self.title = "WINAMP YT - MOBILE"
        return WinampHpWidget()

if __name__ == '__main__':
    WinampMobileApp().run()
