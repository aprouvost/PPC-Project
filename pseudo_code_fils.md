# Process fils :

  Communication:
    
    - Pipe avec le pere
    
  Objets:
  
    - Main (dico, initialement 5 cartes piocher)
    - Boark (sharedMemory)
    - Timer
  
  Fonctions :
  
    - Piocher carte : signal envoyé au pere
    - Timeout -> Pop-up jouer ou piocher lock Pioche et Board + envoyer un siganl au pere
    - freezTimer : signal du pere quand timeout de l'autre joueur
    - Poser carte : signal envoyé au pere + retour du pere pour sipprimer la carte si valid sinon garder la carte et piocher
    - UpdateBoard : signal du pere pour update quand l'autre a jouer
