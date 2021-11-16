import os
import sys
import numpy
import math
import blend_modes
from PIL import Image

output_folder = r"E:/05 - SmokeTest/render"
diffuse_folder = r"E:/05 - SmokeTest/render/particle_02/diffuse/"
neg_folder = r"E:/05 - SmokeTest/render/particle_02/normal_neg/"
pos_folder = r"E:/05 - SmokeTest/render/particle_02/normal_pos/"

atlas_size_x = 4096
atlas_size_y = 4096

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

diffuse_files = os.listdir(diffuse_folder)
neg_files = os.listdir(neg_folder)
pos_files = os.listdir(pos_folder)

atlas_normal = Image.new("RGB", (atlas_size_x, atlas_size_y), (127, 127, 255))
atlas_diffuse = Image.new("RGBA", (atlas_size_x, atlas_size_y), (255, 255, 255, 0))

### setup toolbar
toolbar_width = len(diffuse_files)
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['
###

for i in range(0, len(diffuse_files)):

    diffuse_path = os.path.join(diffuse_folder, diffuse_files[i])
    path_neg = os.path.join(neg_folder, neg_files[i])
    path_pos = os.path.join(pos_folder, pos_files[i])

    diffuse = Image.open(diffuse_path)

    im_neg = Image.open(path_neg)
    R_neg, G_neg, B_neg, A_neg = im_neg.split()

    im_pos = Image.open(path_pos)
    R_pos, G_pos, B_pos, A_pos = im_pos.split()

    white = Image.new("L", diffuse.size, 255)
    grey = Image.new("L", diffuse.size, 127)

    # negative normals shift
    R_neg = list(R_neg.getdata())
    R_neg = [(255 - x) / 2 for x in R_neg]
    R_neg_shifted = Image.new("L", diffuse.size)
    R_neg_shifted.putdata(R_neg)

    G_neg = list(G_neg.getdata())
    G_neg = [(255 - x) / 2 for x in G_neg]
    G_neg_shifted = Image.new("L", diffuse.size)
    G_neg_shifted.putdata(G_neg)

    RG_neg_shifted = Image.merge("RGBA", [R_neg_shifted, G_neg_shifted, grey, white])

    # positive normals shift
    R_pos = list(R_pos.getdata())
    R_pos = [x / 2 + 127 for x in R_pos]
    R_pos_shifted = Image.new("L", diffuse.size)
    R_pos_shifted.putdata(R_pos)

    G_pos = list(G_pos.getdata())
    G_pos = [x / 2 + 127 for x in G_pos]
    G_pos_shifted = Image.new("L", diffuse.size)
    G_pos_shifted.putdata(G_pos)

    RG_pos_shifted = Image.merge("RGBA", [R_pos_shifted, G_pos_shifted, grey, white])

    bg = numpy.array(RG_neg_shifted)
    bg_float = bg.astype(float)

    fg = numpy.array(RG_pos_shifted)
    fg_float = fg.astype(float)

    blended_float = blend_modes.overlay(bg_float, fg_float, 1)
    blended = numpy.uint8(blended_float)
    blended_img = Image.fromarray(blended)

    R_dif, G_dif, B_dif, A_dif = diffuse.split()
    R, G, B, A = blended_img.split()

    normal_img = Image.merge("RGBA", [R, G, white, A_dif])
    normal_base = Image.new("RGBA", diffuse.size, (127, 127, 255, 255))
    img = Image.alpha_composite(normal_base, normal_img)

    k = int(math.sqrt(len(diffuse_files)))
    atlas_normal.paste(img, (img.size[0] * (i % k), img.size[1] * (i // k)))
    atlas_diffuse.paste(diffuse, (diffuse.size[0] * (i % k), diffuse.size[1] * (i // k)))

    # process toolbar update
    sys.stdout.write("-")
    sys.stdout.flush()

    if i == 0:
        blended_img.save(os.path.join(output_folder, 'test.png'), format='PNG')

sys.stdout.write("]\n")
atlas_normal.save(os.path.join(output_folder, 'atlas_normal.png'), format='PNG')
atlas_diffuse.save(os.path.join(output_folder, 'atlas_diffuse.png'), format='PNG')
