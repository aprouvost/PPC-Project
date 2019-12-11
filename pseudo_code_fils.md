* Process fils :

  Communication:
    
    - Pipe avec le pere
    
  Objets:
    - Main (dico, initialement 5 cartes piocher)
    - Boark (sharedMemory)
    - Timer
  
  Fonctions:
    - Piocher carte : signal envoyé au pere
      * un siganl est envoyé au pere pour indiquer que le fils pioche
      * la pile est lock pendant que le fils pioche pour eviter que le 2eme fils pioche la meme carte
      * remet le timer a 0
    - Timeout -> Pop-up jouer ou piocher lock Pioche et Board + envoyer un signal au pere
      * Le joueur est obligé de jouer ou de piocher apres un temps definie
      * remet le timer a 0
    - freezTimer : signal du pere quand timeout de l'autre joueur
      * quand le timer arrive a expiration de l'autre joueur celui-ci se freez
      * lorsque l'autre joueur a jouer ou piocher son timer reprend
    - Poser carte : signal envoyé au pere + retour du pere pour supprimer la carte si valid sinon garder la carte et piocher
      * un signal est envoyer au pere indiquant que le joueur veut jouer ( cette demande est mis dans la message queue)
      * le pere verifie la jouabilité de la carte : 
                                                    + si pas jouable : le pere envoie un signal au fils de piocher
                                                    + si jouable : le pere envoie un signal au fils de supprimer la crte qu'il joue
      * remet le timer a 0
    - UpdateBoard : signal du pere pour update quand l'autre a jouer
      * un signal est envoyé par le pere pour indiquer un changement de la carte au dessus du Board
      * le joueur recupere la carte qui est sur le Board et met a jour celle qui est affiché a l'ecran
