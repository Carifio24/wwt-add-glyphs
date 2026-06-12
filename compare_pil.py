from PIL import Image, ImageChops, ImageEnhance

# Load images
img1 = Image.open("glyphs1.png")
img2 = Image.open("glyphs2.png")

diff = ImageChops.difference(img1, img2)
# enhancer = ImageEnhance.Brightness(diff)
# diff = enhancer.enhance(3)
diff.save("diff_result.png")
