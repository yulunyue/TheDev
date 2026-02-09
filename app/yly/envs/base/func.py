import time


def loop():
    arr = []
    for _ in range(100000):
        arr.extend([0] * 1000)
        time.sleep(0.1)
        print(f"len(arr) = {len(arr)}")


if __name__ == "__main__":
    pass
