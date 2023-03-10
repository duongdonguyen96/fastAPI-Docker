import random
import smtplib
import imghdr
from email.message import EmailMessage
import os


list_content = [
    "Chúc ngủ ngon là một nghệ thuật và người chúc là một nghệ sĩ. Người được chúc ngủ ngon hôm nay là một cô nàng cực đáng yêu trong lòng tôi. Chúc em yêu có giấc mơ đẹp nhé! <3",
    "Hãy mang tất cả những niềm vui của ngày hôm nay vào trong giấc ngủ để có thể mơ thấy thật nhiều điều hạnh phúc em nhé! Mãi yêu em <3 <3 <3 <3",
    "Cả ngày hôm nay bận rộn không có thời gian dành cho em, thông cảm cho anh nhé. Em biết là anh nhớ em rất nhiều mà đúng không? Chúc em yêu có những giấc mơ đẹp và biến nó thành hiện thực nhé <3",
    "Khi anh cô đơn trong đêm và nhìn lên những ngôi sao tỏa sáng trên bầu trời. Điều duy nhất mà anh muốn nhìn thấy đó chính là em. Thiên thần của anh ngủ ngon nhé! <3",
    "Ở ngoài kia, có một người luôn nhớ tới em và mong em có những giấc mơ thật đẹp. Chúc ngủ ngon nhé, người tôi yêu <3",
    "Chúc em yêu của anh ngủ ngon. Dù xa em mỗi đêm nhưng anh sẽ vào trong giấc mơ và mang đến cho em những giấc mơ đẹp nhất",
    "Nếu anh ở bên cạnh em đêm nay thì anh sẽ ôm em thật chặt và bao bọc bởi tình yêu chân thành nhất. Chúc ngủ ngon nhé người yêu của anh.",
    "Chúc nàng công chúa của anh ngủ ngon bên giấc mộng đẹp. Đêm nay, những vì sao lấp lánh trên bầu trời sẽ mang mọi niềm hạnh phúc vào trong giấc mơ. Yêu em rất nhiều!",
    "Hôm nay đã có 3 người hỏi anh về em. Hy vọng rằng họ sẽ tìm thấy em nhanh nhất trong giấc mơ để ban đến những điều tốt đẹp. Đó chính là 3 vị thần về Sức mạnh, May mắn và Tình yêu. Chúc cô bé của anh ngủ thật ngon và sớm gặp được họ nhé!",
    "Hôm nay anh đã gặp một thiên thần và cô ấy ban cho anh một điều ước. Anh đã xin rằng người hãy chăm sóc cho em một cách tốt nhất. Nhưng cô ấy lại từ chối và nói rằng:” Một thiên thần không thể chăm sóc cho thiên thần khác.” Ngủ ngon nhé thiên thần của lòng anh!",
    "Chúc bé yêu của anh ngủ ngon và có những giấc mơ tuyệt vời. Một giấc mộng quên đi hết buồn phiền của ngày hôm nay và để ngày mai sẽ là một ngày mới đầy may mắn và tràn ngập niềm vui nhé!",
    "Trên Trái Đất có 7 tỷ người nhưng có 1 điều lạ là anh chỉ nhắn tin cho mỗi mình em. Có lẽ vì 6.999.999.999 người còn lại không thể thay thế được em. Giờ thì chúc cô bé của anh ngủ ngon và một ngày mới vui vẻ sẽ đến với em!",
    "Một ngày dài mệt mỏi, vất vả sắp kết thúc. Trước khi đặt mình lên giường, em phải hứa với anh rằng sẽ quẳng hết mọi muộn phiền, lo lắng và để lại những điều ngọt ngào, ấm áp nhất vào giấc ngủ nhé. Chúc em yêu ngủ ngon.",
    "Cô bé ngốc của anh à! Em có biết trên thế giới đang có 4,5 triệu người đang ngủ; 3.2 triệu người đang yêu. Nhưng chỉ có duy nhất 1 người đang đọc tin nhắn của anh. Chúc nàng công chúa của lòng anh ngủ ngon nhé!",
    "Em có biết là em sẽ bị triệu tập đến tòa vì đã bước vào giấc mơ và đánh cắp mất trái tim của anh. Em có lời gì biện hộ cho hành vi của mình không? Chúc em yêu ngủ ngon và sáng mai thức dậy trả lời cho anh nhé!",
    "Chúc cô bé của anh ngủ thật ngon và biến mọi điều trong giấc mơ thành sự thật nhé! ",
    "Em có thể làm giúp anh một việc quan trọng này được không? Hãy lên giường sớm, ngủ thật ngon và sáng mai thức dậy với một nụ cười trên môi nhé. Thương em! ",
    "Chúc em yêu ngủ thật ngon và mơ những giấc mộng đẹp nhất. Để rồi một ngày mới sẽ đến với em trong niềm hân hoan và hạnh phúc. Yêu em nhất trên đời!"
    "Chào bạn! Hiện tại, bạn đang có mặt trên chuyến bay của hãng hàng không “Sweet Dreams” của chúng tôi. Để đảm bảo an toàn bạn hãy nằm ngoan trên giường, nhắm mắt thật kỹ vì trong khoảng 5 phút nữa chuyến bay sẽ bắt đầu khởi hành. Hãy tận hưởng thời gian tuyệt vời này cùng tôi trong đêm nay bạn nhé!",
    "Đến giờ đi ngủ rồi đấy, hãy ngủ ngon và mơ về anh nhé! Đừng thức quá muộn bởi nó sẽ ảnh hưởng đến sức khỏe và làm em kém rạng rỡ đấy. Yêu em nhiều! ",
    "Nếu có phép màu ngay lúc này thì anh mong mình có thể đến bên và ôm em vào trong lòng. Nhẹ nhàng hôn lên trán em và khẽ nói câu: “ Chúc người anh thương ngủ ngon”.",
    "Chúc cô bé của anh có một giấc ngủ thật ngon bên những giấc mơ đẹp. Mong rằng, dù ngày mai có mệt mỏi thế nào thì tình yêu của anh sẽ là phương thuốc diệu kỳ giúp em quên đi mọi ưu phiền nhé. Yêu em!",
    "Những ngôi sao tỏa sáng lấp lánh trên bầu trời hôm nay chỉ xuất hiện để chúc em có một buổi tối tốt lành thôi đấy. Hãy để ánh sáng đấy dẫn đường cho những giấc mơ tuyệt vời khi em đi ngủ. Ngủ ngoan nhé cô bé của anh!",
]

