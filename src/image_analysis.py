"""Image preprocessing helpers for the CIFAR-10 study.

All image arrays use uint8 RGB with shape (n, height, width, 3).
"""
from __future__ import annotations

import cv2
import hashlib
import numpy as np
from PIL import Image, ImageEnhance

RANDOM_SEED = 42


def phash64(image: np.ndarray) -> int:
    """Compute a 64-bit perceptual hash using the low-frequency 2-D DCT."""
    rgb = np.asarray(image, dtype=np.uint8)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY) if rgb.ndim == 3 else rgb
    resized = cv2.resize(gray, (32, 32), interpolation=cv2.INTER_AREA).astype(np.float32)
    dct = cv2.dct(resized)
    low = dct[:8, :8].reshape(-1)
    median = np.median(low[1:])
    bits = low > median
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value


def compute_phashes(images: np.ndarray, progress_every: int = 10_000) -> np.ndarray:
    """Compute hashes for all images; stores only 64-bit integers."""
    hashes = np.empty(len(images), dtype=np.uint64)
    for idx, image in enumerate(images):
        hashes[idx] = phash64(image)
        if progress_every and (idx + 1) % progress_every == 0:
            print(f"Đã tính pHash: {idx + 1:,}/{len(images):,}")
    return hashes


def hamming_distance(hash_a: int, hash_b: int) -> int:
    return int(int(hash_a) ^ int(hash_b)).bit_count()


def exact_duplicate_groups(images: np.ndarray) -> list[list[int]]:
    """Return groups of byte-identical images using a SHA-256 pixel digest.

    A perceptual-hash collision does not prove two images are identical. Therefore
    pHash matches are reported separately and only genuinely identical pixel
    arrays are eligible for automatic removal.
    """
    buckets: dict[bytes, list[int]] = {}
    for idx, image in enumerate(images):
        contiguous = np.ascontiguousarray(image)
        digest = hashlib.sha256(contiguous.tobytes()).digest()
        buckets.setdefault(digest, []).append(idx)
    return [indices for indices in buckets.values() if len(indices) > 1]


def phash_collision_groups(hashes: np.ndarray) -> list[list[int]]:
    """Return groups sharing the same 64-bit pHash (candidate matches only)."""
    buckets: dict[int, list[int]] = {}
    for idx, value in enumerate(hashes):
        buckets.setdefault(int(value), []).append(idx)
    return [indices for indices in buckets.values() if len(indices) > 1]


def near_duplicate_pairs(
    hashes: np.ndarray,
    max_images: int = 5_000,
    max_hamming: int = 3,
    random_state: int = RANDOM_SEED,
) -> list[tuple[int, int, int]]:
    """Find near-duplicate candidates within a deterministic subset.

    Hamming distance is measured on the 64-bit pHash. The subset cap avoids the
    quadratic memory cost of comparing all 50,000 CIFAR-10 training images at once.
    Exact pixel-identical copies are separately verified on the full training split.
    """
    from sklearn.neighbors import NearestNeighbors

    n = min(len(hashes), max_images)
    rng = np.random.default_rng(random_state)
    chosen = np.sort(rng.choice(len(hashes), size=n, replace=False)) if len(hashes) > n else np.arange(n)
    binary = np.zeros((n, 64), dtype=np.uint8)
    for row, original_idx in enumerate(chosen):
        value = int(hashes[original_idx])
        binary[row] = [(value >> bit) & 1 for bit in range(63, -1, -1)]

    nn = NearestNeighbors(metric="hamming", algorithm="brute", n_jobs=-1, radius=max_hamming / 64)
    nn.fit(binary)
    neighborhoods = nn.radius_neighbors(return_distance=False)
    pairs = []
    for local_i, neighbors in enumerate(neighborhoods):
        for local_j in neighbors:
            if local_j <= local_i:
                continue
            dist = int(np.count_nonzero(binary[local_i] != binary[local_j]))
            if 0 < dist <= max_hamming:
                pairs.append((int(chosen[local_i]), int(chosen[local_j]), dist))
    return pairs


