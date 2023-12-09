import pygame

pygame.init()
pygame.mixer.init()

try:
    sound = pygame.mixer.Sound("D:\\git\\GameHelper\\package\\genshin\\audio\\challenging_finished.wav")
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))  # 等待音频播放完毕
except pygame.error as e:
    print(f"Error playing sound: {e}")