list_subject = [
    "Chào người yêu bé nhỏ <3",
    "Chào bấy bì <3",
    "Chào đồng chí Thuyên <3",
    "Gửi em thương nhớ <3",
    "Tâm thư gửi em <3",
]

signature = "Người yêu em <3 <3 <3 <3 <3 <3"


sender = "duongdonguyen96@gmail.com"
receiver = "dtieuthuyen12@gmail.com"
password = "ngtnnoaqgrrigcuj"

newMessage = EmailMessage()
newMessage["Subject"] = random.choice(list_subject)
newMessage["From"] = sender
newMessage["To"] = receiver
newMessage.set_content(random.choice(list_content) + signature)

print("====== Lấy danh sách các ảnh======")
path = "C://Users//USER//Downloads//image"
files = os.listdir(path)
print(files)

print("======= Lấy ra 1 ảnh trong danh sách ảnh=====")
files = [random.choice(files)]
print(files)


print(".......... Loading.....!!!!!!")

for file in files:
    with open(path + "//" + file, "rb") as f:
        file_data = f.read()
        file_name = f.name
    newMessage.add_attachment(
        file_data, maintype="application", subtype="octet-stream", filename=file_name
    )

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(sender, password)
        smtp.send_message(newMessage)
except Exception as ex:
    print("_________________________________________________________")
    print(str(ex))

print("================================")
print("Send mail success!!!")
