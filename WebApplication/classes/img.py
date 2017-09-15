__author__ = 'ReS4'
import os

from PIL import Image


class R_imgResizer():
    def __init__(self, path):
        self.path = path

    # def imageResize(self,min_width=100,min_height=100,max_width=700,max_height=500,prefix=''):

    def imageResizeGallery(self, max_width=700, max_height=500, prefix='', save_path=''):

        file_dir = os.path.split(self.path)

        img = Image.open(self.path)

        if img.size[0] > max_width and img.size[1] > max_height:

            if img.size[0] > img.size[1]:
                aspect = float(img.size[1]) / max_height
                new_size = (int(img.size[0] / aspect), max_height)
            elif img.size[0] == img.size[1]:

                if img.size[0] > 700:
                    aspect = float(img.size[0]) / max_width
                    new_size = (int(max_width / aspect), int(max_width / aspect))
                elif img.size[1] > 500:
                    aspect = float(img.size[1]) / max_height
                    new_size = (int(max_height / aspect), int(max_height / aspect))
                else:
                    new_size = (max_width, max_width)

            else:
                aspect = float(img.size[0]) / max_width
                new_size = (max_width, int(img.size[1] / aspect))

            img.resize(new_size, Image.ANTIALIAS).save(save_path + '/' + prefix + file_dir[1])

            return



        elif img.size[0] > max_width:

            aspect = float(max_width) / int(img.size[0])
            new_size = (max_width, int(img.size[1] * aspect))
            img.resize(new_size, Image.ANTIALIAS).save(save_path + '/' + prefix + file_dir[1])
            return


        elif img.size[1] > max_height:
            aspect = float(max_height) / int(img.size[1])
            new_size = (int(img.size[0] * aspect), max_height)
            img.resize(new_size, Image.ANTIALIAS).save(save_path + '/' + prefix + file_dir[1])
            return

        else:
            return



            #
            # if img.size[0] < min_width or img.size[1] < min_height:
            #     if img.size[1] < min_height:
            #         return
            #     elif img.size[0] < min_width:
            #         return
            #     else:
            #         pass
            # else:
            #     if img.size[0] > img.size[1]:
            #         aspect = (int(img.size[1])/max_height)
            #         new_size = (img.size[0]/aspect, max_height)
            #     elif img.size[0] == img.size[1]:
            #         new_size = (max_width, max_width)
            #     else:
            #         aspect = (int(img.size[0])/max_width)
            #         new_size = (max_width, img.size[1]/aspect)
            #
            #     img.resize(new_size,Image.ANTIALIAS).save(file_dir[0]+'/re_'+file_dir[1])

    def imageResize_Crop(self, min_width=100, min_height=100, max_width=100, max_height=100, prefix='', save_path=''):

        file_dir = os.path.split(self.path)

        img = Image.open(self.path)
        if img.size[0] < min_width:
            if img.size[1] < min_height:
                return
            else:
                if img.size[0] > img.size[1]:
                    new_img = img.crop((
                        (((img.size[0]) - max_width) / 2),
                        0,
                        max_width + (((img.size[0]) - max_width) / 2),
                        max_height
                    ))
                else:
                    new_img = img.crop((
                        0,
                        (((img.size[1]) - max_height) / 2),
                        max_width,
                        max_height + (((img.size[1]) - max_height) / 2)
                    ))

                new_img.save(file_dir[0] + '/' + prefix + file_dir[1])
        else:
            if img.size[0] > img.size[1]:
                aspect = (int(img.size[1]) / max_height)
                new_size = (img.size[0] / aspect, max_height)
            elif img.size[0] == img.size[1]:
                new_size = (max_width, max_width)
            else:
                aspect = (int(img.size[0]) / max_width)
                new_size = (max_width, img.size[1] / aspect)

            img.resize(new_size, Image.ANTIALIAS).save(save_path + '/' + prefix + file_dir[1])

            img = Image.open(file_dir[0] + '/' + prefix + file_dir[1])
            if img.size[0] > img.size[1]:
                new_img = img.crop((
                    (((img.size[0]) - max_width) / 2),
                    0,
                    max_width + (((img.size[0]) - max_width) / 2),
                    max_height
                ))
            else:
                new_img = img.crop((
                    0,
                    (((img.size[1]) - max_height) / 2),
                    max_width,
                    max_height + (((img.size[1]) - max_height) / 2)
                ))

            new_img.save(save_path + '/' + prefix + file_dir[1])

    def cropImage(self, max_width=100, max_height=100, save_path=''):

        file_dir = os.path.split(self.path)
        img = Image.open(self.path)
        if img.size[0] > img.size[1]:
            new_img = img.crop((
                (((img.size[0]) - max_width) / 2),
                0,
                max_width + (((img.size[0]) - max_width) / 2),
                max_height
            ))
        else:
            new_img = img.crop((
                0,
                (((img.size[1]) - max_height) / 2),
                max_width,
                max_height + (((img.size[1]) - max_height) / 2)
            ))

        new_img.save(save_path + '/cr_' + file_dir[1])

    def resizeANDcrop(self, max_width, max_height, prefix='', save_path=''):
        '''Downsample the image.
        @param img: Image -  an Image-object
        @param box: tuple(x, y) - the bounding box of the result image
        @param fix: boolean - crop the image to fill the box
        @param out: file-like-object - save the image into the output stream
        '''
        file_dir = os.path.split(self.path)

        box = (max_width, max_height)

        img = Image.open(self.path)

        # preresize image with factor 2, 4, 8 and fast algorithm
        factor = 1
        while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
            factor *= 2
        if factor > 1:
            img.thumbnail((img.size[0] / factor, img.size[1] / factor), Image.NEAREST)

        # calculate the cropping box and get the cropped part

        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2 / box[0]
        hRatio = 1.0 * y2 / box[1]
        if hRatio > wRatio:
            y1 = int(y2 / 2 - box[1] * wRatio / 2)
            y2 = int(y2 / 2 + box[1] * wRatio / 2)
        else:
            x1 = int(x2 / 2 - box[0] * hRatio / 2)
            x2 = int(x2 / 2 + box[0] * hRatio / 2)
        img = img.crop((x1, y1, x2, y2))

        # Resize the image with best quality algorithm ANTI-ALIAS
        img.thumbnail(box, Image.ANTIALIAS)

        # save it into a file-like object
        img.save(save_path + '/' + prefix + file_dir[1], "PNG", quality=75)

    def only_resize(self, max_width, max_height, prefix='', save_path='', structure='PNG', quality=75):
        '''Downsample the image.
        @param img: Image -  an Image-object
        @param box: tuple(x, y) - the bounding box of the result image
        @param fix: boolean - crop the image to fill the box
        @param out: file-like-object - save the image into the output stream
        '''
        file_dir = os.path.split(self.path)

        box = (max_width, max_height)

        img = Image.open(self.path)

        # preresize image with factor 2, 4, 8 and fast algorithm
        factor = 1
        while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
            factor *= 2
        if factor > 1:
            img.thumbnail((img.size[0] / factor, img.size[1] / factor), Image.NEAREST)

        # Resize the image with best quality algorithm ANTI-ALIAS
        img.thumbnail(box, Image.ANTIALIAS)

        # save it into a file-like object
        img.save(save_path + '/' + prefix + file_dir[1], structure, quality=quality)

