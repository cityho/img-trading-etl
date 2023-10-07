from PIL import Image

image_path = 'your_image.jpg'  # 이미지 파일의 경로를 지정하세요.

def get_img_size(image_path):
    try:
        img = Image.open(image_path)

        # 이미지의 가로(width)와 세로(height) 크기 확인
        width, height = img.size

    except Exception as e:
        print(f"이미지를 열 수 없거나 에러가 발생했습니다: {e}")

    return {"width":width, "height": height}


# print(
#     get_img_size("/locdisk/data/hoseung2/img/img_w_ma/kospi/20200303/A105010.png")
# )