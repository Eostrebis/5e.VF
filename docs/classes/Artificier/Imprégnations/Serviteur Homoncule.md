*Objet : une gemme ou un cristal valant au moins 100 PO*

Vous apprenez de complexes méthodes pour magiquement créer un homoncule spécial qui vous servira. L'objet que vous imprégnez de cette manière fonctionne comme le cœur de la créature, autour duquel le corps de la créature se forme instantanément.

Vous choisissez l'apparence de l'homoncule. Certains artificiers préfèrent des oiseaux mécaniques, tandis que d'autres choisissent des fioles ailées ou des chaudrons miniatures animés.

L'homoncule est amical avec vous et vos compagnons, et obéit à vos ordres. Les statistiques de cette créature sont présentées dans son bloc de statistiques plus bas. Ce bloc utilise à plusieurs reprises votre modificateur de maîtrise (PB).

En combat, l'homoncule partage votre initiative, mais agit juste après vous. Il peut bouger et utiliser sa réaction de lui-même, mais ne prend que l'action d'Esquiver si vous n'utilisez pas votre action bonus pour lui donner un ordre. Cet ordre peut être une action dans son bloc ou n'importe quelle autre action. Si vous êtes [[incapacité]], l'homoncule peut prendre n'importe quelle action de son choix.

L'homoncule regagne 2d6 points de vie lorsque le sort [[réparation]] est lancé sur lui. Si vous ou l'homoncule mourez, il disparaît, laissant son cœur au sol.

```statblock
image: [[homonculus.jpg]]
name: Serviteur Homoncule
size: Très Petite
type: Construction 
ac: 13 (armure naturelle)
hp: 1 + votre modificateur d'Intelligence + votre niveau d'artificier (niveau d'artificier*d4 dés de vie)
speed: 20 ft., vol 30 ft.
stats: [4, 15, 12, 10, 10, 7]
saves:
  - Dextérité: "+2+PB"
skillsaves:
  - Discretion: "+2+PB"
  - Perception: "+PB*2"
damage_immunities: Poison
condition_immunities: [[Épuisement|Épuisé]], [[Empoisonné]]
senses: Vision dans le noir 60 ft.
languages: Comprend les langues que vous parlez
cr: --
traits:
  - name: Évasion
    desc: Si l'homoncule est soumis à un effet qui lui autorise un jet de sauvegarde de Dextérité pour ne prendre que la moitié des dégâts, il ne prend plutôt aucun dégâts si il réussit le jet de sauvegarde, et la moitié sinon.
actions:
  - name: Coup de Force
    desc: "Attaque à distance avec une arme : votre modificateur d'attaque avec un sort pour toucher, portée 30 ft., une cible que vous pouvez voir. Touché : 1d4 + PB dégâts de force."
reactions:
  - name: Canalisation de la Magie
    desc: L'homoncule dèlivre un sort avec la portée 'Touché' que vous lancez. L'homoncule doit être à 120 ft. de vous.
```