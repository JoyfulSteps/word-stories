# Truyện học từ

Mở **`stories.html`** (bấm đúp) để đọc truyện trên máy tính.

**Trên điện thoại:** https://joyfulsteps.github.io/word-stories/ (repo công khai `JoyfulSteps/word-stories`, nhánh `main`, GitHub Pages).

Đưa bản mới lên web sau khi viết thêm truyện:
```
python _tools/build.py
git add -A && git commit -m "Add stories ..." && git push
```
Trang thật cập nhật sau khoảng 1–2 phút. Trên điện thoại, kéo xuống để tải lại trang.

Link tới một truyện: `…/word-stories/#W02-1` (mở đúng truyện đó; địa chỉ luôn đổi theo truyện đang đọc). Trang thẻ ngữ pháp dùng link này cho mục "In Minh's story" (xem `D:\English\ielts-grammar\_web\README.md`). Nếu sửa câu trong truyện, chạy lại `python _web/build_site.py` bên ielts-grammar: nó báo lỗi khi câu đã gắn vào thẻ không còn đúng nguyên văn.

**Cài như app và cửa sổ nổi** (2026-11-24, giống từ điển): `manifest.webmanifest` + `icon.svg`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png` (chữ S trắng trên nền xanh #1565c0) ở thư mục gốc; `sw.js` lưu sẵn các file này để app mở được khi offline. Trên máy tính, link ra ngoài (Dictionary, Cambridge, Google Translate, Ask AI) mở trong một cửa sổ nhỏ bên phải, mỗi loại một cửa sổ dùng lại (`data-win` = ws_dict, ws_cam, ws_gt, ws_ai); trên điện thoại vẫn mở tab mới. Ctrl/Shift-click thì để trình duyệt mở tab như thường.

**Link tới đúng câu** (2026-11-24): `…/word-stories/#W02-1?s=17&w=sweater` mở truyện W02-1, cuộn tới câu 17, tô nền câu và tô vàng chữ "sweater". `s=12-13` tô một đoạn nhiều câu. Nếu truyện đã sửa và câu 17 không còn chữ đó, trang tự chọn câu gần nhất có chữ đó.
- Câu được tách **một lần** trong `_tools/build.py` (`split_sentences`, đánh số 1, 2, 3… trong từng truyện) và trang đọc dùng lại đúng cách tách đó.
- `build.py` ghi thêm **`stories.json`** (schema `word-stories/1`): mỗi truyện có `id`, `series`, `title`, `sents` (mọi câu theo thứ tự số câu, giữ `**từ mới**`). Từ điển (`typing-app/tools/build_dictionary.py`, mục "In the stories" trên thẻ) và trang ngữ pháp (`ielts-grammar/_web/build_site.py`) đọc file này khi dựng. Sửa truyện xong thì chạy `build.py` trước, rồi mới dựng lại hai trang kia.
- Bộ truyện (series) khai trong `SERIES` ở đầu `build.py` (mã, tên, mẫu mã truyện). Thêm bộ mới chỉ cần thêm một dòng; từ điển tự nhận khi dựng lại. Chỉ đưa câu tiếng Anh của truyện vào `sents` (không đưa dòng dịch hay phần luyện tập), và số câu trong `sents` phải khớp số câu trên trang.

## Trang đọc (2026-11-24)

