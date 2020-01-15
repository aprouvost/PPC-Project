import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('GeeksForGeeks', True, green, blue)
textRect = text.get_rect()
textRect.center = (640 // 2, 480 // 2)



while True:
    # print("Debut ecoute")

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print("une touche a ete clicer")
            if event.key == pygame.K_LCTRL:
                text = font.render("Left Control clic", True, white, black)
                screen.fill(black)
                screen.blit(text, textRect)
                pygame.display.update()
                print("Left Control clic")
            if event.key == pygame.K_RCTRL:
                text = font.render("Right Control clic", True, white, black)
                screen.fill(black)
                screen.blit(text, textRect)
                pygame.display.update()
                print("Right Control clic")
            if event.key == pygame.K_DOWN:
                text = font.render("Down Control clic", True, white, black)
                screen.fill(black)
                screen.blit(text, textRect)
                pygame.display.update()
                print("Down clic")
