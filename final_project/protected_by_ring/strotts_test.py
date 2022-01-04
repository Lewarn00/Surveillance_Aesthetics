from strotss import *

content_pil, style_pil = pil_loader('content.jpg'), pil_loader('scene_styles/1.jpg')
content_weight = 0.5 * 16.0
device = 'cuda:0'
start = time()
result = strotss(pil_resize_long_edge_to(content_pil, 512), pil_resize_long_edge_to(style_pil, 512), content_weight, device, "uniform")
result.save('generated_art/out_artwork1.png')