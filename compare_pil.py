from PIL import Image, ImageChops

# Load images
img1 = Image.open("glyphs1.png")
img2 = Image.open("glyphs2.png")

diff = ImageChops.difference(img1, img2)
diff.save("diff_result.png")
