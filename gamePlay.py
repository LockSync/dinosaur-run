import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import random
import sys
import os


class Ground(Sprite):
    """地板"""

    def __init__(self, cfg):
        super(Ground, self).__init__()
        """
        1加载图片：两张同样的图片
        2加载图片矩形
        图片1的left 和bottom分别等0和cfg.screen_size[1]
        图片2 left和bottom等于图片1right和bottom

        
        3定义速度，两张图片向左移动
        4.更新
        如果图1right<0 图1left=图2 right
        如果图2right<0 图2left=图1 right
        以此实现地面不断更新

        """
        self.cfg = cfg
        self.image_0 = pygame.image.load('images/ground.png')
        self.image_1 = pygame.image.load('images/ground.png')
        self.rect_0 = self.image_0.get_rect()
        self.rect_1 = self.image_1.get_rect()
        self.rect_0.left = 0
        self.rect_0.bottom = self.cfg.screen_size[1]
        self.rect_1.left = self.rect_1.right
        self.rect_1.bottom = self.rect_0.bottom

        # 移动速度
        self.cfg = cfg
        self.speed = self.cfg.speed

    def update(self):
        """更新地板位置"""
        self.rect_0.left += self.speed
        self.rect_1.left += self.speed
        if self.rect_0.right < 0:
            self.rect_0.left = self.rect_1.right
        if self.rect_1.right < 0:
            self.rect_1.left = self.rect_0.right

    def draw(self, screen):
        """把地板画到屏幕"""
        screen.blit(self.image_0, self.rect_0)
        screen.blit(self.image_1, self.rect_1)


class Cloud(Sprite):
    """云"""

    def __init__(self, cfg, **kwargs):
        super(Cloud, self).__init__()
        """
        加载图片
        加载图片矩形
        定义移动速度
        """
        self.images = []
        self.image_0 = pygame.image.load('images/cloud.png')
        self.image_1 = pygame.image.load('images/blue_cloud.png')
        self.images.append(self.image_0)
        self.images.append(self.image_1)
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.position = (cfg.screen_size[0], random.randrange(30, 75))
        self.rect.left, self.rect.top = self.position

        self.cfg = cfg
        self.speed = -2

    def draw(self, screen):
        """把云画到屏幕上"""
        screen.blit(self.image, self.rect)

    def update(self):
        """更新云位置

        """
        self.rect = self.rect.move([self.speed, 0])
        if self.rect.left < 0:
            self.kill()


class Cactus(Sprite):
    """仙人掌"""

    def __init__(self, cfg, position=(600, 147), sizes=[(40, 40), (40, 40)], **kwargs):
        super(Cactus, self).__init__()
        """加载图片，定义速度"""
        # 导入图片
        self.images = []
        self.image = pygame.image.load('images/cacti-big.png')
        for i in range(3):
            # pygame.transform.scale无损缩放
            # image.subsurface抠图
            self.images.append(pygame.transform.scale(self.image.subsurface((i * 101, 0), (101, 101)), sizes[0]))
        self.image = pygame.image.load('images/cacti-small.png')
        for i in range(3):
            self.images.append(pygame.transform.scale(self.image.subsurface((i * 68, 0), (68, 70)), sizes[1]))
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        # 图形遮罩,用于精确到1像素的碰撞检测
        self.mask = pygame.mask.from_surface(self.image)
        self.cfg = cfg
        self.speed = self.cfg.speed

    def draw(self, screen):
        """把仙人掌画到屏幕上"""
        screen.blit(self.image, self.rect)

    def update(self):
        """
        重写了Group的update方法
        对Group中每一个精灵，都直接调用update方法
        """
        """更新仙人掌"""
        # 移动矩形 仙人掌到达屏幕边缘，调用kill方法
        self.rect = self.rect.move([self.speed, 0])
        if self.rect.right < 0:
            self.kill()


