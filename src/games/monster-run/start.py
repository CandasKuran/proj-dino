import pygame
import sys
import globals
from mainChar import charger_personnage as charger_personnage1
from char2 import charger_personnage as charger_personnage2
from char3 import charger_personnage as charger_personnage3


# Fonction pour afficher une fenêtre de sélection de personnage au centre de l'écran
def afficher_fenetre_selection(parent_ecran):
    global selected_character, player_name  # On utilise les variables globales
    
    # Dimensions de la petite fenêtre
    LARGEUR_FENETRE, HAUTEUR_FENETRE = 600, 400
    NOIR = (0, 0, 0)
    BLANC = (255, 255, 255)
    ROUGE = (255, 0, 0)
    GRIS = (192, 192, 192)

    # Charger les animations pour trois personnages différents
    frames1 = charger_personnage1()  # Animations du premier personnage
    frames2 = charger_personnage2()  # Animations du deuxième personnage
    frames3 = charger_personnage3()  # Animations du troisième personnage

    # Variables pour l'animation de chaque personnage
    index_frame1, index_frame2, index_frame3 = 0, 0, 0
    horloge = pygame.time.Clock()
    intervalle_animation = 100  # Intervalle entre les frames (en millisecondes)

    # Variable pour suivre la sélection du personnage
    selectionne = None  # Aucun personnage sélectionné au début
   

    # Centrer la petite fenêtre dans l'écran parent
    fenetre_rect = pygame.Rect(parent_ecran.get_width() // 2 - LARGEUR_FENETRE // 2,
                               parent_ecran.get_height() // 2 - HAUTEUR_FENETRE // 2,
                               LARGEUR_FENETRE, HAUTEUR_FENETRE)

    police = pygame.font.SysFont("arial", 30)

    # Position des boutons
    bouton_quitter = pygame.Rect(fenetre_rect.x + 100, fenetre_rect.y + 300, 180, 60)
    bouton_continuer = pygame.Rect(fenetre_rect.x + 320, fenetre_rect.y + 300, 180, 60)

    # Variables pour les champs de texte
    input_box = pygame.Rect(fenetre_rect.x + 150, fenetre_rect.y + 250, 300, 40)
    couleur_active = ROUGE
    couleur_inactive = GRIS
    couleur_courante = couleur_inactive
    actif = False
    texte_entre = ''

    # Variables pour les boîtes des personnages
    personnage_rects = [
        pygame.Rect(fenetre_rect.x + 100, fenetre_rect.y + 100, 100, 100),
        pygame.Rect(fenetre_rect.x + 250, fenetre_rect.y + 100, 100, 100),
        pygame.Rect(fenetre_rect.x + 400, fenetre_rect.y + 100, 100, 100)
    ]

    while True:
        # Remplir l'écran parent (fond)
        parent_ecran.fill((26, 28, 27))

        # Afficher la petite fenêtre
        pygame.draw.rect(parent_ecran, BLANC, fenetre_rect)

        # Gérer l'animation des personnages (changer les frames)
        index_frame1 = (index_frame1 + 1) % len(frames1)
        index_frame2 = (index_frame2 + 1) % len(frames2)
        index_frame3 = (index_frame3 + 1) % len(frames3)

        # Dessiner les personnages avec la sélection
        for i, rect in enumerate(personnage_rects):
            # Dessiner une bordure rouge si le personnage est sélectionné
            if selectionne == i:
                pygame.draw.rect(parent_ecran, ROUGE, rect, 5)
            else:
                pygame.draw.rect(parent_ecran, GRIS, rect, 5)

        # Afficher les personnages et ajuster leur taille
        for i, rect in enumerate([frames1[index_frame1], frames2[index_frame2], frames3[index_frame3]]):
            personnage = pygame.transform.scale(rect, (80, 80))  # Redimensionner les personnages
            parent_ecran.blit(personnage, (personnage_rects[i].x + 10, personnage_rects[i].y + 10))

        # Afficher et ajuster la position de la boîte de texte
        input_box.y = fenetre_rect.y + 220  # Boîte de texte un peu plus bas
        pygame.draw.rect(parent_ecran, couleur_courante, input_box, 2)
        txt_surface = police.render(texte_entre, True, NOIR)
        input_box.w = max(300, txt_surface.get_width() + 20)
        parent_ecran.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        # Afficher les boutons
        pygame.draw.rect(parent_ecran, GRIS, bouton_quitter, border_radius=10)
        quitter_texte = police.render("Quitter", True, NOIR)
        parent_ecran.blit(quitter_texte, (bouton_quitter.x + 40, bouton_quitter.y + 10))

        pygame.draw.rect(parent_ecran, GRIS, bouton_continuer, border_radius=10)
        continuer_texte = police.render("Continuer", True, NOIR)
        parent_ecran.blit(continuer_texte, (bouton_continuer.x + 30, bouton_continuer.y + 10))

        # Gérer les événements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                # Si on clique sur le champ de texte
                if input_box.collidepoint(evenement.pos):
                    actif = not actif
                else:
                    actif = False
                couleur_courante = couleur_active if actif else couleur_inactive

                # Gérer les clics sur les personnages
                for i, rect in enumerate(personnage_rects):
                    if rect.collidepoint(evenement.pos):
                        selectionne = i  # Mettre à jour la sélection

                # Gérer les clics sur les boutons
                if bouton_quitter.collidepoint(evenement.pos):
                    return  # Fermer la fenêtre sans sauvegarder
                
                if bouton_continuer.collidepoint(evenement.pos):
                    selected_character = selectionne  # Sauvegarder le personnage sélectionné
                    player_name = texte_entre  # Sauvegarder le nom entré
                    return  # Fermer la fenêtre et retourner à l'écran principal


            if evenement.type == pygame.KEYDOWN:
                if actif:
                    if evenement.key == pygame.K_RETURN:
                        print(texte_entre)  # Simuler la soumission du texte
                    elif evenement.key == pygame.K_BACKSPACE:
                        texte_entre = texte_entre[:-1]
                    else:
                        texte_entre += evenement.unicode

        # Mettre à jour la fenêtre principale avec la petite fenêtre au centre
        pygame.display.flip()
        horloge.tick(10)  # Contrôler la vitesse de l'animation