- **Chạm vào bất kỳ từ nào** để tra: thẻ hiện ở đáy màn hình, gồm từ gốc (`stood → stand`), IPA, nghĩa Việt, định nghĩa, ví dụ, nút 🔊 giọng Jon của từ điển, link Dictionary và Cambridge, dòng "Also in N other stories" (chỉ với từ chưa biết, bấm để sang truyện đó và từ đó nhấp nháy), và câu đang đọc kèm "Vietnamese (paragraph)" (truyện My day), "Google Translate (sentence)", "Ask AI".
- Màu: **xanh đậm** = từ mới của truyện này (ẩn trong Review); xanh gạch chấm = từ chưa biết (status `new` trong `words.tsv`) nhưng thuộc truyện khác. Chữ viết hoa giữa câu là tên riêng, không tô.
- Thứ tự tra: dữ liệu từ điển (`data.js`) → bảng "Extra words" của truyện → báo "not in your dictionary" kèm Google Translate, Cambridge. Từ không có được ghi vào danh sách "Missing words" ở cuối truyện (Show → Copy) để sau gửi AI thêm vào từ điển, W61+.
- **Chọn bài** (24/11/2026, thay ô chọn của điện thoại, vốn luôn mở ở bài 1): bấm tên bài trên thanh trên cùng mở bảng "Stories" (cả màn hình trên điện thoại, thẻ giữa màn hình trên máy tính). Bảng mở đúng chỗ bài đang đọc (tô xanh), có tab theo bộ truyện, tiêu đề nhóm W01…W60, ô tìm theo tên bài, số thứ tự, mã (W37, D012) hoặc một từ mới của bài, dấu ✓ cho bài đã mở (lưu ở localStorage `stories-seen`, tính từ ngày có tính năng này). Esc hoặc × để đóng.
- **Nút `Tap: look up` / `Tap: listen 🎧`** trên thanh trên cùng. Chế độ nghe: chạm một câu để đọc từ câu đó; muốn tra từ thì nhấn giữ. `▶ Listen` vẫn đọc cả truyện. Trên điện thoại, ô chọn giọng và tốc độ chỉ hiện ở chế độ nghe.
- Dữ liệu tra từ **không chép vào trang**: trang nạp `data.js` của từ điển khi chạy. Trên web: `/english-words-dictionary/data.js` (cùng địa chỉ gốc joyfulsteps.github.io). Mở file trên máy tính: `../typing-app/exports/dictionary/site/data.js`. Audio cũng vậy (`audio/<s>.mp3`). Trên điện thoại, trang đọc audio mà từ điển đã lưu (cache `dict-audio-v1`, nút "Save all" của từ điển), nên không cần mạng.
- `build.py` chỉ ghi vào trang một chỉ mục nhỏ `WORDS`: `lex` (dạng từ → từ gốc), `unk` (dạng từ chưa biết), `seen` (từ chưa biết → các truyện có nó). Logic nằm trong `_tools/lexicon.py`.
- `sw.js`: chạy offline trên điện thoại. File của trang: lấy mạng trước, mất mạng thì dùng bản đã lưu. `data.js` của từ điển: dùng bản đã có trong máy trước. Không đụng tới audio.
- Thử trên máy: server `stories-with-dictionary` trong `D:\English\.claude\launch.json` (phục vụ cả `D:\English`), mở `http://localhost:8790/stories/index.html`.

## Bộ truyện "My day" (D001…, từ 2026-11-24)

Truyện đời thường của **chính người đọc**, kể bằng "I", thì hiện tại, để đi đường hay làm gì cũng nghĩ được bằng tiếng Anh. 250–420 chữ, trình độ A2–B1. **Không có danh sách từ**: viết tự nhiên, nhưng chủ động đưa từ chưa biết hợp cảnh vào (khoảng 15–25 từ). `build.py` tự in đậm mọi từ chưa biết.

Thế giới truyện (theo đời thật của người dùng; trang công khai nên **không dùng tên thật của người nhà**, chỉ gọi my dad, my mom, my sister, các cháu dùng tên giả; không ghi gì chi tiết hơn tên Trạm Trôi, Ba Vì, Hà Nam):
- "I": developer backend Java, ở trọ một mình ở **Tram Troi** (Hoài Đức, Hà Nội), đi làm bằng xe máy qua **Highway 32**.
- Quê **Ba Vi** (đồng lúa, không phải vùng bò sữa). Bố thợ xây. Mẹ may vá, làm ruộng, giờ lên trông con thứ hai (6 tháng) cho chị gái làm kế toán; con đầu của chị học mẫu giáo lớn. Chị kia ở **Ha Nam**, có 2 con gái (lớp 2 và lớp 4). Bà nội ở nhà chú.
- **Bit**: robot nhỏ "I" tự làm (cỡ nồi cơm điện, một mắt tròn xanh, hai bánh xe), học tiếng Anh trên mạng nên hiểu thành ngữ theo nghĩa đen. Nhân vật riêng, không dùng nhân vật Doraemon.
- Mạch: ngoài đường · nhà và khu phố · developer · kinh tế và toán quanh mình · động vật, thiên nhiên · truyện cảm động · Bit. Idol của người dùng (GS Đỗ Quốc Anh, Ngô Bảo Châu, Vũ Hà Văn): chỉ nhắc kèm sự thật kiểm chứng được, **không bịa lời**.
- Viết tên Việt không dấu như báo tiếng Anh (Hanoi, Ba Vi, pho, banh mi), để giọng đọc tiếng Anh đọc được và để tra từ.

Đợt thử: D001 Red Light in Tram Troi (đường phố), D002 My Father's Hands (bố), D003 NullPointerException at 2 a.m. (dev), D004 Why Did My Pho Cost More? (kinh tế), D005 The Gecko on My Wall (động vật), D006 Bit and the Cats and Dogs (Bit).