def remove_exact_duplicate_indices(groups: list[list[int]]) -> list[int]:
    """Keep the first member of each exact-hash group; return indices to remove."""
    remove = []
    for group in groups:
        remove.extend(group[1:])
    return sorted(set(remove))


def resize_and_reconstruct(image: np.ndarray, target_size: int) -> np.ndarray:
    """Resize to target_size then return to original 32x32 for fair metric comparison."""
    interpolation = cv2.INTER_AREA if target_size < image.shape[0] else cv2.INTER_CUBIC
    resized = cv2.resize(image, (target_size, target_size), interpolation=interpolation)
    back = cv2.resize(resized, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)
    return back


def augment_image(image: np.ndarray, method: str, rng: np.random.Generator | None = None) -> np.ndarray:
    """Apply one deterministic-by-seed augmentation and return uint8 RGB."""
    rng = rng or np.random.default_rng(RANDOM_SEED)
    image = np.asarray(image, dtype=np.uint8)
    if method == "horizontal_flip":
        output = np.fliplr(image)
    elif method == "vertical_flip":
        output = np.flipud(image)
    elif method == "rotate_15":
        h, w = image.shape[:2]
        matrix = cv2.getRotationMatrix2D((w / 2, h / 2), 15, 1.0)
        output = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    elif method == "random_crop":
        h, w = image.shape[:2]
        pad = 4
        padded = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REFLECT_101)
        top = int(rng.integers(0, 2 * pad + 1))
        left = int(rng.integers(0, 2 * pad + 1))
        output = cv2.resize(padded[top:top + h, left:left + w], (w, h), interpolation=cv2.INTER_AREA)
    elif method == "gaussian_noise":
        noise = rng.normal(0, 10, size=image.shape)
        output = np.clip(image.astype(np.float32) + noise, 0, 255)
    elif method == "brightness_contrast":
        output = ImageEnhance.Contrast(Image.fromarray(image)).enhance(1.2)
        output = ImageEnhance.Brightness(output).enhance(1.1)
        output = np.asarray(output)
    else:
        raise ValueError(f"Augmentation không hỗ trợ: {method}")
    return np.ascontiguousarray(np.clip(output, 0, 255).astype(np.uint8))


def convert_color_space(images: np.ndarray, color_space: str) -> np.ndarray:
    """Convert RGB batch to RGB, grayscale, HSV or CIELAB arrays."""
    if color_space == "RGB":
        return images.copy()
    outputs = []
    for image in images:
        if color_space == "Grayscale":
            converted = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)[..., None]
        elif color_space == "HSV":
            converted = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        elif color_space == "LAB":
            converted = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        else:
            raise ValueError(f"Không gian màu không hỗ trợ: {color_space}")
        outputs.append(converted)
    return np.stack(outputs)


def edge_map(image: np.ndarray, method: str, setting: str) -> np.ndarray:
    """Apply Sobel, Prewitt or Canny with two predefined parameter sets."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if method == "Sobel":
        ksize = 3 if setting == "A" else 5
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=ksize)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=ksize)
        magnitude = cv2.magnitude(gx, gy)
        threshold = np.percentile(magnitude, 85 if setting == "A" else 75)
        return (magnitude >= threshold).astype(np.uint8)
    if method == "Prewitt":
        if setting == "A":
            kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
            ky = kx.T
        else:
            base = np.array([-1, 0, 1], dtype=np.float32)
            kx = np.tile(base, (5, 1))
            ky = kx.T
        gx = cv2.filter2D(gray.astype(np.float32), -1, kx)
        gy = cv2.filter2D(gray.astype(np.float32), -1, ky)
        magnitude = cv2.magnitude(gx, gy)
        threshold = np.percentile(magnitude, 85 if setting == "A" else 75)
        return (magnitude >= threshold).astype(np.uint8)
    if method == "Canny":
        low, high = (50, 150) if setting == "A" else (100, 200)
        return (cv2.Canny(gray, low, high) > 0).astype(np.uint8)
    raise ValueError(f"Edge detector không hỗ trợ: {method}")

