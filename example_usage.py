from client import HarrisCornerDetector

def main():
    detector = HarrisCornerDetector(k=0.04, threshold=100.0)
    img = [[0.0]*10 for _ in range(10)]
    for y in range(3, 7):
        for x in range(3, 7):
            img[y][x] = 200.0
    res = detector.detect_corners(img)
    print("Harris Corner Detection Verification:")
    print(f"Corners Detected: {res['total_corners']}")
    for c in res['corners'][:3]:
        print(f"  Point: ({c['x']}, {c['y']}) -> Score: {c['response']}")

if __name__ == "__main__":
    main()
