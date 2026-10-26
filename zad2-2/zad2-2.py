#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import numpy as np
from pathlib import Path


def load_dem(file_path):
    with open(file_path, "r") as dem_file:
        width, height, distance_cm = map(int, dem_file.readline().split())
        elevations = np.loadtxt(dem_file)

    expected_shape = (height, width)
    if elevations.shape != expected_shape:
        raise ValueError(
            "Nieprawidłowy rozmiar macierzy: "
            f"oczekiwano {expected_shape}, otrzymano {elevations.shape}"
        )

    return width, height, distance_cm, elevations

def count_colors(normalized_elevation):
    if normalized_elevation < 0.5:
        return (2 * normalized_elevation, 1, 0)
    else:
        return (1, 1 - 2 * (normalized_elevation - 0.5), 0)


def apply_sun_lighting(colors, elevations, distance_cm):
    sample_distance = distance_cm / 100
    padded_elevations = np.pad(elevations, 1, mode="edge")
    elevation_right = padded_elevations[1:-1, 2:]
    elevation_down = padded_elevations[2:, 1:-1]

    vector_x = np.stack(
        (np.full_like(elevations, sample_distance),
         np.zeros_like(elevations),
         elevation_right - elevations),
        axis=-1,
    )
    vector_y = np.stack(
        (np.zeros_like(elevations),
         np.full_like(elevations, sample_distance),
         elevation_down - elevations),
        axis=-1,
    )
    normals = np.cross(vector_x, vector_y)
    normals /= np.linalg.norm(normals, axis=-1, keepdims=True)

    sun_vector = np.array([0.6, -0.8, 1.2])
    sun_vector /= np.linalg.norm(sun_vector)
    illumination = np.clip(np.sum(normals * sun_vector, axis=-1), 0, 1)

    hsv_colors = rgb_to_hsv(colors)
    hsv_colors[..., 2] *= 0.55 + 0.9 * illumination
    hsv_colors[..., 2] = np.clip(hsv_colors[..., 2], 0, 1)
    return hsv_to_rgb(hsv_colors)

def create_color_map(elevations, output_path, distance_cm):
    minimum = np.min(elevations)
    maximum = np.max(elevations)
    normalized_elevations = (elevations - minimum) / (maximum - minimum)
    colors = np.array([
        [count_colors(value) for value in row]
        for row in normalized_elevations
    ])

    figure, axis = plt.subplots(figsize=(10, 8))
    colors = apply_sun_lighting(colors, elevations, distance_cm)
    image = axis.imshow(colors, origin="lower")

    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    dem_path = Path(__file__).with_name("big.dem")
    color_map_path = dem_path.with_name("mapa-wysokosci.png")
    width, height, distance_cm, elevations = load_dem(dem_path)

    print(f"Szerokość mapy: {width} punktów")
    print(f"Wysokość mapy: {height} punktów")
    print(f"Odległość między punktami: {distance_cm} cm")
    print("Macierz wysokości:")
    print(elevations)
    print(f"Maksymalna wysokość: {np.max(elevations):.6f} m")
    create_color_map(elevations, color_map_path, distance_cm)
    print(f"Kolorowa mapa została zapisana w pliku: {color_map_path}")
