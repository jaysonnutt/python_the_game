import random
import curses

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

snk_x = sw/4
snk_y = sh/2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

score = 0

food = [sh/2, sw/2]
w.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT

while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Snake died
    if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:
        curses.endwin()
        print('Oh my, you\'ve died. Your score was {} this game.'.format(score))
        try:
            f = open('leader.txt', 'r')
            line = f.read()
            data = line.split(',')
            lead_score = data[1]
            leader_name = data[0]
            if int(lead_score) < score:
                print('You\'ve beaten {}\'s previous high score of {}!'.format(leader_name, lead_score)) 
                new_name = raw_input('What is your name champion? ')
                with open('leader.txt', 'w') as file:
                    file.write(new_name + ',' + str(score))
            quit()
        except IOError:
            if score > 0:
                print('You\'re the new leader.')
                winner_name = raw_input('What is your name? ')
                with open('leader.txt', 'w') as file:
                    file.write(winner_name + ',' + str(score))
            quit()

    new_head = [snake[0][0], snake[0][1]]

    prev_key = None

    if key == curses.KEY_DOWN and prev_key != 'up':
        new_head[0] += 1
        prev_key = 'down'
    if key == curses.KEY_UP and prev_key != 'down':
        new_head[0] -= 1
        prev_key = 'up'
    if key == curses.KEY_LEFT and prev_key != 'right':
        new_head[1] -= 1
        prev_key = 'left'
    if key == curses.KEY_RIGHT and prev_key != 'left':
        new_head[1] += 1
        prev_key = 'right'

    snake.insert(0, new_head)

    if snake[0] == food:
        score = score + 1
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