# Fonction pour afficher l'écran de démarrage
def afficher_ecran_demarrage():
    from game import game_loop 
    from game import afficher_message
    pygame.init()

    # Dimensions de l'écran
    LARGEUR, HAUTEUR = 1200, 800
    NOIR_FONCE = (26, 28, 27)
    NOIR = (0, 0, 0)
    ROUGE = (255, 0, 0)
    GRIS = (192, 192, 192)
    BLEU_CLAIR = (173, 216, 230)

    # Fenêtre de jeu
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Écran de démarrage")

    police_titre = pygame.font.SysFont("comicsansms", 100)
    police_bouton = pygame.font.SysFont("arial", 50)

    # Fonction pour dessiner des boutons avec du texte
    def dessiner_bouton(texte, couleur, rect, couleur_texte):
        pygame.draw.rect(ecran, couleur, rect, border_radius=10)
        texte_surface = police_bouton.render(texte, True, couleur_texte)
        texte_rect = texte_surface.get_rect(center=rect.center)
        ecran.blit(texte_surface, texte_rect)

    # Fonction pour vérifier si la souris survole un bouton
    def souris_survol_bouton(rect):
        pos_souris = pygame.mouse.get_pos()
        return rect.collidepoint(pos_souris)

    # Boucle principale pour afficher l'écran de démarrage
    while True:
        ecran.fill(NOIR_FONCE)

        # Afficher le titre "Monster-Run" au centre de l'écran
        titre = police_titre.render("Monster-Run", True, NOIR)
        ecran.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 100))

        # Création des boutons "Démarrer", "Quitter" et "Sélection de personnage"
        bouton_demarrer = pygame.Rect(LARGEUR // 2 - 200, HAUTEUR // 2, 180, 60)
        bouton_quitter = pygame.Rect(LARGEUR // 2 + 50, HAUTEUR // 2, 180, 60)

        # Ajuster la taille du bouton selon la taille du texte "Sélection Personnage"
        texte_selection = "Sélection Personnage"
        largeur_bouton_selection = police_bouton.size(texte_selection)[0] + 40
        bouton_selection = pygame.Rect(LARGEUR // 2 - largeur_bouton_selection // 2, HAUTEUR // 2 + 100, largeur_bouton_selection, 60)

        # Vérifier si la souris survole les boutons
        couleur_demarrer = BLEU_CLAIR if souris_survol_bouton(bouton_demarrer) else GRIS
        couleur_quitter = BLEU_CLAIR if souris_survol_bouton(bouton_quitter) else GRIS
        couleur_selection = BLEU_CLAIR if souris_survol_bouton(bouton_selection) else GRIS

        # Dessiner les boutons avec une bordure
        dessiner_bouton("Démarrer", couleur_demarrer, bouton_demarrer, NOIR)
        dessiner_bouton("Quitter", couleur_quitter, bouton_quitter, NOIR)
        dessiner_bouton(texte_selection, couleur_selection, bouton_selection, NOIR)

        # Gérer les événements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_demarrer.collidepoint(evenement.pos):
                    from game import game_loop
                    game_loop()
                if bouton_quitter.collidepoint(evenement.pos):
                    pygame.quit()
                    sys.exit()
                if bouton_selection.collidepoint(evenement.pos):
                    afficher_fenetre_selection(ecran)  # Afficher l'écran de sélection du personnage
                if player_name:
                    actif_texte = f"Joueur Actif: {player_name}"
                    police_actif = pygame.font.SysFont("arial", 30)
                    ecran.blit(police_actif.render(actif_texte, True, NOIR), (10, 10))
        pygame.display.flip()

# Appeler la fonction d'affichage de l'écran de démarrage avant le début du jeu
if __name__ == "__main__":
    afficher_ecran_demarrage()
