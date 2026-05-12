from matplotlib.testing.compare import compare_images

result = compare_images(
    expected="glyphs1.png",
    actual="glyphs2.png",
    tol=1.6,
)

print(result)
