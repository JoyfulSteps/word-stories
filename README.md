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
- `python _tools/words_for.py W11 W12` in ra từ của từng truyện (`*` = từ mới, phải in đậm).

## Cốt truyện tổng (người dùng giao viết hết 225 truyện, 17/11/2026)

Thị trấn: **Riverford**, một thị trấn nhỏ ở Anh, có sông, lâu đài trên đồi, trường cao đẳng (college). Quán cà phê **The Blue Cup** của Daniel (cháu trai Grandma Rose). Em họ y tá: Kate (cháu gái Grandma Rose).

**Phần 0: W01–W07, Minh hồi nhỏ ở Việt Nam** (toàn từ đã biết, truyện ngắn và dễ). Kể theo kiểu hồi tưởng, Minh từ 6 đến 18 tuổi ở một thị trấn ven sông gần Hà Nội (hay bị lụt). Mẹ là cô giáo, bố sửa xe máy, em gái Lan nhỏ hơn 4 tuổi, bà nội. Bạn thân Tuấn. Cuối phần: Minh đỗ học bổng đi Anh.

**Phần 1: W08–W19, năm đầu ở Anh** (tháng 9 → tháng 6). W08–W10 đã viết (đến, ốm, nhà cửa, Sam thuê studio, mất điện, nấu ăn, bưu kiện). Tiếp: W11 đồ ăn, đi chợ, Giáng sinh, sinh nhật Mia; W12 thiên nhiên, chuyến đi trang trại ở Wales; W13 thị trấn, giao thông, đi London; W14 học hành, Minh xin làm thêm ở The Blue Cup; W15 công nghệ, thể thao, Leo đá chung kết, chạy từ thiện; W16 lễ hội văn hóa ở trường; W17 đêm đố vui (quiz night); W18–W19 mạch **bí mật của Grandma Rose** (thư cũ, người bạn thời trẻ tên Margaret) và **cuộc thi vẽ của Mia**; kết thúc năm học, Minh về Việt Nam nghỉ hè.

**Thời gian thực tế đã viết:** W08–W15 là năm đầu (tháng 9 → tháng 7); W16 bắt đầu năm thứ hai (tháng 8–9). Hana (sinh viên Nhật, học điều dưỡng) xuất hiện từ W16-3. W17-3 → W19-1: tìm lại Margaret (bạn thân của Grandma Rose, ở gần Edinburgh, con gái tên Fiona); W19-2: Mia đoạt giải, được học lớp nghệ thuật ở London ngày thứ Bảy; W19-3: Minh về Việt Nam ăn Tết (tháng 2), tình cảm với Hana bắt đầu.

**Phần 2: W20–W33, phần còn lại của năm thứ hai và năm thứ ba (lên đại học ở thành phố gần đó).** Minh làm ở The Blue Cup; bạn mới Hana (sinh viên Nhật học điều dưỡng), có tình cảm nhẹ với Minh. Leo chấn thương đầu gối, phải bỏ bóng đá rồi tìm đam mê mới. Grandma Rose ngã, nằm viện, hồi phục. Quán The Blue Cup gặp khó về tiền và cả nhóm cứu quán. Sam mở công ty thiết kế nhỏ. Mia muốn học trường nghệ thuật nhưng Tom muốn con học luật; cuối cùng Tom đồng ý. Có mâu thuẫn và kịch tính, nhưng kết ấm áp.

**Đã viết thực tế ở phần 2:** Minh làm ở The Blue Cup, cứu quán (cổ phần cộng đồng, W26), thực tập rồi thành phóng viên Gazette (W27–W33; biên tập Grace Okafor là con gái chủ nhà Mr. Okafor), Leo chấn thương → muốn làm bác sĩ thú y, Mia học nghệ thuật ở London, Minh viết tiểu thuyết *Two Rivers* (agent Diana Ross, được xuất bản), W33-3 Minh và Hana sang Tokyo (Hana làm y tá; Minh viết loạt bài "Two Small Towns" từ xa cho Gazette, hợp đồng 1 năm).

**Phần 3 (đã điều chỉnh): W34–W42, Minh là phóng viên viết từ Nhật, Việt Nam và Riverford.** Mỗi truyện là một phóng sự hoặc vụ việc theo chủ đề từ của đơn vị.

(Kế hoạch cũ:) **Phần 3: W34–W42, Minh thực tập ở báo *The Riverford Gazette*.** Biên tập viên: bà Grace Okafor (nghiêm, giỏi). Mỗi truyện là một vụ việc hoặc phóng sự: bệnh viện, thời tiết và môi trường, khoa học ở trường đại học, công ty phá sản, phiên tòa, triển lãm nghệ thuật, ngôn ngữ. Có yếu tố điều tra và bí ẩn.

**Đã viết thực tế ở phần 3 (W34–W42):** Minh ở Tokyo, làm cho báo tiếng Anh rồi trang độc lập Open Tokyo (biên tập Yuko; đồng nghiệp Ben, Aiko, Min-ji, Pierre); Margaret mất (W34-5), để lại căn nhà ở Scotland cho Grandma Rose; Lan sang Tokyo học sư phạm; Leo đi Borneo (đười ươi); Minh cầu hôn Hana (W40-4), ba đám cưới: Nhật (W42-2), Việt Nam (W42-3), Scotland (W42-4); W42-5 hai người về Riverford, Minh làm podcast *Riverford Talks* với Gazette.

**Đã viết thực tế ở phần 4 (W43–W60):** các tập podcast *Riverford Talks* và bản tin "This Week in Riverford"; Minh thành tổng biên tập Gazette (W52-1, Grace nghỉ hưu); Rose Mai ra đời (W50-4); Tom bị nhồi máu cơ tim (W54-4); cá hồi trở lại sông (W54-5); Grandma Rose mất ở tuổi 95 (W59-3); W60-3 là truyện kết thúc. Ngày 17/11/2026: **đã viết đủ 225 truyện, phủ 8.662/8.662 từ**.

**Phần 4: W43–W60, bài báo và podcast *Riverford Talks* do Minh dẫn.** Dạng phỏng vấn, tranh luận, bài báo về đề tài IELTS (giáo dục, môi trường, tội phạm, toàn cầu hóa, công nghệ, sức khỏe, nhà ở, việc làm). Khách mời là các nhân vật cũ và chuyên gia. 550–700 từ, câu rõ ràng. Có thể có bài dạng "bài báo" hoặc "lá thư gửi tòa soạn".

Quy tắc chung: mỗi truyện có tiêu đề, tự đứng được (đọc riêng vẫn hiểu), nhưng nối tiếp mạch chung. Từ mới đặt trong ngữ cảnh đủ rõ để đoán nghĩa. Không dùng từ trong danh sách sai nghĩa với cột `vi` khi có thể.
