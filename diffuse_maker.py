from PIL import Image
import os
import sys

diffuse_folder = r"E:/05 - SmokeTest/render/particle_02/diffuse/"
neg_folder = r"E:/05 - SmokeTest/render/particle_02/normal_neg/"

if not os.path.exists(diffuse_folder):
    os.makedirs(diffuse_folder)

neg_files = os.listdir(neg_folder)

### setup toolbar
toolbar_width = len(neg_files)
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['
###

for i in range(0, len(neg_files)):
    name = os.path.splitext(neg_files[i])[0]
    num = name[-3:]

    neg_path = os.path.join(neg_folder, neg_files[i])
    im_neg = Image.open(neg_path)
    R_neg, G_neg, B_neg, A_neg = im_neg.split()

    white = Image.new("L", im_neg.size, 255)

    diffuse = Image.merge("RGBA", [white, white, white, A_neg])
    diffuse.save(os.path.join(diffuse_folder, 'diffuse_' + num + ".png"), format='PNG')

    # process toolbar update
    sys.stdout.write("(" + str(i).zfill(2) + ")")
    sys.stdout.flush()

sys.stdout.write("]\n")
