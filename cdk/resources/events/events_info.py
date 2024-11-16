from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import numpy as np
import boto3

def lambda_handler(event, context):

    texts = {"Eduardo": 21,
                "Data Engineer": 12}
    images = {"spark.png": (130, 0),
                "aws.png": (125, 165)}
    make_thumbnail(texts, images)

s3 = boto3.resource('s3', region_name='us-east-1')
bucket = s3.Bucket('stori-technical-test')

def add_image(base_image, image, size, loc, rot):
    crop = image.resize(size=size)
    rotate = crop.rotate(rot, expand=True)
    base_image.paste(rotate, loc, rotate)


def get_images(name):
    file = bucket.Object(name)
    response_stori = file.get()
    file_layout = response_stori['Body']
    print(name, file_layout)
    main_image = Image.open(file_layout)
    return np.array(main_image)

def save_img(image,name):
    object = bucket.Object(name)
    file_stream = BytesIO()
    image.save(file_stream, format='png')
    object.put(Body=file_stream.getvalue())


def make_thumbnail(texts, images):
    stori = get_images('stori.png')
    im_stori = Image.fromarray(stori)

    for index, i in enumerate(images.keys()):
        extra_image = get_images(i)
        image = Image.fromarray(extra_image)
        add_image(im_stori, image, size=image.size, loc=images[i], rot=0)

        draw = ImageDraw.Draw(im_stori)
        for index,text in enumerate(texts):
            draw.text(xy=(100,110+ (texts[text]*index*2)), text=text, fill=(255,255,255), align="center", font=ImageFont.load_default())

    save_img(im_stori, "output/stori_thumbnails.png")