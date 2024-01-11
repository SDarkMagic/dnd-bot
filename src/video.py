from moviepy.editor import *
import pathlib
from sys import platform

class TurnClip:
    def __init__(self, name: str, gif=False) -> None:
        self.output_path = (pathlib.Path(__file__).parent.parent) / 'output' / f'{name.lower()}.{"gif" if gif else "mp4"}'
        if name.endswith("'s"):
            pass
        elif (name.endswith("s")):
            name += "'"
        else:
            name += "'s"
        self.v_padding = 13
        self.h_padding = 10
        self.raw_text = f"It's {name} turn"
        self.base_clip_path = (pathlib.Path(__file__).parent.parent) / 'templates' / 'turn.mp4'
        self.base_clip = VideoFileClip(str(self.base_clip_path.absolute()))
        self.text_clip = self._create_text_clip()
        return

    def _calc_text_area_size(self):
        height = (self.base_clip.h * 0.21) - (self.v_padding * 2)
        width = self.base_clip.w - (self.h_padding * 2)
        return (width, height)

    def _create_text_clip(self):
        available_fonts = TextClip.list('font')
        font = 'Impact'
        if ('Impact' not in available_fonts):
            font = 'Comic-Sans-MS' if platform == 'windows' else 'Arial'
        text_area = self._calc_text_area_size()
        clip = TextClip(self.raw_text, method='caption', size=text_area, font=font, color='black')
        return clip

    def composite(self, shadow_offset=10):
        self.text_clip = self.text_clip.set_position((self.h_padding, self.v_padding))
        output = str(self.output_path.absolute()) # Convert the pathlib object to an absolute path string since moviepy only accepts strings for path objects
        if (self.output_path.exists()):
            return True, output
        drop_shadow = self.text_clip.copy()
        drop_shadow = drop_shadow.set_opacity(0.5)
        drop_shadow = drop_shadow.set_position((self.h_padding + shadow_offset, self.v_padding + shadow_offset))
        result_clip = CompositeVideoClip([self.base_clip,
                                          drop_shadow,
                                          self.text_clip])
        try:
            result_clip = result_clip.set_duration(5.0)
            if (self.output_path.suffix == '.gif'):
                result_clip.write_gif(output, fps=self.base_clip.fps, program='ImageMagick', fuzz=0)
            else:
                result_clip.write_videofile(output)
            return True, output
        except Exception as e:
            print(e)
            return False, e

if __name__ == '__main__':
    clip = TurnClip('Melody')
    written, data = clip.composite()
    if (written == True):
        pass
    else:
        print('failed to write file')