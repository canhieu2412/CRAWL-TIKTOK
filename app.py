import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os

class TikTokScraper:
    def __init__(self, url, output="./tiktok"):
        self.url = url
        self.id = None
        self.output = output
        self.session = requests.session()  # Sử dụng session để quản lý cookie và yêu cầu
        self.vid_data = {}
    
    def check_url(self):
        #tat nhien là phải kiểm tra roi =)) , có thể có trường hợp link bị rút gọn , lỡ đâu là link cornhub
        response_check = requests.get(self.url, allow_redirects=True)
        final_url = response_check.url
        #gửi rì quét vào cái link bất kì có thể là rút gọn để có thể ra được phiên bản link đầy đủ rồi đối chiếu thôi :3
        if not final_url.startswith(("https://vt.tiktok.com", "https://www.tiktok.com")):
            raise ValueError("ERROR, Sai link rồi bạn ơi!")
        self.url = final_url

        return response_check
        

    def get_information(self):
        #sau khi ngồi mò mẫm với hàng chục link vid thì e phát hiện là có thể lấy luôn id vid và người đăng vid.Nên là e tận dụng bằng cách dùng thư viện re
        self.id= re.search(r'/video/(\d+)', self.url).group(1)
        self.author= re.search(r'tiktok\.com/@([^/]+)/video', self.url).group(1)

        headers = {
            "accept": "*/*",
            "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
            "Referer": "https://www.tiktok.com/",
            "Accept-Encoding": "identity;q=1, *;q=0"
        }
        cookies = {
            'tt_webid': '1' * 19,
            'tt_webid_v2': '1' * 19
        }
        response = self.session.get(self.url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(response.text, "html.parser")

        vid_data = {
            "id": self.id,
            "author_name": self.author,
            "views": "",
            "likes":"",
            "comments": "",
            "saves": "",
            "date": "",
            "description": "",
            "hashtag": [],
        }



        #TikTok nhúng rất nhiều dữ liệu JSON quan trọng vào trong thẻ <script> có id="__UNIVERSAL_DATA_FOR_REHYDRATION__"
        #Phần này chứa dữ liệu toàn bộ về video, người dùng, thời gian đăng, lượt xem, v.v. dưới dạng JSON.


        script_tag = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
        if script_tag:
            try:
                raw_json = script_tag.string
                data = json.loads(raw_json)
                ts = int(data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['createTime'])

            #Lọc sâu vào cấu trúc JSON để lấy trường createTime.
            #createTime chính là thời gian đăng video dưới dạng UNIX timestamp (số giây kể từ 01/01/1970).
            #Trường này thường ở trong phần itemStruct của itemInfo trong webapp.video-detail

                date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                #Chuyển timestamp số nguyên thành đối tượng datetime trong Python
                #Sau đó format thành chuỗi thời gian đẹp dạng "YYYY-MM-DD HH:MM:SS"

                vid_data["date"] = date_str
            except Exception as e:
                print("Không lấy được thời gian đăng:", e)
                
        if script_tag:
            try:
                raw_json = script_tag.string
                #Lấy nội dung dạng chuỗi từ bên trong thẻ <script>

                data = json.loads(raw_json)
                item_struct = data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']
                stats = item_struct.get('stats', {})
                #Lấy thông tin thống kê của video từ itemStruct, nếu không có thì trả về dictionary rỗng.

                vid_data["likes"] = stats.get('diggCount', '')
                #Gán số lượt "thích" (likes) vào biến vid_data["likes"]
                #'diggCount' là key trong stats chứa số lượt thích.
                #tương tự với những cái còn lại
                vid_data["comments"] = stats.get('commentCount', '')
                vid_data["views"] = stats.get('playCount', '')
                vid_data["saves"] = stats.get('shareCount', '')

                #ở đây e sẽ dùng hàm sub() có trong thư viện re để xóa bỏ các kí tự bắt đầu bằng kí tụ '#' để lấy ra được phần mô tả
                vid_data["description"] = re.sub(r'#\w+', '', item_struct.get('desc', '')).strip()

                text_tags = item_struct.get('textExtra', []) #Lấy giá trị của hashtagName từ mỗi tag trong text_tags, trả về chuỗi rỗng nếu không có
                #Chỉ lấy các tag có hashtagName không rỗg với e cộng thêm kí tự hashtag để giữ nguyên định dạng của nó khi xuất sang file Json
                vid_data["hashtag"] = ['#'+tag.get('hashtagName', '') for tag in text_tags if tag.get('hashtagName')]


                #đoạn này là e viết sau , lúc viết phần download stuck quá thì mò ra được thêm cách này , cái phần này mục đích chỉ là để lấy link video
                video_data = item_struct.get('video', {})
                self.video_url = video_data.get('playAddr', '')


            except Exception as e:
                print(f"Lỗi khi lấy thông tin từ JSON: {e}")


            self.vid_data = vid_data
            #ở đây thì e sẽ lưu lại kết quả của dict vào trong self.vid_data , để còn sử dụng trong hàm lưu thành file Json


    def save_2_json(self):
        #đầu tiên thì ta phải set filename trước theo đúng định dạng trong file a Vuahz
        filename = f"tiktok_{self.id}.json"
        file_path = os.path.join(self.output, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:

                json.dump(self.vid_data, f, ensure_ascii=False, indent=4)

            print(f" Đã lưu thành công data vào : {file_path}")

        except Exception as e:
            print(f"Lỗi khi lưu file JSON: {e}")



    def download(self):
        if not self.video_url:
            print("Lỗi: Không tìm thấy URL video!")
            return

        filename = f"tiktok_{self.id}.mp4"
        file_path = os.path.join(self.output, filename)
        os.makedirs(self.output, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        headers = {
            "accept": "*/*",
            "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
            "Referer": "https://www.tiktok.com/",
            "Range": "bytes=0-",
            "Accept-Encoding": "identity;q=1, *;q=0"
        }
        cookies = {
            'tt_webid': '1' * 19,
            'tt_webid_v2': '1' * 19
        }
        
        try:
            response = self.session.get(self.video_url, headers=headers, cookies=cookies)
            response.raise_for_status()  # Kiểm tra mã trạng thái HTTP
            with open(file_path, 'wb') as f:
                f.write(response.content)  # Lưu toàn bộ nội dung video
            print(f"Đã tải thành công video tại: {file_path}")
        except requests.RequestException as e:
            print(f"Lỗi khi tải video: {e}")
        except Exception as e:
            print(f"Lỗi không xác định khi tải video: {e}")

if __name__ == "__main__":
    a = 'https://www.tiktok.com/@jasminenguyen1998/video/7504965130900344071'
    b = TikTokScraper(a)
    b.check_url() 
    b.get_information()
    b.save_2_json() 
    b.download()

