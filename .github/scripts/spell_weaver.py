import itertools
import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from typing import List, Dict, Tuple


# ==========================================
# 1. LE MOTEUR LOGIQUE (ENCODAGE UBS)
# ==========================================
class SpellEncoder:
    """Générateur d'encodage binaire asymétrique pour la notation magique (UBS)."""

    def __init__(self, n_vertices: int):
        self.n = n_vertices
        print(f"[*] Initialisation de l'encodeur pour n={self.n}...")
        self.unique_binaries = self._generate_unique_binaries()
        print(f"[*] {len(self.unique_binaries)} séquences cycliquement uniques générées.")
        self.feature_maps = {}

    def _generate_unique_binaries(self) -> List[List[int]]:
        """Génère les séquences UBS avec filtrage esthétique et mélange."""
        all_combinations = list(itertools.product([0, 1], repeat=self.n))
        unique_sets = set()
        result = []

        for bits in all_combinations:
            # --- 1. FILTRAGE DE DENSITÉ ---
            # On compte le nombre de "1" dans la séquence (le nombre de lignes)
            nb_lignes = sum(bits)

            # On rejette les séquences trop vides (< 3 lignes)
            # ou trop pleines (plus de n-3 lignes) pour garder un rendu aéré
            if nb_lignes < 3 or nb_lignes > self.n - 3:
                continue
            # ------------------------------

            t_bits = tuple(bits)
            if t_bits not in unique_sets:
                result.append(list(bits))
                # Bloquer les rotations
                for i in range(self.n):
                    rotated = tuple(list(bits)[i:] + list(bits)[:i])
                    unique_sets.add(rotated)

        # --- 2. CHAOS DÉTERMINISTE ---
        # On fixe une "graine" mathématique. Ainsi, random.shuffle mélangera
        # toujours la liste exactement de la même manière à chaque exécution.
        # "Fireball" aura toujours la même tête demain ou dans 10 ans.
        # -----------------------------

        return result

    def register_attribute(self, k_step: int, features: List[str]):
        """Associe une liste de caractéristiques à un pas k avec un mélange unique."""
        if len(features) > len(self.unique_binaries):
            raise ValueError(f"Pas assez de séquences uniques pour k={k_step}.")

        sorted_features = sorted(list(set(features)))
        attribute_map = {}

        # --- LE CORRECTIF : Un mélange unique pour chaque k_step ---
        import random
        # On copie la liste globale pour ne pas l'altérer
        shuffled_binaries = self.unique_binaries.copy()

        # On utilise une graine mathématique basée sur 'k_step'
        # Ainsi, la liste pour k=1 sera mélangée différemment de k=2, etc.
        # Mais le résultat restera éternellement le même pour chaque sort !
        random.seed(42 + k_step)
        random.shuffle(shuffled_binaries)
        # -----------------------------------------------------------

        for i, feature in enumerate(sorted_features):
            attribute_map[feature] = shuffled_binaries[i]

        self.feature_maps[k_step] = attribute_map

    def encode_spell(self, spell_data: Dict[int, str]) -> Dict[int, List[int]]:
        """Convertit les données textuelles d'un sort en séquences binaires."""
        encoded = {}
        for k_step, feature_value in spell_data.items():
            if k_step not in self.feature_maps:
                raise KeyError(f"L'attribut k={k_step} n'est pas enregistré.")
            if feature_value not in self.feature_maps[k_step]:
                raise ValueError(f"La caractéristique '{feature_value}' est inconnue pour k={k_step}.")
            encoded[k_step] = self.feature_maps[k_step][feature_value]
        return encoded


