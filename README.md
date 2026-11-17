# Truyện học từ

Mở **`stories.html`** (bấm đúp) để đọc truyện trên máy tính.

**Trên điện thoại:** https://joyfulsteps.github.io/word-stories/ (repo công khai `JoyfulSteps/word-stories`, nhánh `main`, GitHub Pages).

Đưa bản mới lên web sau khi viết thêm truyện:
```
python _tools/build.py
git add -A && git commit -m "Add stories ..." && git push
```
Trang thật cập nhật sau khoảng 1–2 phút. Trên điện thoại, kéo xuống để tải lại trang.

## Kế hoạch

- **8.662 từ** trong từ điển (cả từ đã biết và chưa biết), mỗi từ có trong ít nhất 1 truyện.
- Chia thành **225 truyện**, đi theo thứ tự W01 → W60. Mỗi truyện có **tối đa khoảng 30 từ mới** và khoảng 70 từ của danh sách.
- Đơn vị nào toàn từ đã biết (W01–W07, W60…) thì thành truyện dễ, dùng để ôn và đọc nhanh.
- Các truyện kể nối tiếp nhau về Minh, một sinh viên Việt Nam sống với gia đình Parker ở Anh.
- `words.tsv`: mỗi dòng là một từ: `status` (new/known), `group` (A hay gặp / B vừa / C hiếm), `story` (thuộc truyện nào).

## Cách học một truyện (khoảng 30 phút một ngày)

| Ngày | Làm gì | Thời gian |
|---|---|---|
| Ngày 1 | Đọc **Read** + nghe **Listen** 1 lần → bấm từ xanh xem nghĩa → đọc lại lần 2, không tra | 20 phút |
| Ngày 2 | **Review**: từ mới bị che, nhớ lại rồi bấm để kiểm tra. Đọc to 1 đoạn | 10 phút |
| Ngày 4–5 | Review lần nữa. Che cột tiếng Việt trong bảng từ, tự nói nghĩa | 5–10 phút |
| Ngày 10–14 | Review lần cuối. Kể lại truyện bằng 4–5 câu (nói hoặc viết) | 10 phút |

Mỗi ngày: **1 truyện mới + ôn 1–2 truyện cũ**. Không cần thuộc hết, chỉ cần hiểu cả truyện và nhớ được hơn nửa số từ là đạt.

## Dành cho AI làm tiếp

- Truyện viết ở `text/<mã truyện>.md`: dòng đầu `# Tiêu đề`, từ mới in đậm `**từ**`, dòng thư hoặc trích dẫn bắt đầu bằng `> `.
- Từ của mỗi truyện lấy từ cột `story` trong `words.tsv`. Chỉ in đậm từ `new`. Từ `known` phải có mặt trong truyện nhưng không in đậm.
- Mỗi lần viết xong, chạy `python _tools/build.py`: kiểm tra đủ từ, đúng in đậm, rồi dựng lại `stories.html`. Chỉ báo xong khi không còn lỗi.
- `_tools/plan.py` dựng lại `words.tsv`: chạy lại sẽ chia truyện lại, **không chạy** khi đã có truyện, trừ khi người dùng đánh dấu lại từ.
- Nhân vật: Minh (19 tuổi, người Việt, du học ở Anh); Tom Parker (người Mỹ, hơi béo, hói), Anna (người Anh, giáo viên); cặp sinh đôi Leo và Mia (15 tuổi); Grandma Rose (80 tuổi, người Anh, khôn ngoan); Sam (bạn học người Tây Ban Nha, ở căn studio thuê của Mr. Patel); Mr. Lee (hàng xóm, đối tác của Tom). Tom nói từ Mỹ, Grandma Rose nói từ Anh: dùng cặp này để đưa các cặp từ Anh–Mỹ vào truyện.
- Trình độ người đọc A2–B1: câu ngắn, thì quá khứ đơn, 450–550 từ mỗi truyện.
