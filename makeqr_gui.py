import flet as ft
from makeqr import create_qrcode
from typing import List, Tuple
import datetime, random, os, time, base64

def container(page: ft.Page):
    qr_texts: List[List[str, str]] = []
    txtfield_col = ft.Column()
    savefile = 'save.txt'

    def mkhash():
        unixtime = int(datetime.datetime.timestamp(datetime.datetime.now()))
        rnd1, rnd2 = random.random(), random.random()
        return f'{unixtime}-{rnd1}-{rnd2}'
    
    def init():
        if os.path.exists(savefile):
            with open(savefile, 'r') as f:
                for line in f.readlines():
                    qr_texts.append([mkhash(), line.strip()])
    init()

    def add_text():
        qr_texts.append([mkhash(), ''])
        update_textfields()

    def change_text(id: str, e):
        for item in [t for t in qr_texts if t[0] == id]:
            item[1] = e.control.value

    def remove_text(id: str):
        for item in [t for t in qr_texts if t[0] == id]:
            qr_texts.remove(item)
        update_textfields()

    def append_textfield(idx: int, id: str, v: str):
        return ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINED,
                    icon_color=ft.Colors.PINK_700,
                    icon_size=40,
                    tooltip='DELETE',
                    on_click=lambda e: remove_text(id),
                ),
                ft.TextField(
                    label=f'No. {idx + 1}',
                    value=[v[1] for v in qr_texts if v[0] == id][0],
                    expand=True,
                    multiline=True,
                    min_lines=1,
                    on_change=lambda e: change_text(id, e)
                )
            ], expand=True
        )

    def update_textfields():
        txtfield_col.controls.clear()
        txtfield_col.controls.extend([append_textfield(idx, a[0], a[1]) for idx, a in enumerate(qr_texts)])
        page.update()
    
    def save_texts():
        try:
            with open(savefile, 'w') as f:
                f.write('\n'.join([r[1] for r in qr_texts]))
            page.open(ft.SnackBar(ft.Text(f"{len(qr_texts)} text{'' if len(qr_texts) == 1 else 's'} Saved.")))
        except Exception as e:
            page.open(ft.SnackBar(ft.Text(f"Error: {str(e)}")))
        finally:
            page.update()

    # Initialize
    update_textfields()
    loading_overlay = ft.Container(
        content=ft.Column([ft.ProgressRing(), ft.Text('Generating...', size=20)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.BLACK54,
        alignment=ft.alignment.center,
        visible=False,
        expand=True
    )
    qr_col = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    def generate_qr():
        loading_overlay.visible = True
        page.update()
        try:
            create_qrcode([v[1] for v in qr_texts if v[1]], preview=False)
            qr_col.controls.clear()
            output_img = f'./output_qr/concatinated.png'
            if os.path.exists(output_img):
                with open(output_img, 'rb') as f:
                    out_b64 = base64.b64encode(f.read()).decode()
                gen_image = ft.Image(src_base64=out_b64)
                qr_col.controls.append(gen_image)
        finally:
            loading_overlay.visible = False
            page.update()
    gen_button = ft.OutlinedButton(
            'GENERATE QR CODES',
            on_click=lambda e: generate_qr()
    )
    save_button = ft.OutlinedButton(
        'SAVE STRINGS',
        on_click=lambda e: save_texts()
    )
    button_controls = ft.Row([
        gen_button,
        save_button
    ], expand=True, alignment=ft.MainAxisAlignment.CENTER)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.Stack([
            ft.Column([
                txtfield_col,
                ft.IconButton(
                    icon=ft.Icons.ADD_BOX_OUTLINED,
                    icon_color=ft.Colors.GREEN_500,
                    icon_size=40,
                    tooltip='Add new content',
                    on_click=lambda e: add_text()
                ),
                button_controls,
                qr_col
            ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.HIDDEN
            ),
            loading_overlay
        ], expand=True)
    )

try:
    ft.app(container)
except:
    pass
