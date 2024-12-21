def keys(pygame, running, move_up, move_down, move_left, move_right):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                move_up = True
            if event.key in (pygame.K_s, pygame.K_DOWN):
                move_down = True
            if event.key in (pygame.K_a, pygame.K_LEFT):
                move_left = True
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP):
                move_up = False
            if event.key in (pygame.K_s, pygame.K_DOWN):
                move_down = False
            if event.key in (pygame.K_a, pygame.K_LEFT):
                move_left = False
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                move_right = False
    return running, move_up, move_down, move_left, move_right