import numpy as np
import imageio
import scipy.ndimage
import cv2

# Görüntü yolu
img_path = "jason.jpg"

# RGB'den gri tonlamaya dönüşüm
def rgb2gray(rgb_image):
    return np.dot(rgb_image[...,:3], [0.2989, 0.5879, 0.1140])

# Karakalem efekti (dodge blend)
def dodge(front, back):
    result = front * 255 / (255 - back)
    result[result > 255] = 255  # Piksel değerlerini 255 ile sınırlama
    result[back == 255] = 255  # Arka planın beyaz olduğu yerleri beyaz bırakma
    return result.astype("uint8")

# Görüntüyü yükle ve işleme başla
image = imageio.imread(img_path)  # Görüntüyü oku
gray_image = rgb2gray(image)  # Gri tonlamaya çevir
inverted_image = 255 - gray_image  # İnvert (ters) görüntü oluştur

# Gaussian bulanıklık uygula
blurred_image = scipy.ndimage.gaussian_filter(inverted_image, sigma=15)

# Karakalem efektini uygula
sketch_image = dodge(blurred_image, gray_image)

# Çıkış görüntüsünü yeniden boyutlandırır (örneğin, genişliği 600 piksel olacak şekilde)
height, width = sketch_image.shape
new_width = 600
scale_factor = new_width / width
new_height = int(height * scale_factor)
resized_image = cv2.resize(sketch_image, (new_width, new_height))

# Sonucu kaydet ve göster
cv2.imwrite("karakalem.png", sketch_image)  # Çıkışı kaydet
cv2.imshow("Karakalem Çizim", resized_image)  # Yeniden boyutlandırılmış görüntüyü göster
cv2.waitKey(0)
cv2.destroyAllWindows()
