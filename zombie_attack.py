import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import zombie_attack.game
    zombie_attack.game.ZombieAttackGame().run()
