'''
    09/06/26
    Second attempt at pendulum but this time using better gui and putting theta in radians to hopefully use matplotlib
    to create sin and cos graphs.
    Update;
    Was going to use sliders for gui but realised keys would be easier, also used text to display x2, y2 and Vo.
    Theta turned out to be in radians already, had to figure out the arctan method to find radians.
    Got matplotlib to display radians to time.
    Completed
    11/06/26
'''
import asyncio # lets web handle loops
import matplotlib
import numpy as np
import pygame as pg
from fontTools.merge.util import current_time

#use 1 window(did not take an hour to figure out)
matplotlib.use('Agg')
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import sys
#putting everything in big safe loop
async def main():
    global preRunning, running, θ, omega, alpha, x2, y2, x2fake, y2fake, Vo, R, x2t, y2t, Vot, Rt, θt, frame_count, graph_surf, current_time

    #matplotlib setup
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(5,4), dpi=100)

    #pygame setup
    SCREEN_WIDTH = 1300
    SCREEN_HEIGHT = 600
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    fps = 60
    running = False
    preRunning = True

    #vars

    #colours
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    DARK_BLUE = (0, 0, 200)
    GREY = (200, 200, 200)

    #math vars
    R = 200
    Vo = 0
    pi = np.pi
    centrePoint = [400,300]
    g = 9.81
    PPM = 100
    l = R / PPM
    omega = Vo/R #angular velocity
    x1 = centrePoint[0]
    y1 = (centrePoint[1]+R)
    x2 = centrePoint[0]
    y2 = centrePoint[1] + R
    θ = np.arctan2(x2 - centrePoint[0], y2 - centrePoint[1])
    #θ = 0
    x1fake = x1 - centrePoint[0]
    y1fake = y1 - centrePoint[1]
    x2fake = x2 - centrePoint[0]
    y2fake = y2 - centrePoint[1]
    alpha = -(g / l) * np.sin(θ)

    #display text setup ye
    pg.display.set_caption('Pendulum Sim')#changegs window name which makes a big difference
    my_font = pg.font.SysFont(pg.font.get_default_font(), 30)
    x2t = f"X position relative to centre = {x2fake:.2f}"
    y2t = f"Y position relative to centre = {y2fake:.2f}"
    Vot = f"Vo = {Vo:.2f} (885 ≈ equilibrium)"
    Rt = f"R length = {R:.1f}"
    θt = f"radians = {θ:.2f}"

    def doText():
        text_surfaceθ = my_font.render(θt, True, (0, 0, 0))
        text_surfaceVo = my_font.render(Vot, True, (0, 0, 0))
        text_surfaceRt = my_font.render(Rt, True, (0, 0, 0))
        text_surfacex2 = my_font.render(x2t, True, (0, 0, 0))
        text_surfacey2 = my_font.render(y2t, True, (0, 0, 0))

        screen.blit(text_surfaceVo, (10, 10))
        screen.blit(text_surfaceθ, (10, 50))
        screen.blit(text_surfaceRt, (10, 90))
        screen.blit(text_surfacex2, (800, 10))
        screen.blit(text_surfacey2, (800, 50))

    #live plot stuff used ai for this
    time_history = []
    θ_history = []
    current_time = 0.0

    #copied
    def get_graph_surface(t_data, θ_data):
        ax.clear()
        ax.plot(t_data, θ_data, color='blue', label='theta (rad)')
        ax.set_ylabel("Angle (Radians)")
        ax.set_xlabel('time (s)')
        ax.set_title("pendulum Sim")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_ylim(-pi, pi)

        #only shows last 5 secs
        if t_data:
            ax.set_xlim(max(0, t_data[-1] -5), max(5, t_data[-1]))

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = bytes(renderer.buffer_rgba())
        size = canvas.get_width_height()

        return pg.image.fromstring(raw_data, size, "RGBA")

    #theta setup and Vo if gonna use so cant be used during pendulum swing which may mess things up
    while preRunning:
        dt = clock.tick(fps) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill(WHITE)

        def calcNewRad():
            global θ, omega, alpha
            omega = Vo / R
            omega += alpha
            #θ = np.arccos((x1fake * x2fake + y1fake * y2fake) / (R * R)) * ((x2-centrePoint[0])/abs((x2-centrePoint[0])))
            #other way of writing what i wrote above without using cos and making code simpler-from ai
            θ = np.arctan2(x2 - centrePoint[0], y2 - centrePoint[1])

        #keys (a = move pend. left, d = move pend. right, w = start sim. q = Vo +, e = Vo -, z = increaseR, c = decreaseR)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            θ -= 0.05
            x2 = centrePoint[0] + R * np.sin(θ)
            y2 = centrePoint[1] + R * np.cos(θ)
            x2fake = x2 - centrePoint[0]
            y2fake = y2 - centrePoint[1]
        if keys[pg.K_d]:
            θ += 0.05
            x2 = centrePoint[0] + R * np.sin(θ)
            y2 = centrePoint[1] + R * np.cos(θ)
            x2fake = x2 - centrePoint[0]
            y2fake = y2 - centrePoint[1]
        if keys[pg.K_q]:
            Vo -= 10
            omega = Vo / R
        if keys[pg.K_e]:
            Vo += 10
            omega = Vo / R
        if keys[pg.K_z]:
            R += 5
            x2 = centrePoint[0] + R * np.sin(θ)
            y2 = centrePoint[1] + R * np.cos(θ)
        if keys[pg.K_c]:
            R -= 5
            x2 = centrePoint[0] + R * np.sin(θ)
            y2 = centrePoint[1] + R * np.cos(θ)
        if keys[pg.K_w]:
            preRunning = False
            running = True
            calcNewRad()

        # draw
        pg.draw.line(screen, BLACK, centrePoint, (x2, y2), 2)
        pg.draw.circle(screen, BLACK, (centrePoint[0], centrePoint[1]), 5)
        pg.draw.circle(screen, RED, (x2, y2), 10)

        x2t = f"X position relative to centre = {x2fake:.2f}"
        y2t = f"Y position relative to centre = {y2fake:.2f}"
        Vot = f"Vo = {Vo:.2f} (885 ≈ equilibrium)"
        Rt = f"R length = {R:.1f}"
        θt = f"radians = {θ:.2f}"
        doText()

        graph_surf = get_graph_surface(time_history, θ_history)
        screen.blit(graph_surf, (800, 100))
        pg.display.flip()
        await asyncio.sleep(0)

    #saving computer
    frame_count = 0
    graph_surf = None

    while running:
        dt = clock.tick(fps) / 1000.0
        if dt > 0.1:
            dt = 0.1

        current_time += dt

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill(WHITE)

        #physics
        l = R / PPM
        θ = np.arctan2(x2 - centrePoint[0], y2 - centrePoint[1])
        alpha = -(g / l) * np.sin(θ)
        omega += alpha * dt
        θ += omega * dt
        x2 = centrePoint[0] + R * np.sin(θ)
        y2 = centrePoint[1] + R * np.cos(θ)
        x2fake = x2 - centrePoint[0]
        y2fake = y2 - centrePoint[1]

        #more graphing stuff
        time_history.append(current_time)
        θ_history.append(θ)

        #draw
        pg.draw.line(screen, BLACK, centrePoint, (x2, y2), 2)
        pg.draw.circle(screen,BLACK,(centrePoint[0],centrePoint[1]),5)
        pg.draw.circle(screen,RED,(x2,y2),10)

        if frame_count % 6 == 0 or graph_surf is None:
            graph_surf = get_graph_surface(time_history, θ_history)

        frame_count += 1
        screen.blit(graph_surf, (800, 100))

        # text
        x2t = f"X position relative to centre = {x2fake:.2f}"
        y2t = f"Y position relative to centre = {y2fake:.2f}"
        Vot = f"Vo = {Vo:.2f} (885 ≈ equilibrium)"
        Rt = f"R length = {R:.1f}"
        θt = f"radians = {θ:.2f}"
        doText()

        #necessary stuff
        pg.display.flip()
        #print(round(θ, 2))
        #print(round((x2-x1), 2))
        #print(round((y1-y2), 2))
        await asyncio.sleep(0)

    pg.quit()

asyncio.run(main())