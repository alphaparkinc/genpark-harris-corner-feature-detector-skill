"""Harris Corner Detection Engine
100% Python Standard Library.
"""

class HarrisCornerDetector:
    """Autocorrelation matrix corner response calculator."""
    def __init__(self, k=0.04, threshold=1e4):
        self.k = k
        self.threshold = threshold

    def detect_corners(self, image):
        h, w = len(image), len(image[0])
        ix = [[0.0 for _ in range(w)] for _ in range(h)]
        iy = [[0.0 for _ in range(w)] for _ in range(h)]
        for y in range(h):
            for x in range(w):
                ix[y][x] = (image[y][min(x + 1, w - 1)] - image[y][max(x - 1, 0)]) / 2.0
                iy[y][x] = (image[min(y + 1, h - 1)][x] - image[max(y - 1, 0)][x]) / 2.0

        ix2 = [[ix[y][x] ** 2 for x in range(w)] for y in range(h)]
        iy2 = [[iy[y][x] ** 2 for x in range(w)] for y in range(h)]
        ixiy = [[ix[y][x] * iy[y][x] for x in range(w)] for y in range(h)]

        corners = []
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                s_ix2 = sum(ix2[y+dy][x+dx] for dy in [-1,0,1] for dx in [-1,0,1])
                s_iy2 = sum(iy2[y+dy][x+dx] for dy in [-1,0,1] for dx in [-1,0,1])
                s_ixiy = sum(ixiy[y+dy][x+dx] for dy in [-1,0,1] for dx in [-1,0,1])

                det_m = s_ix2 * s_iy2 - s_ixiy * s_ixiy
                trace_m = s_ix2 + s_iy2
                r = det_m - self.k * (trace_m ** 2)
                if r > self.threshold:
                    corners.append({"x": x, "y": y, "response": round(r, 2)})

        return {
            "total_corners": len(corners),
            "corners": corners[:15]
        }
