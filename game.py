from scenes import MainScene, GameOverScene


class Game:
    class Scenes:
        main = MainScene
        gameover = GameOverScene

    def start(self):
        self.Scenes.main(self).start()