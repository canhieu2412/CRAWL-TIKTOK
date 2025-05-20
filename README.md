# TikTokScraper - Công cụ thu thập dữ liệu và tải video từ TikTok

## Giới thiệu
`TikTokScraper` là một script Python được thiết kế để thu thập thông tin từ video TikTok (bao gồm ID, tác giả, lượt xem, lượt thích, bình luận, lượt chia sẻ, ngày đăng, mô tả và hashtag) và tải video về máy. Script sử dụng các thư viện như `requests`, `BeautifulSoup`, và `re` để truy cập và phân tích dữ liệu từ URL TikTok.

## Yêu cầu
Để chạy script, bạn cần cài đặt các thư viện Python sau:
- `requests`: Để gửi yêu cầu HTTP.
- `beautifulsoup4`: Để phân tích HTML.
- `python` (phiên bản 3.6 trở lên).

Cài đặt các thư viện cần thiết bằng lệnh:

```bash
pip install requests beautifulsoup4
```

## Cấu trúc script
Script bao gồm một lớp `TikTokScraper` với các phương thức chính:
1. `__init__(url, output)`: Khởi tạo với URL của video TikTok và thư mục đầu ra (mặc định là `./tiktok`).
2. `check_url()`: Kiểm tra tính hợp lệ của URL TikTok (hỗ trợ cả URL rút gọn).
3. `get_information()`: Thu thập thông tin video như ID, tác giả, lượt xem, lượt thích, bình luận, lượt chia sẻ, ngày đăng, mô tả và hashtag.
4. `save_2_json()`: Lưu thông tin video vào file JSON với định dạng `tiktok_<video_id>.json`.
5. `download()`: Tải video về máy dưới định dạng `tiktok_<video_id>.mp4`.


## Cách sử dụng
1. **Chuẩn bị**: Đảm bảo bạn đã cài đặt các thư viện cần thiết và có một URL video TikTok hợp lệ.
2. **Chạy script**:
   - Tạo một instance của lớp `TikTokScraper` với URL video và (tuỳ chọn) thư mục đầu ra.
   - Gọi các phương thức theo thứ tự: `check_url()`, `get_information()`, `save_2_json()`, và `download()`.

   Ví dụ:
   ```python
   from tiktok_scraper import TikTokScraper

   # URL video TikTok
   url = "https://www.tiktok.com/@jasminenguyen1998/video/7504965130900344071"
   scraper = TikTokScraper(url, output="./tiktok_videos")
   scraper.check_url()
   scraper.get_information()
   scraper.save_2_json()
   scraper.download()
   ```

3. **Kết quả**:
   - File JSON (`tiktok_<video_id>.json`) chứa thông tin video sẽ được lưu vào thư mục chỉ định.
   - Video (`tiktok_<video_id>.mp4`) sẽ được tải về cùng thư mục.

## Lưu ý
- **URL hợp lệ**: Script chỉ hoạt động với URL TikTok chính thức (bắt đầu bằng `https://www.tiktok.com` hoặc `https://vt.tiktok.com`).
- **Header và cookie**: Script sử dụng một bộ header và cookie mẫu để gửi yêu cầu HTTP. Nếu gặp lỗi liên quan đến truy cập, bạn có thể cần cập nhật cookie hoặc user-agent trong script.
- **Thư mục đầu ra**: Đảm bảo thư mục đầu ra tồn tại hoặc script sẽ tự động tạo nó.
- **Xử lý lỗi**: Script bao gồm xử lý lỗi cơ bản (ví dụ: URL không hợp lệ, lỗi tải video). Kiểm tra thông báo lỗi trong console để khắc phục.

## Ví dụ kết quả
Sau khi chạy script với URL hợp lệ:
- File JSON (`tiktok_7504965130900344071.json`) có thể chứa:
  ```json
  {
      "id": "7504965130900344071",
      "author_name": "jasminenguyen1998",
      "views": "30100",
      "likes": "2126",
      "comments": "26",
      "saves": "38",
      "date": "2025-05-16 15:57:46",
      "description": "Tại sao speaking tốt nhưng không được điểm cao?",
      "hashtag": ["#jasminenguyenielts",
        "#jasminenguyen1998",
        "#traenglish",
        "#ielts",
        "#ieltsspeaking",
        "#ieltstips"]
  }
  ```
- Video sẽ được lưu tại: `./tiktok/tiktok_7504965130900344071.mp4`.

## Xử lý sự cố
- **Lỗi "Sai link rồi bạn ơi!"**: Kiểm tra lại URL TikTok. Đảm bảo URL bắt đầu bằng `https://www.tiktok.com` hoặc `https://vt.tiktok.com`.
- **Lỗi tải video**: Kiểm tra kết nối mạng hoặc cập nhật cookie/user-agent trong script.
- **Lỗi JSON**: Đảm bảo script có quyền ghi vào thư mục đầu ra.
