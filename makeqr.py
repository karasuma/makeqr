import sys, pyqrcode, cv2, os, time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Literal, Tuple, List

def create_qrcode(
        contents: List[str],
        title: str = '',
        errlevel: Literal['L', 'M', 'Q', 'H'] = 'L',
        version: int = 0,
        qr_row: int = 5,
        pixel_scale: int = 3,
        foreground: List[int] = [0, 0, 0],
        background: List[int] = [255, 255, 255],
        preview: bool = True
        ) -> None:
    # Abort if contents has no valid text
    if not [a for a in contents if a]:
        print('0 content QRified.')
        return
    # Get the maximum version of QR code from the longest content of contents
    for longest_content in [c for c in contents if len(c) == max([len(cl) for cl in contents])]:
        sample_qr = pyqrcode.create(longest_content, error=errlevel, mode='binary')
        version = max(version, sample_qr.version)
    # Make output directory and clear previous images
    temp_dir = './output_qr'
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    for img in [p for p in Path(temp_dir).iterdir() if p.is_file()]:
        img.unlink()
    # Create QR codes
    foreground[0], foreground[2] = foreground[2], foreground[0]
    background[0], background[2] = background[2], background[0]
    imgarray: List[List[str]] = [[]]
    for idx, content in enumerate(list(set(contents))):
        if(idx > 0 and idx % qr_row == 0):
            imgarray.append([])
        print(content+' ... ', end='', flush=True)
        if 1 <= version and version <= 40:
            qrcode = pyqrcode.create(content, error=errlevel, version=version, mode='binary')
        else:
            qrcode = pyqrcode.create(content, error=errlevel, mode='binary')
        qrcode.png(f'{temp_dir}/{idx+1}.png', scale=max(1, pixel_scale), module_color=foreground, background=background)
        imgarray[int(idx / qr_row)].append(f'{temp_dir}/{idx+1}.png')
        print('Done.', flush=True)
    print(f'{len(list(set(contents)))} contents QRified.')
    print('image concatinating...', end='', flush=True)
    # Tiling
    max_cols = max(len(row) for row in imgarray)
    sample_img = cv2.imread(imgarray[0][0])
    h, w = sample_img.shape[:2]
    c = sample_img.shape[2] if len(sample_img.shape) == 3 else 1
    bg_color = background[:c]
    blank = np.full((h, w, c), bg_color, dtype=sample_img.dtype)
    im_v = cv2.vconcat([
        cv2.hconcat([
            cv2.imread(path) if path else blank
            for path in row + [None] * (max_cols - len(row))
        ])
        for row in imgarray
    ])
    # Header
    image_name = 'concatinated'
    if title:
        title_font = cv2.FONT_HERSHEY_SIMPLEX
        title_height = 60
        img_h, img_w = im_v.shape[:2]
        font_scale = 1.0
        thickness = 2
        (text_w, text_h), _ = cv2.getTextSize(title, title_font, font_scale, thickness)
        title_img = np.full((title_height, img_w, 3), background, dtype=im_v.dtype) 
        cv2.putText(
            title_img, title,
            ((img_w - text_w) // 2, (title_height + text_h) // 2),
            title_font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA
        )
        im_v = cv2.vconcat([title_img, im_v])
        image_name = title
    image_path = f'{temp_dir}/{image_name}.png'
    cv2.imwrite(image_path, im_v)
    time.sleep(0.1)
    if preview:
        plt.imshow(cv2.cvtColor(im_v, cv2.COLOR_BGR2RGB))
        plt.show()
    print('Generation completed.')

def main():
    row = 5
    scale = 3
    title = ''
    contents = [a for a in sys.argv][1:]
    for arg in sys.argv:
        if '--row=' in arg.lower():
            try:
                row = int(arg.lower().replace('--row=', ''))
                contents.remove(arg)
            except:
                print(arg + ' is not number.')
        if '--scale=' in arg.lower():
            try:
                scale = int(arg.lower().replace('--scale=', ''))
                contents.remove(arg)
            except:
                print(arg + ' is not number.')
        if '--title=' in arg.lower():
            title = arg[len('--title='):]
            contents.remove(arg)
    create_qrcode(contents, title=title, qr_row=row, pixel_scale=scale)

if __name__ == '__main__':
    main()

