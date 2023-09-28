from PIL import Image
from flask import Flask, render_template, request
import filetype
from colorthief import ColorThief

app = Flask(__name__)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if not filetype.is_image(f):
            print('Error! Uploaded file is not recognized as an image!')
            return 'File not recognized as an image.. Please use a different image'
        color_thief = ColorThief(f)
        palette = color_thief.get_palette(color_count=11)  # Subtract 1 for some reason
        color_palette = []
        for i in palette:
            color_palette.append('#%02x%02x%02x' % i)
        img = Image.open(f)
        img.save('static/img/output.png')
        return render_template('color.html', palette=color_palette)


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
