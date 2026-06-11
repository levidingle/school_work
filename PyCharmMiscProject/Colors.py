for i in range(256):
    print(f"\033[38;5;{i}mColor {i:3}\033[0m", end="  ")
    if (i + 1) % 8 == 0:
        print()