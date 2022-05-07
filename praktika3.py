from time import sleep
from tkinter import *
from random import *
from math import *

answer = False
while answer == False:
    try:
        firework_num = int(input("Сколько фейерверков хотите запустить? "))
        answer = True
    except:
        pass

height = 600
width = 800
root = Tk()
root.title("Практика 3")

canvas = Canvas(root, width=width, height=height, background="black")
canvas.pack()

colors = ['red', 'blue', 'yellow', 'green', 'brown', 'orange', 'purple', 'navy']

remainder = int(firework_num % 10)
main_loop_times = int((firework_num - remainder) / 10)
for main_loop_number in range(main_loop_times + 1):
    ball_objects_fireworks = []
    angles_fireworks = []
    radii_of_particles_fireworks = []
    vx_fireworks = []
    vy_fireworks = []
    frame_number = []
    frames_seen = []
    firework_color = []
    ball_numbers = []
    glide_time = []
    xcenters_fireworks = []
    ycenters_fireworks = []
    interval_v = 4
    if main_loop_number == 0:
        number_of_fireworks = remainder
    else:
        number_of_fireworks = 10

    xcenter = 100
    ycenter = 100

    for j in range(number_of_fireworks):
        ball_num = randint(30, 95)
        balls = []
        angles = []
        r = []
        xs = []
        ys = []
        vx = []
        vy = []
        xcenter += (width - 200) / number_of_fireworks
        ycenter = ycenter + randint(-5, 10)

        for i in range(ball_num):
            a = []
            balls.append(0)
            angles.append(uniform(0, 2 * pi))
            r.append(randint(4, 5))
            xs.append(xcenter)
            ys.append(ycenter)
            vx.append(uniform(-interval_v * 1.1, interval_v * 1.1))
            vy.append(uniform(-interval_v, interval_v))

        ball_objects_fireworks.append(balls)
        angles_fireworks.append(angles)
        radii_of_particles_fireworks.append(r)
        xcenters_fireworks.append(xs)
        ycenters_fireworks.append(ys)
        vx_fireworks.append(vx)
        vy_fireworks.append(vy)
        frame_number.append(randint(17, 34))
        glide_time.append(randint(0, 12))
        firework_color.append(colors[randint(0, len(colors) - 1)])

    rocketsx = []
    rocketsy = []
    rocketsv = []
    rocket_body_objects = []
    rocket_radii = []
    rocket_start_frame = []
    rocket_n = []
    rocket_tail_objects = []
    rocket_head_object = []
    animate_firework = []
    initial_start = 30
    for i in range(number_of_fireworks):
        rocketsx.append(xcenters_fireworks[i])
        rocketsy.append(height - 100)
        rocketsv.append(uniform(14, 18))
        rocket_body_objects.append(0)
        rocket_tail_objects.append(0)
        rocket_head_object.append(0)
        rocket_radii.append(randint(4, 7))
        animate_firework.append(False)
        rocket_start_frame.append(initial_start)
        initial_start += randint(20, 40)
        rocket_n.append(0)
        frames_seen.append(0)

    shuffle(rocket_start_frame)
    setoff = []
    frame = 0
    while len(setoff) < number_of_fireworks:
        for i in range(number_of_fireworks):
            if animate_firework[i] == False:
                if rocket_start_frame[i] <= frame:
                    rocketsy[i] -= rocketsv[i] - rocket_n[i] ** 2
                    rocket_n[i] += 0.009
                    rc = [rocketsx[i][0] - rocket_radii[i], rocketsy[i] - rocket_radii[i],
                          rocketsx[i][0] + rocket_radii[i],
                          rocketsy[i] + rocket_radii[i], ]
                    rocket_body_objects[i] = canvas.create_oval(rc[0], rc[1], rc[2], rc[3], fill=firework_color[i])
                if rocketsy[i] < ycenters_fireworks[i][0]:
                    animate_firework[i] = True
                    canvas.delete(rocket_body_objects[i])
                    rocketsx[i] = 0
                    rocketsy[i] = 0
                    rocketsv[i] = 0
                    rocket_body_objects[i] = 0
                    rocket_radii[i] = 0
                    rocket_start_frame[i] = 0
                    rocket_n[i] = 0
            elif frames_seen[i] <= frame_number[i]:
                for k in range(len(radii_of_particles_fireworks[i])):
                    radii_of_particles_fireworks[i][k] = radii_of_particles_fireworks[i][k] - 4 / frame_number[i]
                    xcenters_fireworks[i][k] = xcenters_fireworks[i][k] + radii_of_particles_fireworks[i][k] * cos(
                        angles_fireworks[i][k]) + vx_fireworks[i][k]
                    ycenters_fireworks[i][k] = ycenters_fireworks[i][k] - radii_of_particles_fireworks[i][k] * sin(
                        angles_fireworks[i][k]) + vy_fireworks[i][k] + 0.005 * frames_seen[i] ** 2
                    ball_objects_fireworks[i][k] = canvas.create_oval(
                        xcenters_fireworks[i][k] - radii_of_particles_fireworks[i][k],
                        ycenters_fireworks[i][k] - radii_of_particles_fireworks[i][k],
                        xcenters_fireworks[i][k] + radii_of_particles_fireworks[i][k],
                        ycenters_fireworks[i][k] + radii_of_particles_fireworks[i][k],
                        fill=firework_color[i], outline=firework_color[i])
                frames_seen[i] += 1
            elif frames_seen[i] - glide_time[i] <= frame_number[i]:
                for k in range(len(radii_of_particles_fireworks[i])):
                    xcenters_fireworks[i][k] = xcenters_fireworks[i][k] + radii_of_particles_fireworks[i][k] * cos(
                        angles_fireworks[i][k]) + vx_fireworks[i][k] / 2
                    ycenters_fireworks[i][k] = ycenters_fireworks[i][k] - radii_of_particles_fireworks[i][k] * sin(
                        angles_fireworks[i][k]) + vy_fireworks[i][k] / 2 + 0.005 * frames_seen[i] ** 2
                    ball_objects_fireworks[i][k] = canvas.create_oval(
                        xcenters_fireworks[i][k] - radii_of_particles_fireworks[i][k],
                        ycenters_fireworks[i][k] - radii_of_particles_fireworks[i][k],
                        xcenters_fireworks[i][k] + radii_of_particles_fireworks[i][k],
                        ycenters_fireworks[i][k] + radii_of_particles_fireworks[i][k],
                        fill=firework_color[i], outline=firework_color[i])
                frames_seen[i] += 1
            else:
                if i not in setoff:
                    setoff.append(i)
        canvas.update()
        sleep(0.025)
        for i in range(number_of_fireworks):
            if animate_firework[i] == False:
                canvas.delete(rocket_body_objects[i])
            else:
                for particle in ball_objects_fireworks[i]:
                    canvas.delete(particle)
        frame += 2