24/11/2026 người dùng chốt **60 truyện** và giao viết hết. **Đã viết xong D007–D060 cùng ngày** (build sạch, mỗi truyện 400–525 chữ, 9–34 từ chưa biết). Thứ tự đi theo **một năm** ở Trạm Trôi (đông → Tết → xuân → hè → thu → gió mùa trở lại ở D060), xen kẽ các mạch:
- Đông: D007 The Northeast Monsoon · D008 My Landlady (bà Hoa) · D009 Code Review · D010 A Flat Tire on Highway 32 · D011 The Cat in My Alley (mèo Thuyền Trưởng/Captain) · D012 Homework on a Video Call (Mai, Na) · D013 Bit and "Break a Leg" · D014 Money That Grows (quy tắc 72) · D015 Laundry in Winter · D016 The Morning Market · D017 The Stand-up Meeting · D018 My Mother and the Baby · D019 Sparrows on the Wire · D020 Bit Cooks Dinner
- Tết: D021 Cleaning Before Tet · D022 The Price of Peach Blossoms · D023 The Bus Home to Ba Vi · D024 Tet at My Uncle's House (bà nội) · D025 Spring Damp · D026 Back to Work After Tet · D027 Bit and the Lucky Money
- Xuân, hè: D028 Ants in My Kitchen · D029 Planting Rice in Ba Vi · D030 The Ride-hailing Driver's Numbers · D031 The Lost Wallet · D032 Helping the Intern (Khoa) · D033 Karaoke Next Door · D034 The Lottery Stall (xác suất, nhắc Vũ Hà Văn) · D035 Frogs After the Rain · D036 Bit and the Heat · D037 Heatwave · D038 Power Cut · D039 English at Work · D040 My Sister the Accountant · D041 Summer Storm · D042 Mosquito Season · D043 The Barber Under the Tree (bố lên Hà Nội) · D044 Too Tired to Sleep · D045 Bit Spills the Beans
- Thu: D046 Opportunity Cost (nhắc GS Đỗ Quốc Anh, chỉ là người mình ngưỡng mộ) · D047 My Mother's Sewing Machine · D048 The Smell of Milk Flowers · D049 Night Food Street · D050 The Buffalo and the Ducks · D051 Harvest Day · D052 How Many Motorbikes? (ước lượng) · D053 Moving Day for Our Data · D054 Bit and the Moon Festival · D055 Why, Why, Why? (Bi) · D056 Sunrise on Ba Vi Mountain · D057 The Dog Next Door (chó Mực/Muc) · D058 Payday · D059 A Call from My Grandmother · D060 One Year in Tram Troi

Nhân vật phụ (tên giả): đồng nghiệp Linh (developer lâu năm), Đức/Duc (tester), trưởng nhóm (nữ, không tên), Tuấn; bà chủ trọ Hoa; ông cụ nhà bên có chó Mực. Người kể **không có giới tính** trong truyện: không dùng son/daughter, không để ai gọi "anh/chị" riêng một bên (bản dịch viết "anh/chị", "cậu/dì"); tránh cả những cảnh lộ giới tính (đi thợ cắt tóc nam, chuyện hẹn hò, cưới xin).

Từ điển chỉ có **một nghĩa** cho mỗi từ, nên khi viết tránh dùng từ ở nghĩa khác. Đã gặp: nail (móng tay, không phải đinh), degree (bằng cấp), interest (sự quan tâm), compound (khu), deposit (gửi tiền, không phải tiền cọc), porridge (cháo yến mạch), steam (hấp), straw (ống hút), tap (vòi nước), lap (vòng đua), jam (mứt, không phải tắc đường), pole (cực), lighter (bật lửa), giant (người khổng lồ), cleaner (người dọn dẹp), checked (kẻ ô), pick (chọn, không phải pick up), leaves (lá cây, kể cả khi là động từ "she leaves"), server (người phục vụ), conditioner (dầu xả), shift (sự thay đổi), steps (bậc thềm), mode (mốt thống kê), migration (di cư), joint (chung), colony (thuộc địa), wine (rượu vang), bangs (tóc mái), tight (chật), matches (diêm), state (bang), rough (gồ ghề), rush (vội vàng), sack (sa thải), endangered. Số có gạch nối (twenty-four) và dạng -er/-est gấp đôi phụ âm (hotter, fatter, bigger) không tra được: viết số bằng chữ số, đổi cách nói. Script kiểm tra nghĩa từ in đậm: đọc `index.html`, in `new` của từng truyện D (w = vi).

Không biết giới tính hai cháu của chị làm kế toán (con đầu 5 tuổi, con thứ hai 6 tháng): trong truyện gọi bằng tên giả hoặc "the baby", **không dùng he/she**. Hai cháu gái ở Hà Nam dùng tên giả Mai (lớp 4) và Na (lớp 2).

Định dạng file `text/D001.md`:
```
# Tiêu đề
Đoạn tiếng Anh…
= Bản dịch tiếng Việt của đoạn đó (ẩn trên trang, nút VI)

## Say it yourself
- Câu dùng được ngay. = Câu tiếng Việt.
! Việc nhỏ để làm ngoài đời (Your turn). = Tiếng Việt.

## Extra words
honk | v | bấm còi
```
`build.py` báo `!!` nếu truyện có từ không nằm trong từ điển mà chưa có trong "Extra words" (tên riêng viết hoa, số đếm, dạng rút gọn như don't thì bỏ qua). Khi build xong, xem danh sách từ in đậm của truyện: nếu từ điển cho nghĩa khác nghĩa trong câu (ví dụ "night shift" ≠ shift "sự thay đổi"), đổi cách viết câu.

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