# # s = R_imgResizer("../static/images/healthy-food2.jpg")

# s = R_imgResizer("../static/images/profile.jpg")
# s.imageResizeGallery(prefix='gll_')


# s = R_imgResizer("../static/images/header.png")
# s.imageResize_Crop(max_width=150,max_height=200)
# s.imageResize_Crop(max_width=150,max_height=200,prefix='150x200_',save_path="../static/images")

# imageResize("../static/images/healthy-food2.jpg")


#
# import sys

#
# def crop_resize(image, size, exact_size=False):
#     """
#     Crop out the proportional middle of the image and set to the desired size.
#     * image: a PIL image object
#     * size: a 2-tuple of (width,height);  at least one must be specified
#     * exact_size: whether to scale up for smaller images
#     If the image is bigger than the sizes passed, this works as expected.
#     If the image is smaller than the sizes passed, then behavior is dictated
#     by the ``exact_size`` flag.  If the ``exact_size`` flag is false,
#     the image will be returned unmodified.  If the ``exact_size`` flag is true,
#     the image will be scaled up to the required size.
#     """
#     assert size[0] or size[1], "Must provide a width or a height"
#
#     size = list(size)
#
#     image_ar = image.size[0]/float(image.size[1])
#     crop = size[0] and size[1]
#     print(crop)
#     if not size[1]:
#         size[1] = int(image.size[1]*size[0]/float(image.size[0]) )
#     if not size[0]:
#         size[0] = int(image.size[0]*size[1]/float(image.size[1]) )
#     size_ar = size[0]/float(size[1])
#
#     if size[0] > image.size[0]:
#         if size[1] > image.size[1]:
#             if not exact_size:
#                 return image
#         else:
#             pass
#             # raise NotImplementedError
#     elif size[1] > image.size[1]:
#         pass
#
#     if crop:
#         if image_ar > size_ar:
#             # trim the width
#             xoffset = int(0.5*(image.size[0] - size_ar*image.size[1]))
#             image = image.crop((xoffset, 0, image.size[0]-xoffset, image.size[1]))
#         elif image_ar < size_ar:
#             # trim the height
#             yoffset = int(0.5*(image.size[1] - image.size[0]/size_ar))
#             image = image.crop((0, yoffset, image.size[0], image.size[1] - yoffset))
#
#     return image.resize(size, Image.ANTIALIAS)
#
# ims = crop_resize(Image.open("../static/images/healthy-food2.jpg",'r'),(200,0),exact_size=True)
# ims.save("../static/images/crop_healthy-food2.jpg")
