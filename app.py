from ursina import *
import webbrowser
from threading import Thread

app = Ursina()

window.fullscreen = False


class GameScene(Entity):
    def __init__(self, level, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.right_door = None
        self.left_door = None
        self.cameraBtn = None
        self.cameras = None
        self.text3 = None
        self.text2 = None
        self.energy_state = False

        class text:
            text = None

        self.text = text
        self.door = None
        self.lol = None
        self.flashlight = None
        self.background = None
        self.lvl = level

        self.world = None
        self.ground = None
        self.pizzeria_texture = None
        self.pizzeria = None
        self.player = None
        self.pizzeria_model = None

        self.state = {'left': False,
                      'right': False}

        self.animatronics = {
            'bonny': [0, False, False, 'right', 1, 105],
            'freddy': [0, False, False, 'left', 1.2, 160],
            'chica': [0, False, False, 'right', 1.3, 135],
            'foxy': [0, False, False, 'left', 1.4, 115]
        }

        self.timer = 0
        self.energy = 100

        self.last_x = 0

        self.winner = False

        self.loser = False

        self.load()

    def load(self, off=False):
        if not off:
            self.background = Animation('assets/images/game.gif', parent=camera.ui)
            self.background.scale /= 6
            self.background.position = (0, 0)

            #self.left_door = Animation('assets/images/open.gif', parent=self.background,
            #                           position=(-0.5, 0),
            #                           loop=False,
            #                           color=rgb(0, 0, 0)
            #                           )
            #self.left_door.scale /= 6

            #self.right_door = Animation('assets/images/open.gif', parent=self.background,
            #                            position=Vec2(0.5, 0),
             #                           loop=False,
            #                            color=rgb(0, 0, 0)
             #                           )  # 123

            #self.right_door.scale /= 6

        self.lol = self.background.scale[2] / 2

        self.text = Text(f'{self.time_to_str()}', scale=2,
                         position=Vec2(-0.85, 0.45))
        self.text2 = Text(f'{self.energy} %', scale=2,
                          position=Vec2(0.70, -0.45))

        self.text3 = Text(f'Двери:\n'
                          f'left: {"да" if self.state["left"] else "нет"}\n'
                          f'right: {"да" if self.state["right"] else "нет"}',
                          scale=1.1,
                          position=Vec2(-0.85, -0.35))

        self.cameras = CameraMenu(self)

        self.cameraBtn = Button(position=Vec2(0, -0.4),
                                scale=(0.7, 0.1, 0.5),
                                text='Открыть камеры',
                                on_click=lambda: [playsound('click.mp3'), self.cameras.deopen() if self.cameras.state
                                else self.cameras.open()])

    def unload(self, off=False):
        self.cameras.unload()
        for i in [self.text, self.text2, self.text3, self.cameras, self.cameraBtn]:
            destroy(i)
        if not off:
            destroy(self.background)

    def time_to_str(self):
        minutes = int(self.timer / 60)
        seconds = int(self.timer - minutes * 60)
        if minutes == 0:
            minutes = 12
        res = f'{minutes}:'
        if len(str(seconds)) > 1:
            res += str(seconds)
        else:
            res += f'0{seconds}'
        return res

    def input(self, key):
        if key == 'left mouse down':
            if mouse.x <= -0.65:
                self.edit_door('left')
            elif mouse.x >= 0.65:
                self.edit_door('right')
            elif -0.16 >= round(mouse.x, 2) >= -0.19:
                playsound('pasx.mp3')
        if key == 'a':
            self.edit_door('left')
        if key == 'd':
            self.edit_door('right')
        if key == 'space':
            playsound('click.mp3')
            self.cameras.deopen() if self.cameras.state else self.cameras.open()
        elif key == 'escape':
            self.lose()

    def off_light(self):
        self.energy_state = True
        playsound('power.mp3')

        self.state['left'] = False
        self.state['right'] = False

        playsound('door.mp3')
        playsound('door.mp3')

        self.text3.text = f'Двери:\n' \
                          f'left: {"да" if self.state["left"] else "нет"}\n' \
                          f'right: {"да" if self.state["right"] else "нет"}'

        last_pos = (self.background.x, self.background.y)

        destroy(self.background)

        self.background = Animation('assets/images/off.gif', parent=camera.ui, loop=False, fps=60)
        self.background.scale /= 6
        self.background.position = last_pos

        self.unload(True)
        self.load(True)

    def update(self):
        if self.loser:
            return
        if self.timer >= 360 and self.winner is False:
            self.win()
            return
        elif self.winner:
            return

        self.text.text = self.time_to_str() + ' AM'
        self.text2.text = f'{int(self.energy)} %'
        self.timer += time.dt

        if self.energy > 0 and self.energy_state is False:
            if self.state['left']:
                self.energy -= time.dt
            if self.state['right']:
                self.energy -= time.dt
            self.energy -= 0.00001

        elif self.energy <= 0 and self.energy_state is False:
            self.off_light()

        if mouse.moving and abs(self.lol - mouse.x) >= 0.1:
            if mouse.x < self.lol:
                self.camera_move('left')
            else:
                self.camera_move('right')
        elif mouse.moving:
            self.camera_move('normal')
        self.check_animatronics()

    def camera_move(self, index):
        if index == 'left':
            self.background.position = (0.2, 0)
        elif index == 'normal':
            self.background.position = (0, 0)
        else:
            self.background.position = (-0.2, 0)

    def edit_door(self, x):
        if self.energy_state:
            return playsound('error.mp3')
        playsound('door.mp3')

        self.state[x] = not self.state[x]

        self.text3.text = f'Двери:\n' \
                          f'left: {"да" if self.state["left"] else "нет"}\n' \
                          f'right: {"да" if self.state["right"] else "нет"}'

        #if self.state[x]:
            #a = 'close.gif'
        #else:
            #a = 'open.gif'

        #destroy(getattr(self, f'{x}_door'))

        #obj = Animation(f'assets/images/{a}', parent=self.background,
        #                position=(-0.5 if x == 'left' else 0.5, 0),
        #                loop=False,
        #                fps=60
        #                )
        #obj.scale /= 6

        #setattr(self, f'{x}_door', obj)

    def check_animatronics(self):
        for animatronic in self.animatronics:
            if self.animatronics[animatronic][2] is False:
                self.animatronics[animatronic][0] += (time.dt * self.lvl) / self.animatronics[animatronic][4]
                if self.animatronics[animatronic][0] >= self.animatronics[animatronic][5] and self.animatronics[
                    animatronic][1] is False:
                    playsound(animatronic + '.mp3')
                    self.animatronics[animatronic][1] = True
                if self.animatronics[animatronic][1] and self.animatronics[animatronic][0] >= self.animatronics[ \
                        animatronic][5] + 50:
                    if self.state[self.animatronics[animatronic][3]]:
                        self.animatronics[animatronic][0] = 0
                        self.animatronics[animatronic][1] = False
                        self.animatronics[animatronic][2] = False
                        return
                    self.screamer(animatronic)
                    self.animatronics[animatronic][2] = True

    def screamer(self, animat):
        self.loser = True
        playvideo(animat + '.mp4')
        a = lambda: [time.sleep(5), self.lose()]
        Thread(target=a).start()

    def win(self):
        self.winner = True
        playsound('win.mp3')
        anim = Animation('win', loop=False, parent=camera.ui)
        anim.scale /= 2
        a = lambda: [time.sleep(5), self.lose()]
        Thread(target=a).start()

    def lose(self):
        global scene
        self.unload()
        scene = StartScene()
        destroy(self)


class CameraMenu(Entity):
    def __init__(self, player: GameScene, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ground = None
        self.player = player
        self.index = 1

        self.buttons = []

        self.state = False

        self.bonus = False

        self.clicks = ''

        self.bonus_sec = 0

        self.bonus_dest = False
        self.bonus_vid = None

    def get_func(self, i):
        def a():
            playsound('click.mp3')
            self.change(i)

        return a

    def load(self):
        self.ground = Entity(model='quad',
                             scale=(1.5, 0.9, 1.5),
                             position=Vec2(0, 0),
                             parent=camera.ui)
        x, y = 0.3, 0
        for i in range(1, 7):
            if self.index is not None and i == self.index:
                ent = Button(model='quad',
                             position=Vec2(x, y),
                             scale=(0.1, 0.08, 0.1),
                             color=rgb(120, 120, 120),
                             text='CAM ' + str(i),
                             on_click=self.get_func(i))
            else:
                ent = Button(model='quad',
                             position=Vec2(x, y),
                             scale=(0.1, 0.08, 0.1),
                             text='CAM ' + str(i),
                             on_click=self.get_func(i))
            if i % 3 == 0:
                x = 0.3
                y -= 0.1
            else:
                x += 0.15
            self.buttons.append(ent)
        self.state = True

        destroy(self.player.cameraBtn)

        self.player.cameraBtn = Button(position=Vec2(0, -0.4),
                                       scale=(0.7, 0.1, 0.5),
                                       text='Закрыть камеры',
                                       on_click=lambda: [playsound('click.mp3'),
                                                         self.player.cameras.deopen() if self.player.cameras.state
                                                         else self.player.cameras.open()])

    def update(self):
        if self.state:
            self.update_ground()
            if '4131' in self.clicks and self.bonus is False:
                self.bonus_vid = playvideo('bonus.mp4')
                self.bonus = True
            elif self.bonus is True and self.bonus_sec < 6:
                self.bonus_sec += time.dt
            elif self.bonus_sec >= 6 and self.bonus_dest is False:
                destroy(self.bonus_vid)
                self.bonus_dest = True
            if self.player.energy <= 0.5:
                self.deopen()

    def unload(self):
        [destroy(i) for i in self.buttons]
        destroy(self.ground)
        self.buttons = []
        self.state = False

        destroy(self.player.cameraBtn)

        self.player.cameraBtn = Button(position=Vec2(0, -0.4),
                                       scale=(0.7, 0.1, 0.5),
                                       text='Открыть камеры',
                                       on_click=lambda: [playsound('click.mp3'),
                                                         self.player.cameras.deopen() if self.player.cameras.state
                                                         else self.player.cameras.open()])

    def change(self, index):
        if self.bonus is False:
            self.clicks += str(index)
        try:
            if self.index is not None:
                old = self.buttons[self.index - 1]
                old_pos = (old.x, old.y)
                destroy(old)

                self.buttons[self.index - 1] = Button(model='quad',
                                                      position=Vec2(*old_pos),
                                                      scale=(0.1, 0.08, 0.1),
                                                      text='CAM ' + str(self.index),
                                                      on_click=self.get_func(self.index))
        except:
            pass

        self.index = index
        last = self.buttons[index - 1]

        position = (last.x, last.y)
        destroy(last)
        self.buttons[index - 1] = Button(model='quad',
                                         position=Vec2(*position),
                                         scale=(0.1, 0.08, 0.1),
                                         text='CAM ' + str(index),
                                         color=rgb(150, 150, 150),
                                         on_click=self.get_func(index))

        self.update_ground()

    def draw(self, animatronic):
        pass

    def update_ground(self):
        if self.index == 1:
            axa = [self.player.animatronics[i][1] for i in ['freddy', 'chica', 'bonny']]
            if True in axa:
                x = ''
                if self.player.animatronics['freddy'][1] is False:
                    x += 'f'
                if self.player.animatronics['chica'][1] is False:
                    x += 'c'
                if self.player.animatronics['bonny'][1] is False:
                    x += 'b'
                x = '1/' + x
                print(x)
            elif False not in axa:
                x = str(self.index) + '/none'
            else:
                x = str(self.index) + '/all'
        elif self.index == 3:
            x = str(self.index) + '/'

            if self.player.animatronics['foxy'][1]:
                x += '4'
            elif self.player.animatronics['foxy'][0] >= self.player.animatronics['foxy'][5]:
                x += '3'
            elif self.player.animatronics['foxy'][0] >= 60:
                x += '2'
            else:
                x += '1'
        else:
            x = str(self.index)

        self.ground.texture = load_texture('assets/camera/' + f'{x}.png')

    def open(self):
        if self.player.energy <= 0.5:
            return playsound('error.mp3')
        self.state = True
        self.load()
        self.update_ground()

    def deopen(self):
        self.state = False
        self.unload()


class StartMenu(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load()

    def load(self):
        y = 0.3
        for i in range(1, 7):
            setattr(self, 'btn_%s' % i, Button('Ночь %s' % i,
                                               position=Vec2(0, y),
                                               scale=(0.4, 0.1, 0.5),
                                               on_click=self.get_func(i)))
            y -= 0.1

    def get_func(self, index):
        def lamb():
            playsound('click.mp3')
            self.start_game(index)

        return lamb

    def unload(self):
        for i in range(1, 7):
            destroy(getattr(self, 'btn_%s' % i))

    def start_game(self, index):
        global scene
        scene.unload()
        for i in range(1, 7):
            destroy(getattr(self, 'btn_%s' % i))
        scene = GameScene(index)


class SettingsMenu(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fullscreen = None
        self.load()

    def load(self):
        y = 0.3
        self.fullscreen = Button('Полноэкранный режим',
                                 position=Vec2(0, y),
                                 scale=(0.4, 0.1, 0.5),
                                 on_click=self.set_fullscreen)

    def unload(self):
        destroy(self.fullscreen)

    def set_fullscreen(self):
        if window.fullscreen:
            window.fullscreen = False
        else:
            window.fullscreen = True


class StartScene(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sett_menu = None
        self.exitBtn = None
        self.music = None
        self.menu = None
        self.authorBtn = None
        self.playBtn = None
        self.settingsBtn = None
        self.background = None
        self.load()

    def load(self):
        background_image = "assets/images/background.gif"
        self.background = Animation(background_image, parent=camera.ui)
        self.background.scale /= 6
        self.background.position = (0, 0)

        self.playBtn = Button('Начать игру',
                              position=Vec2(-0.5, 0.3),
                              scale=(0.4, 0.1, 0.5),
                              on_click=lambda: [playsound('click.mp3'), self.open_menu()])

        self.settingsBtn = Button('Настройки',
                                  position=Vec2(-0.5, 0.2),
                                  scale=(0.4, 0.1, 0.5),
                                  on_click=lambda: [playsound('click.mp3'), self.open_settings()])

        self.authorBtn = Button('Автор',
                                position=Vec2(-0.5, 0.1),
                                scale=(0.4, 0.1, 0.5),
                                on_click=lambda: [playsound('click.mp3'), webbrowser.open('https://t.me/lord_code')])

        self.exitBtn = Button('Выйти из игры',
                              position=Vec2(-0.5, -0.01),
                              scale=(0.4, 0.1, 0.5),
                              on_click=lambda: [playsound('click.mp3'), os._exit(0)])

        self.music = Audio('music/background.mp3')
        self.music.play()

    def open_settings(self):
        if self.sett_menu is None:
            if self.menu is not None:
                self.menu.unload()
                self.menu = None
            self.sett_menu = SettingsMenu()
        else:
            self.sett_menu.unload()
            self.sett_menu = None

    def unload(self):
        destroy(self.background)
        destroy(self.playBtn)
        destroy(self.settingsBtn)
        destroy(self.authorBtn)
        destroy(self.exitBtn)
        if self.menu:
            self.menu.unload()
            self.menu = None
        if self.sett_menu:
            self.sett_menu.unload()
            self.sett_menu = None
        self.music.stop(True)

    def open_menu(self):
        if self.menu is None:
            if self.sett_menu is not None:
                self.sett_menu.unload()
                self.sett_menu = None
            self.menu = StartMenu()
        else:
            self.menu.unload()
            self.menu = None

    # def update(self):
    #     if held_keys['1']:
    #         player.update = lambda: FirstPersonController.update(player)


def playsound(name):
    audio = Audio('assets/music/' + name)
    audio.play()
    return audio


def playvideo(name):
    xx = 'assets/videos/' + name
    video_player = Entity(model='quad', parent=camera.ui, scale=(1.5, 1), texture=xx)
    video_sound = loader.loadSfx(xx)
    video_player.texture.synchronizeTo(video_sound)
    video_sound.play()
    return video_player


if __name__ == '__main__':
    scene = StartScene()
    app.run()