class Scoreboard(Sprite):
    """
    计分板，不需移动，只需要实时更新当前分数
    每满一百分，发出一个提示音
    """

    def __init__(self, position, size=(11, 13), is_highest=False, bg_color=None, **kwargs):
        super(Scoreboard, self).__init__()
        self.images = []
        self.position = position
        image = pygame.image.load('images/numbers.png')
        for i in range(12):
            self.images.append(pygame.transform.scale(image.subsurface((i*20, 0), (20, 24)), size))
        if is_highest:
            self.image = pygame.Surface((size[0] * 8, size[1]))
        else:
            self.image = pygame.Surface((size[0] * 5, size[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position
        # 一些必要变量
        self.is_highest = is_highest
        self.bg_color = bg_color
        self.score = '00000'

    def set_score(self,score):
        """设置得分"""
        # 用零填充5位
        self.score = str(score).zfill(5)

    def draw(self, screen):
        """画到屏幕上"""
        self.image.fill(self.bg_color)
        for idx, digital in enumerate(list(self.score)):
            digital_image = self.images[int(digital)]
            if self.is_highest:
                self.image.blit(digital_image, ((idx + 3) * digital_image.get_rect().width, 0))  # ?????
            else:
                self.image.blit(digital_image, (idx * digital_image.get_rect().width, 0))
        screen.blit(self.image, self.rect)


class Ptera(Sprite):
    """
    飞龙
    """

    def __init__(self, cfg, size=(46, 40), **kwargs):
        super(Ptera, self).__init__()
        self.cfg = cfg
        self.size = size
        # 随即生成飞龙的位置
        self.position = (600, random.randrange(1, 100))
        self.images = []
        self.image = pygame.image.load('images/ptera.png')
        for i in range(2):
            self.images.append(pygame.transform.scale(self.image.subsurface((i * 92, 0), (92, 81)), self.size))
        self.image_idx = 0
        self.image = self.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position
        self.mask = pygame.mask.from_surface(self.image)
        # 定义一些必要变量
        self.cfg = cfg
        self.speed = self.cfg.speed
        self.refresh_rate = 10
        self.refresh_counter = 0

    def update(self):
        """更新飞龙位置"""
        """
        所有飞龙出场时都是0号形态，每移动10个像素，改变成一号形态，再过10个像素，再变成0号形态，两种形态来回变换，
        直到到达屏幕边缘
        如果有一种形态飞出屏幕边缘，则kill掉整只飞鸟
        """
        if self.refresh_counter % self.refresh_rate == 0:
            self.refresh_counter = 0
            self.image_idx = (self.image_idx + 1) % len(self.images)
            self.load_image()
        self.rect = self.rect.move([self.speed, 0])
        if self.rect.right < 0:
            self.kill()
        self.refresh_counter += 1

    def draw(self):
        """把飞龙画到屏幕上"""
        screen.blit(self.image, self.rect)

    def load_image(self):
        """
        载入当前状态的图片
        飞龙有两种状态
        """
        self.image = self.images[self.image_idx]
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)


class Dinosaur(Sprite):
    """
     position=(40, 147), size=[(44, 47), (59, 47)]
     unduck transform : ((i*88, 0), (88, 95))
     duck transform : (i*118, 0), (118, 95)
    """
    """小恐龙"""

    def __init__(self, cfg, position=(40, 147), size=[(44, 47), (59, 47)], **kwargs):
        super(Dinosaur, self).__init__()
        if size is None:
            size = [(44, 47), (59, 47)]
        """加载图片"""
        self.image_0 = pygame.image.load('images/dino.png')
        self.image_1 = pygame.image.load('images/dino_ducking.png')
        self.images = []
        # 把dino.png截取五部分
        for i in range(5):
            self.images.append(pygame.transform.scale(self.image_0.subsurface((i * 88, 0), (88, 95)), size[0]))

        # 把dino_ducking.png截取两部分
        for i in range(2):
            self.images.append(pygame.transform.scale(self.image_1.subsurface((i * 118, 0), (118, 95)), size[1]))

        self.image_idx = 0
        self.image = self.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        self.mask = pygame.mask.from_surface(self.image)

        # 定义必要变量
        self.init_position = position
        self.refresh_rate = 5
        self.refresh_counter = 0
        self.speed = 11.5
        self.gravity = 0.6
        self.is_jumping = False
        self.is_ducking = False
        self.is_dead = False
        self.movement = [0, 0]

    def draw(self, screen):
        """把恐龙画到屏幕上"""
        screen.blit(self.image, self.rect)

    def update(self):
        """更新恐龙位置"""
        # 判断是否死亡，如果恐龙死亡，加载不低头状态最后一张图片
        if self.is_dead:
            self.image_idx = 4
            self.load_image()
            return
        # 判断是否跳跃
        if self.is_jumping:
            self.movement[1] += self.gravity  # movement = (0,0) gravity = 0.6
            # 恐龙在空中的时候，图片切换成不低头状态第一张图片
            self.image_idx = 0
            self.load_image()
            self.rect = self.rect.move(self.movement)
            if self.rect.bottom >= self.init_position[1]:
                # ？？？？
                # 如果恐龙落地，is_jumping为false
                self.rect.bottom = self.init_position[1]
                self.is_jumping = False
        # 判断是否低头
        elif self.is_ducking:
            if self.refresh_counter % self.refresh_rate == 0:
                # 每到一个5的整数
                self.refresh_counter = 0
                self.image_idx = 5 if self.image_idx == 6 else 6
                self.load_image()
        else:
            if self.refresh_counter % self.refresh_rate == 0:
                self.refresh_counter = 0
                if self.image_idx == 1:
                    self.image_idx = 2
                elif self.image_idx == 2:
                    self.image_idx = 3
                else:
                    self.image_idx = 1
                self.load_image()

        self.refresh_counter += 1

    def load_image(self):
        """载入当前状态图片
        四种状态
        """
        '''
        for i in range(len(self.images)):
            self.image = self.images[i]
            self.rect = self.image.get_rect()
            self.rect.left,self.rect.bottom = self.position
            self.mask = pygame.mask.from_surface(self.image)
            self.draw()
        '''
        self.image = self.images[self.image_idx]
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)

    def unduck(self):
        """不低头"""
        self.is_ducking = False

    def jump(self, sounds):
        """
        跳跃
        每跳一次发出声音
        """
        if self.is_dead or self.is_jumping or self.is_ducking:
            return
        sounds['jump'].play()
        self.is_jumping = True
        self.movement[1] = -1 * self.speed

    def duck(self):
        """
        判断恐龙是否低头
        """
        if self.is_jumping or self.is_dead:
            return
        self.is_ducking = True

    def die(self, sounds):
        """死亡
        死亡时发出提示音
        """
        if self.is_dead:
            return
        sounds['die'].play()
        self.is_dead = True


class Cfg():
    """配置类
    属性：屏幕大小，背景颜色，FPS，图片加载路径，音乐加载路径

    """

    def __init__(self):
        self.screen_size = (600, 150)
        self.bg_color = (235, 235, 235)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.fps = 60
        # 地面，飞龙，仙人掌移动速度
        self.speed = -6

        # 音频素材路径
        # os.path.join连接路径名 ,os.getcwd()返回当前路径
        self.audio_paths = {'die': os.path.join(os.getcwd(), 'audios/die.wav'),
                            'jump': os.path.join(os.getcwd(), 'audios/jump.wav'),
                            'point': os.path.join(os.getcwd(), 'audios/point.wav')}

        # 子弹宽度高度颜色
        self.bullet_width = 10
        self.bullet_height = 2
        self.bullet_color = (60, 60, 60)


class Bullet(Sprite):
    """子弹类"""

    def __init__(self, cfg, dino, screen):
        super(Bullet, self).__init__()
        """定义子弹矩形，定义速度
        子弹rect.height = 恐龙rect.height
        子弹rect.left = 恐龙rect.right
        """
        self.cfg = cfg
        self.rect = pygame.Rect(0, 0, cfg.bullet_width, cfg.bullet_height)
        self.rect.centery = dino.rect.centery
        self.rect.left = dino.rect.right
        self.speed = 50

    def update(self, screen):
        """更新子弹位置
        当子弹飞出屏幕边缘，删除子弹
        """
        screen_rect = screen.get_rect()
        self.rect = self.rect.move([self.speed, screen_rect.x])

        if self.rect.x > screen_rect.x:
            self.kill()

    def draw(self, screen):
        """把子弹画到屏幕上"""
        pygame.draw.rect(screen, self.cfg.bullet_color, self.rect)


'''
class HeartBonus(Sprite):
    """心形bonus
    在空中随机产生bonus矩形
    碰撞检测
    如果恐龙和bonus矩形发生碰撞，恐龙life +1
    """
    def __init__(self):
    super(HeartBonus,self).__init__()
    pass
        

    def update(self):
        pass

    def draw(self):
        pass
'''


def game_end_interface(screen, cfg):
    """游戏结束界面"""

    """
    当恐龙碰撞到飞龙，游戏结束，显示replay按钮
    并把最高分和当前分显示在结束界面上
    最高分不会清零

    玩家按方向上键 或者鼠标点击replay按钮，游戏重新开始
    """
    # 把replay 和 gameover 图像rect放在屏幕居中位置
    # gameover图像 在reply图像上方
    replay_image = pygame.image.load('images/replay.png')
    replay_image = pygame.transform.scale(replay_image, (35, 31))
    replay_image_rect = replay_image.get_rect()
    replay_image_rect.centerx = cfg.screen_size[0] / 2
    replay_image_rect.top = cfg.screen_size[1] * 0.52
    game_over_image = pygame.image.load('images/gameover.png')
    game_over_image = pygame.transform.scale(game_over_image, (190, 11))
    game_over_image_rect = game_over_image.get_rect()
    game_over_image_rect.centerx = cfg.screen_size[0] / 2
    game_over_image_rect.top = cfg.screen_size[1] * 0.35
    clock = pygame.time.Clock()

    # 键盘监听
    # 玩家退出游戏
    # 按上建，游戏继续
    # 鼠标点击，游戏继续
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if replay_image_rect.collidepoint(mouse_pos):
                    return True
        screen.blit(replay_image, replay_image_rect)
        screen.blit(game_over_image, game_over_image_rect)
        pygame.display.update()
        clock.tick(cfg.fps)


def game_start_interface(screen, sounds, cfg):
    """游戏开始界面"""
    dino = Dinosaur('images/dino.png')
    ground = pygame.image.load('images/ground.png').subsurface((0, 0), (83, 19))
    rect = ground.get_rect()
    rect.left, rect.bottom = cfg.screen_size[0] / 20, cfg.screen_size[1]
    clock = pygame.time.Clock()
    press_flag = False
    """
    玩家点击quit游戏结束
    玩家按方向键上键开始,press_flag变为true,并发出jump的声音
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    press_flag = True
                    dino.jump(sounds)

        dino.update()
        screen.fill(cfg.bg_color)
        screen.blit(ground, rect)
        dino.draw(screen)
        pygame.display.update()
        clock.tick(cfg.fps)
        if (not dino.is_jumping) and press_flag:
            return True


def main(highest_score):
    """游戏主循环"""
    cfg = Cfg()
    screen = pygame.display.set_mode(cfg.screen_size)
    ground = Ground(cfg)
    pygame.init()
    pygame.display.set_caption("小恐龙")
    # 音频文件
    sounds = {}
    for key, value in cfg.audio_paths.items():
        # pygame mixer.Sound创建音频对象
        sounds[key] = pygame.mixer.Sound(value)
    game_start_interface(screen, sounds, cfg)
    # 小恐龙
    dino = Dinosaur(cfg)
    # 子弹
    bullet = Bullet(cfg, dino, screen)
    # 子弹编组
    bullet_group = Group()
    # 仙人掌编组
    cac_group = Group()
    # 飞龙编组
    ptera_group = Group()
    # 云朵编组
    cloud_group = Group()
    # 设置游戏FPS
    clock = pygame.time.Clock()
    # 添加障碍物时间
    add_obstacle_timer = 0
    # 记分
    score_timer = 0
    score = 0
    highest_score = highest_score
    score_board = Scoreboard(position=(534, 15), bg_color=cfg.bg_color)
    highest_score_board = Scoreboard(position=(435, 15), bg_color=cfg.bg_color, is_highest=True)
    while True:
        '''
                    up 按下 恐龙跳跃

                    down 按下 恐龙低头
                    down 松开 恐龙不低头

                    space 按下 发射子弹

                    松开 : KEYUP
                    按下: KEYDOWN
                    KEYDOWN 和 KEYUP 就是PUBG里的保持和切换
        '''


        # 键盘监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    dino.jump(sounds)

                elif event.key == pygame.K_SPACE:
                    bullet_group.add(bullet)
                elif event.key == pygame.K_DOWN:
                    dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.unduck()

        # 随机产生云朵，如果云朵group的个数小于5，在 group里添加一朵新云朵
        if len(cloud_group) < 5 and random.randrange(0, 300) == 10:
            cloud_group.add(Cloud(cfg))
        add_obstacle_timer += 1
        if add_obstacle_timer > random.randrange(50, 150):
            add_obstacle_timer = 0
            # 随机产生仙人掌和飞龙
            random_value = random.randrange(0, 10)
            if 5 <= random_value < 7:
                cac_group.add(Cactus(cfg))
            else:
                ptera_group.add(Ptera(cfg))

        # 更新子弹
        bullet_group.update(screen)
        # 更新地面
        ground.update()
        # 恐龙
        dino.update()
        # 更新云朵
        cloud_group.update()
        # 更新仙人掌编组
        cac_group.update()
        # 更新飞龙编组
        ptera_group.update()
        # 更新云编组
        cloud_group.update()

        # 碰撞检测
        # 恐龙 和 仙人掌 或者 飞鸟的精灵编组相撞，游戏结束，死亡提示音
        for item in cac_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)

        for item in ptera_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)

        score_timer += 1
        # // 取最小整数 当像素每往前移动5格时，分数加一分
        # 当前分数大于最高分，把最高分替换为当前分数
        # 分数每满一百分，发出提示音
        # 游戏分数每满1000分，提高游戏速度
        if score_timer > (cfg.fps // 12):
            score_timer = 0
            score += 1
            score = min(score, 99999)
            if score > highest_score:
                highest_score = score
            if score % 100 == 0:
                sounds['point'].play()
            if score % 1000 == 0:
                for item in cloud_group:
                    item.speed -= 1
                for item in cac_group:
                    item.speed -= 1
                for item in ptera_group:
                    item.speed -= 1

        screen.fill(cfg.bg_color)

        ground.draw(screen)

        dino.draw(screen)

        cloud_group.draw(screen)


        bullet_group.draw(screen)

        # Sprite自带draw方法,对每一个精灵调用blit方法。Sprite的1update方法被重写
        cac_group.draw(screen)

        ptera_group.draw(screen)

        cloud_group.draw(screen)
        score_board.set_score(score)
        highest_score_board.set_score(highest_score)
        score_board.draw(screen)
        highest_score_board.draw(screen)

        pygame.display.update()
        clock.tick(cfg.fps)
        if dino.is_dead:
            break

    return game_end_interface(screen, cfg), highest_score


if __name__ == "__main__":
    highest_score = 0
    while True:
        flag, highest_score = main(highest_score)
        if not flag:
            break
