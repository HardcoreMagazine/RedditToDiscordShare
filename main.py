if __name__ == '__main__':
    if input('Type "1" if you want to run bot in legacy mode: ') == '1':
        import LegacyBotController # contains executable script
    else:
        import LatestBotController # contains executable script
