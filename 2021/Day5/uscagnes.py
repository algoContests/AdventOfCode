import random
input = "Jphi Phil Hub Franck Christophe Jérôme JPaul Mario Fabio Marc"
les_copains = input.split(' ')
capitaine = "Hub"
meilleur_joueur = random.choice(les_copains)
meilleur_joueur = random.choice([meilleur_joueur] + [capitaine])
print(meilleur_joueur)
