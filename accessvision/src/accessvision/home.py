import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from accessvision import yolo


class BienvenueApp(toga.App):

    def startup(self):
        # Créer une fenêtre principale
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Chemin de l'image de fond
        background_image_path = "assets/fond.png"
        background_image = toga.Image(background_image_path)
        self.view = toga.ImageView(background_image)

        # Créer une boîte pour contenir l'image de fond
        self.background_box = toga.Box(
            style=Pack(flex=1, direction=COLUMN, alignment=CENTER, width=300, height=900),
            children=[],
        )

        # Ajouter la vue de l'image de fond à la boîte de fond
        self.background_box.add(self.view)

        # Définir le contenu de la fenêtre principale
        self.main_window.content = self.background_box

        # Afficher l'écran d'accueil
        self.show_welcome_screen()

        # Afficher la fenêtre principale
        self.main_window.show()

    def show_welcome_screen(self):
        self.clear_background_box()
        self.background_box.add(self.view)

        # Créer une boîte pour contenir les widgets "BIENVENUE" et "COMMENCER"
        content_box = toga.Box(
            style=Pack(direction=COLUMN, alignment=CENTER, padding_top=-600),
            children=[]
        )

        # Créer un label "BIENVENUE"
        bienvenue_label = toga.Label(
            'BIENVENUE',
            style=Pack(text_align=CENTER,
                       font_size=40,
                       color='#000000',
                       font_family='Arial',  # Assurez-vous que cette police est disponible
                       font_weight='bold')
        )

        # Créer un bouton "COMMENCER"
        commencer_button = toga.Button(
            'COMMENCER',
            on_press=self.on_commencer_press,
            style=Pack(padding_top=100,
                       padding_bottom=20,
                       width=200,
                       height=50,
                       background_color='#e8f2fd',  # Couleur personnalisée
                       color='black',  # Couleur du texte
                       font_family='Arial',  # Assurez-vous que cette police est disponible
                       font_weight='bold'
                       )
        )

        # Ajouter le label et le bouton à la boîte de contenu
        content_box.add(bienvenue_label)
        content_box.add(commencer_button)

        # Mettre à jour la boîte de fond avec la nouvelle boîte de contenu
        self.background_box.add(content_box)

    def clear_background_box(self):
        # Supprimer tous les enfants sauf l'image de fond
        for child in self.background_box.children[:]:
            self.background_box.remove(child)

    def show_detection_screen(self):
        # Effacer les éléments existants
        self.clear_background_box()

        # Créer une boîte pour contenir les widgets "En cours de détection..." et "STOP"
        content_box = toga.Box(
            style=Pack(direction=COLUMN, alignment=CENTER, height=900),
            children=[]
        )
        content_box.style.background_color = '#e8f2fd'

        # Créer un label "En cours de détection..."
        detection_label = toga.Label(
            'En cours de détection...',
            style=Pack(text_align=CENTER,
                       font_size=40,
                       color='#000000',
                       font_family='Arial',  # Assurez-vous que cette police est disponible
                       font_weight='bold',
                       padding_top=200)
        )

        # Créer un bouton "STOP"
        stop_button = toga.Button(
            'STOP',
            on_press=self.on_stop_press,
            style=Pack(padding_top=100,
                       padding_bottom=20,
                       width=200,
                       height=50,
                       background_color='#e8f2fd',  # Couleur personnalisée
                       color='black',  # Couleur du texte
                       font_family='Arial',  # Assurez-vous que cette police est disponible
                       font_weight='bold'
                       )
        )

        # Ajouter le label et le bouton à la boîte de contenu
        content_box.add(detection_label)
        content_box.add(stop_button)

        # Mettre à jour la boîte de fond avec la nouvelle boîte de contenu
        self.background_box.add(content_box)

    def on_commencer_press(self, widget):
        print("Le bouton 'COMMENCER' a été pressé!")
        self.show_detection_screen()
        try:
            yolo.start_yolo_thread()
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_stop_press(self, widget):
        self.show_welcome_screen()
        try:
            yolo.on_stop_press()
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    return BienvenueApp('Bienvenue', 'com.example.bienvenue')


