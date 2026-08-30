---
title: "Pourquoi les data centers boivent notre eau (et ce que le local-first change)"
date: 2026-08-30T19:40:00+02:00
draft: false
description: "Un serveur qui calcule est un radiateur. Derrière chaque requête vers un hyperscaler, des litres d'eau s'évaporent quelque part pour refroidir la machine. Voici d'où vient cette consommation et pourquoi faire tourner ses propres modèles en local en change une partie."
tags: ["souverainete", "ecologie", "ia-locale", "reflexion"]
cover:
  image: "images/data-center-eau-local-first.png"
  alt: "Illustration sur la consommation d'eau des data centers et le local-first"
  caption: "Généré avec ComfyUI"
---

On parle beaucoup d'énergie quand on évoque l'intelligence artificielle. Moins d'eau. Pourtant, chaque fois que vous envoyez un prompt à un grand modèle hébergé dans le cloud, une goutte — en fait, plusieurs litres — d'eau quelque part s'évapore pour que la réponse vous revienne. Ce n'est pas une métaphore. C'est de la thermodynamique élémentaire, déplacée à l'échelle industrielle.

## Un serveur qui calcule est un radiateur

Tout appareil qui transforme du courant en calcul finit, inévitablement, par le transformer en chaleur. C'est la première loi de la thermodynamique : l'énergie ne disparaît pas, elle se dégrade. Dans un data center, des milliers de serveurs empilés chauffent en continu. Sans évacuation, le matériel monte jusqu'à son seuil de sécurité, puis « throttle » (ralentit) ou s'éteint. Le refroidissement n'est donc pas un luxe : c'est ce qui permet au calcul d'exister.

Il existe deux manières de refroidir. L'air, simple mais peu efficace pour les fortes densités. Et l'eau, bien plus performante. Les grands centres utilisent des **tours de refroidissement évaporatives** : on fait circuler l'eau contre les échangeurs chauds, une partie s'évapore, et cette évaporation emporte la chaleur. Le hic : l'eau évaporée est perdue. Il faut en réinjecter en permanence.

## Deux postes, un seul oublié

La consommation d'eau d'un data center se compte sur deux lignes, et la deuxième est celle que presque personne ne voit.

La première, **directe** : l'eau pompée sur site pour les tours de refroidissement. Les études (Google, Meta, département de l'Énergie américain) donnent une fourchette d'environ **1,8 à 2 litres d'eau évaporée par kWh** de charge informatique. Pour un centre qui tourne à plusieurs mégawatts, on parle de millions de litres par jour.

La deuxième, **indirecte** : l'eau nécessaire à la *production* de l'électricité que le centre consomme. Une centrale thermique ou nucléaire doit elle aussi refroidir ses turbines — et évapore de l'eau dans ses propres tours. Même l'hydroélectricité a un coût en évaporation des retenues. Comptabilisée, cette eau « virtuelle » amont fait souvent passer le total à **3 à 5 litres par kWh**.

Autrement dit, une bonne partie de l'eau « consommée » par un data center ne touche jamais ses serveurs. Elle s'est évaporée ailleurs, dans une centrale, pour produire le courant qu'il a avalé.

## L'effet amplificateur de l'IA générative

Jusqu'à récemment, les data centers servaient surtout du stockage, des requêtes web, des vidéos. Des charges réparties, pas toujours intenses. L'IA générative a changé la donne : l'entraînement comme l'inférence de grands modèles saturent des **GPU qui chauffent fort** — une seule puce de type H100 peut tirer plusieurs centaines de watts, et un cluster en compte des milliers.

Une session d'entraînement de quelques jours, ou des milliards de prompts d'utilisateurs, se traduisent en volumes d'eau considérables. Les rapports de durabilité de Microsoft et Meta le montrent noir sur blanc : des **milliards de litres par an**, et une hausse à deux chiffres depuis l'explosion des LLM.

Le point qui fâche : ces centres poussent souvent dans des **zones déjà en stress hydrique** — l'Arizona, la Virginie, certaines régions d'Europe. On puise l'eau locale pour rafraîchir des calculs qui servent des utilisateurs à l'autre bout du monde. La facture environnementale est délocalisée, et donc invisible à celui qui tape son prompt.

## Ce que le local-first change (vraiment)

Faire tourner ses propres modèles en local — comme on le pratique ici avec Gemma 4 12B sur Ollama, ou Zombie en ComfyUI — ne rend pas la physique magiquement gratuite. Votre machine consomme du courant, donc indirectement un peu d'eau en amont. Mais trois choses changent :

- **Vous ne servez pas des millions d'inconnus.** Le calcul sert une personne, pas une plateforme mondiale. La densité d'usage s'effondre.
- **Vous évitez le refroidissement évaporatif industriel.** Pas de tour de refroidissement chez vous : la chaleur part dans la pièce, ou via le circuit déjà présent de votre logement.
- **Vous reprenez le contrôle du coût réel.** Énergie, chaleur, matériel, usure : ce sont des variables que vous voyez, pas un compte opaque chez un hyperscaler.

C'est l'essence même de la souveraineté numérique : ne pas seulement reprendre la main sur ses données, mais comprendre — et assumer — le coût matériel de son propre usage de l'IA.

## Une nuance honnête

Le local n'est pas une absolution écologique. Un poste personnel mal optimisé peut être *moins* efficient à watt près qu'un centre conçu pour le PUE (Power Usage Effectiveness) optimal. La différence n'est pas dans l'efficience unitaire, elle est dans **l'échelle et la responsabilité** : un calcul fait pour vous, à la demande, plutôt qu'une infrastructure permanente qui tourne pour tout le monde.

Et il y a une piste souvent oubliée : la chaleur de votre machine, plutôt que de la dissiper dans le vide, peut **chauffer une pièce en hiver**. Récupérer la déperdition, c'est retourner la thermodynamique à votre avantage.

## En guise de conclusion

Demander « pourquoi les data centers consomment de l'eau » revient à demander « où va la chaleur de mes calculs ». La réponse honnête : elle s'évapore, loin, au détriment d'aquifères locaux, pour des services que nous rendons transparents.

Passer au local-first ne résout pas le réchauffement climatique. Mais ça transforme une facture invisible en un choix visible — et ça commence par reconnaître que chaque token généré a un poids physique, pas seulement numérique.
