
import requests
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
from io import BytesIO


def scrape_and_export_to_excel(output_path, num_posts):
    url = "http://nhasachtinhoc.blogspot.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        posts = soup.find_all("div", class_="post")

        data = []

        for post in posts[:num_posts]:
            title = post.find("h3").text.strip()
            content = post.find("div", class_="post-body").text.strip()
            image_url = post.find("img")["src"]

            try:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_data = image_response.content
                    image = Image.open(BytesIO(image_data))
                else:
                    image = None
                    print(f"Lỗi: Không thể tải hình ảnh từ {image_url}")
            except Exception as e:
                image = None
                print(f"Lỗi: {str(e)}")

            data.append([title, content, image])

        df = pd.DataFrame(data, columns=["Tiêu đề", "Nội dung", "Hình ảnh"])
        df.to_excel(output_path, index=False)
        print(f"Dữ liệu từ {num_posts} bài viết đã được xuất thành công vào tệp Excel: {output_path}")
    else:
        print("Không thể kết nối đến trang web.")


num_posts = int(input("Nhập số lượng bài viết muốn lấy: "))


output_path = input("Nhập đường dẫn và tên tệp Excel để lưu (phải có đuôi .xlsx ): ")

scrape_and_export_to_excel(output_path, num_posts)