# ==========================================
# 2. LE MOTEUR GRAPHIQUE (RENDU MATPLOTLIB)
# ==========================================
class SpellWeaver:
    """Moteur de rendu graphique pour tracer les sorts."""

    def __init__(self, n_vertices: int, radius: float = 10.0, distortion: float = 0.0, grid_type: str = 'circle'):
        self.n = n_vertices
        self.radius = radius
        self.points = self._generate_anchors(grid_type, distortion)

    def _generate_anchors(self, grid_type: str, distortion: float) -> List[Tuple[float, float]]:
        """Génère les points d'ancrage selon le modèle mathématique choisi."""
        points = []

        if grid_type == 'circle':
            # Cercle classique / Polygone régulier
            angles = np.linspace(np.pi / 2, -3 * np.pi / 2, self.n, endpoint=False)
            for angle in angles:
                x = self.radius * np.cos(angle)
                y = self.radius * np.sin(angle)
                points.append((x, y))

        elif grid_type == 'semi_circle':
            # Demi-cercle (comme l'exemple "Acid Splash" du document)
            angles = np.linspace(np.pi, 0, self.n)
            for angle in angles:
                x = self.radius * np.cos(angle)
                y = self.radius * np.sin(angle)
                points.append((x, y))

        elif grid_type == 'quadratic':
            # Fonction quadratique y = ax^2 + c (comme l'exemple "Scorching Ray")
            # On répartit les points sur l'axe X
            xs = np.linspace(-self.radius, self.radius, self.n)
            for x in xs:
                # Parabole inversée (en forme de V ou de U)
                a = 0.8 / self.radius
                y = a * (x ** 2) - (self.radius / 2)
                points.append((x, y))

        elif grid_type == 'linear':
            # Une simple ligne droite inclinée
            xs = np.linspace(-self.radius, self.radius, self.n)
            for x in xs:
                y = 0.5 * x
                points.append((x, y))
        elif grid_type == 'exponential':
            # Courbe de croissance y = e^x
            # On utilise np.linspace avec un léger décalage pour éviter que les
            # points de gauche ne soient trop écrasés les uns sur les autres.
            xs = np.linspace(-self.radius, self.radius * 0.8, self.n)

            for x in xs:
                # On divise x par (radius / 3) pour adoucir la pente de l'exponentielle
                # et on soustrait (radius / 2) pour recentrer le graphique sur l'axe Y
                y = np.exp(x / (self.radius / 3)) - (self.radius / 2)
                points.append((x, y))
        elif grid_type == 'logarithmic':
            # Courbe logarithmique y = ln(x)
            # On génère nos x de manière classique
            xs = np.linspace(-self.radius, self.radius, self.n)

            for x in xs:
                # On ajoute (radius + 1) à x pour s'assurer que le paramètre du log
                # est toujours strictement supérieur à 0, même quand x = -radius.
                valeur_positive = x + self.radius + 1

                # On multiplie par un facteur (radius / 3) pour que la courbe prenne
                # un peu de hauteur, et on soustrait pour recentrer le dessin.
                y = (self.radius / 3) * np.log(valeur_positive) - (self.radius / 2)
                points.append((x, y))
        elif grid_type == 'spiral':
            # Spirale Logarithmique (La solution cosmique)

            # Nombre de rotations de la spirale (1.0 = 1 tour complet)
            # 1.5 ou 2.0 donne d'excellents résultats pour n=15
            rotations = 1.5
            theta_max = rotations * 2 * np.pi

            # On répartit les angles de 0 à theta_max
            thetas = np.linspace(0, theta_max, self.n)

            # Formule mathématique : r = a * e^(k * theta)
            # 'a' est le rayon initial (on le met à 15% du rayon max pour ne pas écraser les 1ers points au centre)
            a = self.radius * 0.15

            # 'k' calcule la vitesse d'expansion pour atteindre exactement self.radius à la fin
            k = np.log(self.radius / a) / theta_max

            for theta in thetas:
                r = a * np.exp(k * theta)
                # Conversion des coordonnées polaires (r, theta) en cartésiennes (x, y)
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                points.append((x, y))

        else:
            raise ValueError(f"Type de grille '{grid_type}' inconnu.")

        # Application de la distorsion organique
        if distortion > 0.0:
            distorted_points = []
            for x, y in points:
                dx = x + np.random.uniform(-distortion, distortion)
                dy = y + np.random.uniform(-distortion, distortion)
                distorted_points.append((dx, dy))
            return distorted_points

        return points

    def _draw_arc(self, ax, p1: Tuple[float, float], p2: Tuple[float, float],
                  color: str, curvature: float, lw: float):
        """Trace une courbe de Bézier quadratique avec un décalage orthogonal."""
        mid_x, mid_y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

        # Calcul du vecteur entre les deux points
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        # Le point de contrôle est décalé selon le vecteur normal (-dy, dx)
        # La valeur de 'curvature' définit l'intensité de ce décalage
        ctrl_x = mid_x - dy * curvature
        ctrl_y = mid_y + dx * curvature

        path = Path([p1, (ctrl_x, ctrl_y), p2], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
        patch = patches.PathPatch(path, facecolor='none', edgecolor=color, lw=lw, alpha=0.7)
        ax.add_patch(patch)

    def scribe_spell(self, binary_features: Dict[int, List[int]], style_config: Dict[int, Dict] = None,
                     show_nodes: bool = True, transparency: bool = False):
        """Trace le sort final avec option de transparence et cadrage forcé."""

        fig, ax = plt.subplots(figsize=(10, 10))

        # Transparence totale
        if transparency:
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.set_aspect('equal')
        ax.axis('off')

        # ---------------------------------------------------------
        # LE CORRECTIF : Forcer le cadrage de la caméra Matplotlib
        # ---------------------------------------------------------
        px, py = [p[0] for p in self.points], [p[1] for p in self.points]

        # On calcule une marge de 10% basée sur le rayon pour que les courbes extérieures respirent
        marge = self.radius * 0.1

        # On impose les limites de l'axe X et Y
        ax.set_xlim(min(px) - marge, max(px) + marge)
        ax.set_ylim(min(py) - marge, max(py) + marge)
        # ---------------------------------------------------------

        # Affichage conditionnel des sommets
        if show_nodes:
            ax.scatter(px, py, c='#111111', edgecolors='#111111', s=50, zorder=5, facecolors='none', lw=1.5)

        # Tracé des arcs pour chaque attribut (k)
        for k_step, sequence in binary_features.items():
            config = style_config.get(k_step, {}) if style_config else {}
            color = config.get('color', '#333333')
            curvature = config.get('curvature', 0.2)
            lw = config.get('lw', 2.0)

            for i, bit in enumerate(sequence):
                if bit == 1:
                    target_idx = (i + k_step) % self.n
                    self._draw_arc(ax, self.points[i], self.points[target_idx], color, curvature, lw)

        plt.tight_layout()

        # Sauvegarde propre avec transparence
        # plt.savefig("glyphe_magique.png", transparent=True, dpi=300, bbox_inches='tight')

        plt.show()


# ==========================================
# 3. EXÉCUTION ET GÉNÉRATION DU SORT
# ==========================================
if __name__ == "__main__":
    # --- A. INITIALISATION (7 attributs -> n=15) ---
    N_SOMMETS = 15
    encoder = SpellEncoder(n_vertices=N_SOMMETS)

    # Listes exhaustives pour la 5e édition
    encoder.register_attribute(k_step=1, features=[f"Niveau {i}" for i in range(10)])
    encoder.register_attribute(k_step=2,
                               features=["Abjuration", "Conjuration", "Divination", "Enchantement", "Evocation",
                                         "Illusion", "Nécromancie", "Transmutation"])
    encoder.register_attribute(k_step=3,
                               features=["Acide", "Contondant", "Froid", "Feu", "Force", "Foudre", "Nécrotique",
                                         "Perforant", "Poison", "Psychique", "Radiant", "Tranchant", "Tonnerre",
                                         "Aucun"])
    encoder.register_attribute(k_step=4,
                               features=["Cible Unique", "Cibles Multiples", "Cône", "Cube", "Cylindre", "Ligne",
                                         "Sphère"])
    encoder.register_attribute(k_step=5,
                               features=["Personnel", "Contact", "10 ft", "30 ft", "60 ft", "120 ft", "150 ft", "Vue",
                                         "Illimité"])
    encoder.register_attribute(k_step=6,
                               features=["Barde", "Clerc", "Druide", "Ensorceleur", "Magicien", "Occultiste", "Paladin",
                                         "Rôdeur", "Artificier", "Multiples"])
    encoder.register_attribute(k_step=7, features=["V", "S", "M", "V, S", "V, M", "S, M", "V, S, M"])

    # --- B. DÉFINITION D'UN SORT COMPLEXE ---
    # Exemple : Boule de Feu
    fireball_data = {
        1: "Niveau 3",
        2: "Evocation",
        3: "Feu",
        4: "Sphère",
        5: "150 ft",
        6: "Multiples",  # Magicien, Ensorceleur
        7: "V, S, M"
    }

    floating_disk = {
        1: "Niveau 1",
        2: "Enchantement",
        3: "Aucun",
        4: "Cibles Multiples",
        5: "30 ft",
        6: "Clerc",
        7: "V, S"
    }

    print("\n[*] Encodage du sort en cours...")
    encoded_spell = encoder.encode_spell(fireball_data)
    encoded_disk = encoder.encode_spell(floating_disk)


    for k, seq in encoded_spell.items():
        print(f"   k={k} -> {seq}")

    for k, seq in encoded_disk.items():
        print(f"   k={k} -> {seq}")

    # --- C. GÉNÉRATION GRAPHIQUE ---
    # On ajoute une petite distorsion pour l'aspect "dessiné à la main"
    grimoire_tech = SpellWeaver(n_vertices=15, grid_type='circle', distortion=0.0,)

    # Configuration des 7 couches (couleurs, courbure vers le centre, épaisseur)
    style_palette = {
        1: {'color': '#111111', 'curvature': 0, 'lw': 1.8},  # Violet (Niveau) - Périphérie
        2: {'color': '#111111', 'curvature': 0, 'lw': 1.8},  # Vert (École)
        3: {'color': '#111111', 'curvature': 0, 'lw': 1.5},  # Rouge (Dégâts)
        4: {'color': '#111111', 'curvature': 0, 'lw': 1.5},  # Rose (Zone)
        5: {'color': '#111111', 'curvature': 0, 'lw': 1.2},  # Orange (Portée)
        6: {'color': '#111111', 'curvature': 0, 'lw': 1.0},  # Cyan (Classes)
        7: {'color': '#111111', 'curvature': 0, 'lw': 0.8}  # Argent (Composantes) - Centre du sort
    }

    print("\n[*] Tracé du sort...")
    grimoire_tech.scribe_spell(encoded_spell, style_config=style_palette, show_nodes=False, transparency=False)
    grimoire_tech.scribe_spell(encoded_disk, style_config=style_palette, show_nodes=False, transparency=False)