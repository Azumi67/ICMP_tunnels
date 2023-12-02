![R (2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/a064577c-9302-4f43-b3bf-3d4f84245a6f)
نام پروژه : تانل های ICMP با پورت فوروارد و ریورس تانل FRP
---------------------------------------------------------------
----------------------------------
![Update-Note--Arvin61r58](https://github.com/Azumi67/ICMP_tunnels/assets/119934376/4a7b736f-1a86-4733-b86e-b635ea5297d9) **اپدیت**
- به جدیدترین نسخه اپدیت شد و از arm64 هم پشتیبانی میکند.
- ریستارت تایمر 6 ساعته برای تانل FRP اضافه شد.
- تغییرات در کامند ها داده شده که کمتر cpu را درگیر کند. به هنگام تست اسپید تست، cpu تا 55 درصد اشغال میشود.
-  تعداد tcp window تا 3.5 برابر کمتر شده است تا cpu را کمتر درگیر کند. این باعث میشه کانکشن شما کمی کندتر شود اما مشکل cpu کمتر دیده شود.
- پورت استفاده شده در پینگ تانل و FRP ، پورت 443 میباشد و در هر دو طرف تانل از کلید استفاده شده است.
- در پینگ تانل در صورت استفاده ار تک پورت، پورت تانل به صورت پیش فرض 443 خواهد بود اما در تعداد بالاتر پورت ها، پورت لوکال ، هم سان با پورت کانفیگ خارج خواهد بود.
- در socat امکان انتخاب پورت ها توسط شما وجود دارد و پیش فرض نمیباشد.
- پورت های دیفالت بیشتر برای راحت تر کردن کانفیگ ها استفاده شده است ( چون خیلی ها میگفتن اسکریپت ها جالب نیست و سخته). اگر فکر میکنید پورت های دیفالت مشکل ساز هستن ، باید تغییرات زیادی رو انجام بدم.
-----------
**توضیح کوتاه در مورد این پروژه :**

- در این اسکریپت 3 مدل تانل ICMP قرار دادم که بوسیله سوکت و haproxy امکان پورت فوروارد و همچنین استفاده از ریورس تانل هم فراهم شده است.
- در یکی از تانل های ICMP، امکان تانل بر روی ایپی 6 هم امکان پذیر میباشد و همچنین استفاده از 10 کانفیگ همزمان وجود دارد.
- با سوکت امکان پورت فوروارد TCP , UDP فراهم شده است
- با Haproxy امکان مولتی پورت فراهم شده است و تنها از TCP پشتیبانی میکند.
- من در وقت آزاد این را درست کردم و ممکن است اشتباهاتی هم داخلش باشد. پیشاپیش ببخشید.
- خودم تمام روش ها را داخل سرور های مختلف تست کردم و جواب داده . بر روی دبیان 12 و اوبونتو 20 تست شده است.
- اگر از پنل v2ray استفاده میکنید، لطفا ایپی پرایوت ها را باز کنید.
- پنل شما در خارج باید نصب شده باشد
- مناسب برای وایرگارد و V2ray و Openvpn
- لطفا اگر تنها برای یک کانفیگ میخواهید، تانل را انجام دهید تعداد کانفیگ خود را به درستی وارد نمایید.
- لطفا برای کانفیگ دوباره، نخست از منوی uninstall اقدام به حذف تانل یا پورت فوروارد ها کنید تا مشکلی پیش نیاید.
- برای راحتی شما تعدادی از پورت ها به صورت دیفالت انتخاب شده است
- در آخر هر کانفیگ، ایپی 4 سرور ایران شما با پورت نهایی نمایش داده میشود که با استفاده از آن در کلاینت وایرگارد یا V2ray میتوانید به اینترنت متصل شوید.

------------------------
![307981](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/39b2794b-fd04-4ae5-baea-d4b66138766e)
 **فهرست :**


 ----------------------

- **دسترسی سریع به اسکریپت** >> **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%A7%D8%B3%DA%A9%D8%B1%DB%8C%D9%BE%D8%AA-%D9%85%D9%86)**
- **امکانات** >> **[کلیک](https://github.com/Azumi67/ICMP_tunnels/tree/main#%D8%A7%D9%85%DA%A9%D8%A7%D9%86%D8%A7%D8%AA)**
- **آموزش** : 
- **تانل Pingtunnel با IPV4 و TCP - تک پورت** >> **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-pingtunnel-%D8%A8%D8%A7-ipv4-%D9%88-tcp---%D8%AA%DA%A9-%D9%BE%D9%88%D8%B1%D8%AA)**
-  **تانل Pingtunnel با IPV4 و TCP - مولتی پورت** >> **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-pingtunnel-%D8%A8%D8%A7-ipv4-%D9%88-tcp---%D9%85%D9%88%D9%84%D8%AA%DB%8C-%D9%BE%D9%88%D8%B1%D8%AA)**
-  **تانل Pingtunnel با IPV6 و TCP - مولتی پورت** >> **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-pingtunnel-%D8%A8%D8%A7-ipv6-%D9%88-tcp---%D9%85%D9%88%D9%84%D8%AA%DB%8C-%D9%BE%D9%88%D8%B1%D8%AA)**
- **تانل Pingtunnel با IPV4 و UDP - تک پورت** >>  **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-pingtunnel-%D8%A8%D8%A7-ipv4-%D9%88-udp---%D8%AA%DA%A9-%D9%BE%D9%88%D8%B1%D8%AA)**
- **تانل Pingtunnel با IPV6 و UDP - تک پورت**  >>  **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-pingtunnel-%D8%A8%D8%A7-ipv6-%D9%88-udp---%D8%AA%DA%A9-%D9%BE%D9%88%D8%B1%D8%AA)**
- **تانل Icmptunnel همراه با Socat UDP - تک پورت**  >>  **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-icmptunnel-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%A8%D8%A7-socat-udp---%D8%AA%DA%A9-%D9%BE%D9%88%D8%B1%D8%AA)**
- **تانل HANS همراه با Socat TCP - تک پورت**  >>  **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-hans-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%A8%D8%A7-socat-tcp---%D8%AA%DA%A9-%D9%BE%D9%88%D8%B1%D8%AA)**
- **تانل HANS همراه با Haproxy TCP - مولتی پورت**  >>  **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-hans-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%A8%D8%A7-haproxy-tcp---%D9%85%D9%88%D9%84%D8%AA%DB%8C-%D9%BE%D9%88%D8%B1%D8%AA)**
- **تانل HANS همراه با ریورس تانل FRP - مولتی پورت - TCP**  >>  **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-hans-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%A8%D8%A7-%D8%B1%DB%8C%D9%88%D8%B1%D8%B3-%D8%AA%D8%A7%D9%86%D9%84-frp---%D9%85%D9%88%D9%84%D8%AA%DB%8C-%D9%BE%D9%88%D8%B1%D8%AA---tcp)**
- **تانل Icmptunnel همراه با ریورس تانل FRP - مولتی پورت - UDP**  >>  **[کلیک](https://github.com/Azumi67/ICMP_tunnels#%D8%AA%D8%A7%D9%86%D9%84-icmptunnel-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%A8%D8%A7-%D8%B1%DB%8C%D9%88%D8%B1%D8%B3-%D8%AA%D8%A7%D9%86%D9%84-frp---%D9%85%D9%88%D9%84%D8%AA%DB%8C-%D9%BE%D9%88%D8%B1%D8%AA---udp)**
     
     
     

------------------------
![check](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/13de8d36-dcfe-498b-9d99-440049c0cf14)
**امکانات**
-

- تانل ICMP با سه روش متفاوت و امکان استفاده هم زمان از پورت فوروارد و تانل ریورس FRP
- پشتیبانی از TCP و UDP
- قابلیت تانل تک پورت و چندین پورت TCP و UDP
- مناسب برای V2ray و Openvpn و Wireguard
- قابلیت تانل ICMP و پورت فوروارد سوکت - TCP و UDP 
- قابلت تانل ICMP و مولتی پورت با استفاده ازHaproxy - از TCP پشتیبانی میکند
- تانل ICMP با استفاده از IPV4 | IPV6 و پشتیبانی از 10 کانفیگ - از TCP و UDP پشتیبانی میکند
- تانل ICMP و استفاده همزمان از ریورس تانل FRP - از TCP و UDP پشتیبانی میکند
- قابلیت مشاهده جداگانه تمامی سرویس ها
- امکان حذف تمامی تانل ها و سرویس ها به صورت جداگانه

 ------------------------------------------------------

![147-1472495_no-requirements-icon-vector-graphics-clipart](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/98d8c2bd-c9d2-4ecf-8db9-246b90e1ef0f)
 **پیش نیازها**

 - لطفا سرور اپدیت شده باشه.
 - میتوانید از اسکریپت اقای [Hwashemi](https://github.com/hawshemi/Linux-Optimizer) و یا [OPIRAN](https://github.com/opiran-club/VPS-Optimizer) هم برای بهینه سازی سرور در صورت تمایل استفاده نمایید. (پیش نیاز نیست)


----------------------------

  
  ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش**
-
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل Pingtunnel با IPV4 و TCP - تک پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : PingTunnel ICMP > KHAREJ > IPV4**


 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/8f5cfd6e-b052-4f23-8bc3-cbe40038f91f" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- من یک کانفیگ vmess با پورت 8080 دارم پس پورت خارج را 8080 قرار میدم.
- چون یک عدد کانفیگ دارم ، عدد 1 را برای تعداد کانفیگ قرار دادم. شما اگر تعداد بیشتری کانفیگ دارید عدد دیگری را قرار دهید.
- خب کانفیگ در سرور خارج تمام شده است.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : PingTunnel ICMP > IRAN > IPV4 TCP**

<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/83d98e1f-a23b-4b97-a959-cec0f70785d0" alt="Image" />
</p>


- گزینه IPV4 TCP را برای ایران انتخاب میکنیم. در این کانفیگ میخواهیم بر روی تک پورت، تانل را انجام دهیم
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- ایپی 4 سرور خارج را وارد میکنم
- پورت کانفیگ خارج هم 8080 بود
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت V2ray استفاده نمایید.
- پورت دیفالت برای کانفیگ تک پورت، به صورت پیش فرض بر روی 443 قرار دارد

------------------

  ![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1b367bc9-aaed-4a8d-84a6-a2a1fc31b831)**نکات**
  
  - در کانفیگ های مولتی پورت یا چندین کانفیگ، پورت سمت ایران هم باید خودتان انتخاب کنید اما من پورت لوکال را مانند پورت خارج به صورتپیش فرض قرار داده ام.
  - به عبارتی اگر پورت خارج را 8080 وارد نمایید، پورت لوکال هم به صورت پیش فرض 808 خواهد بود. این کار برای راحتی کار انجام شده است.
  

--------------------------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل Pingtunnel با IPV4 و TCP - مولتی پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : PingTunnel ICMP > KHAREJ > IPV4**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/02669a0a-b481-4886-b03a-a8bb88745c4f" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- من دو کانفیگ vmess با پورت 8080 و 8081 دارم پس تعداد کانفیگ را 2 قرار میدم و پورت کانفیگ اول را 8080 و پورت کانفیگ دوم را 8081 قرار میدم
- چون 2 عدد کانفیگ دارم ، عدد 2 را برای تعداد کانفیگ قرار دادم. شما اگر تعداد بیشتری کانفیگ دارید عدد دیگری را قرار دهید.
- خب کانفیگ در سرور خارج تمام شده است.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : PingTunnel ICMP > IRAN > IPV4 TCP**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/785abaa8-0fc0-48ad-bc52-6d7c7387e105" alt="Image" />
</p>


- گزینه IPV4 TCP را برای ایران انتخاب میکنیم. در این کانفیگ میخواهیم بر روی دو پورت، تانل را انجام دهیم. اگر شما تعداد بیشتری پورت دارید، عدد دیگری را انتخاب نمایید
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- ایپی 4 سرور خارج را وارد میکنم
- پورت های کانفیگ خارج هم 8080 و 8081 بود
- من از پورت یکسان در سمت خارج و ایران استفاده نمودم. لوکال پورت، پورت سمت سرور ایران میباشد و این پورت، پورت نهایی شما میباشد و پورت لوکال به صورت پیش فرض انتخاب میشود.
- شما فقط کافیه پورت خارج را وارد نمایید.
- در آخر، ایپی سرور ایرانتان با پورت های مورد نظر را مشاهده میکنید. از این ادرس ها میتوانید در کلاینت V2ray استفاده نمایید.


------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل Pingtunnel با IPV6 و TCP - مولتی پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : PingTunnel ICMP > KHAREJ >IPV6**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/02669a0a-b481-4886-b03a-a8bb88745c4f" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- از ایپی ورژن 6 میخواهیم استفاده کنیم
- من دو کانفیگ vmess با پورت 8080 و 8081 دارم پس تعداد کانفیگ را 2 قرار میدم و پورت کانفیگ اول را 8080 و پورت کانفیگ دوم را 8081 قرار میدم
- چون 2 عدد کانفیگ دارم ، عدد 2 را برای تعداد کانفیگ قرار دادم. شما اگر تعداد بیشتری کانفیگ دارید عدد دیگری را قرار دهید.
- خب کانفیگ در سرور خارج تمام شده است.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : PingTunnel ICMP > IRAN >IPV6 TCP**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/c90e6a0d-41c0-4045-a8f5-1959881cc231" alt="Image" />
</p>


- گزینه IPV6 TCP را برای ایران انتخاب میکنیم. در این کانفیگ میخواهیم بر روی دو پورت، تانل را انجام دهیم. اگر شما تعداد بیشتری پورت دارید، عدد دیگری را انتخاب نمایید
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- ایپی 4 سرور خارج را وارد میکنم و سپس ایپی ورژن 6 خارج را وارد مینماییم
- پورت های کانفیگ خارج هم 8080 و 8081 بود
- من از پورت یکسان در سمت خارج و ایران استفاده نمودم. لوکال پورت، پورت سمت سرور ایران میباشد و این پورت، پورت نهایی شما میباشد و پورت لوکال به صورت پیش فرض انتخاب میشود.
- شما فقط کافیه پورت خارج را وارد نمایید.
- در آخر، ایپی سرور ایرانتان با پورت های مورد نظر را مشاهده میکنید. از این ادرس ها میتوانید در کلاینت V2ray استفاده نمایید.


--------------------------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل Pingtunnel با IPV4 و UDP - تک پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : PingTunnel ICMP > KHAREJ > IPV4**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/a77e4553-49f9-4fe0-9bab-ae6e9f404d98" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- من یک کانفیگ وایرگارد با پورت 50824 دارم و میخواهم این تانل را انجام دهم.
- پورت خارج را عدد 50824 میذارم.
- چون 1 عدد کانفیگ دارم ، عدد 1 را برای تعداد کانفیگ قرار دادم. شما اگر تعداد بیشتری کانفیگ دارید عدد دیگری را قرار دهید.
- خب کانفیگ در سرور خارج تمام شده است.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : PingTunnel ICMP > IRAN > IPV4 UDP**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/57c6d2a1-2f17-4532-91fb-1eb9128e6d9c" alt="Image" />
</p>


- گزینه IPV4 UDP را برای ایران انتخاب میکنیم. در این کانفیگ میخواهیم بر روی 1 پورت، تانل را انجام دهیم. اگر شما تعداد بیشتری پورت دارید، عدد دیگری را انتخاب نمایید
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- ایپی 4 سرور خارج را وارد میکنم
- پورت کانفیگ خارج هم 50824 بود
- درکانفیگ تک پورت، به صورت پیش فرض از پورت 443 استفاده شده است.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت Wireguard استفاده نمایید.


------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل Pingtunnel با IPV6 و UDP - تک پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : PingTunnel ICMP > KHAREJ > IPV6**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/a77e4553-49f9-4fe0-9bab-ae6e9f404d98" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- من یک کانفیگ وایرگارد با پورت 50824 دارم و میخواهم این تانل را انجام دهم.
- پورت خارج را عدد 50824 میذارم.
- چون 1 عدد کانفیگ دارم ، عدد 1 را برای تعداد کانفیگ قرار دادم. شما اگر تعداد بیشتری کانفیگ دارید عدد دیگری را قرار دهید.
- خب کانفیگ در سرور خارج تمام شده است.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : PingTunnel ICMP > IRAN > IPV6 UDP**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/f17bb882-2eee-4cde-9256-428761955e1c" alt="Image" />
</p>


- گزینه IPV6 UDP را برای ایران انتخاب میکنیم. در این کانفیگ میخواهیم بر روی 1 پورت، تانل را انجام دهیم. اگر شما تعداد بیشتری پورت دارید، عدد دیگری را انتخاب نمایید
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- ایپی 4 سرور خارج را وارد میکنم
- پورت کانفیگ خارج هم 50824 بود
- درکانفیگ تک پورت، به صورت پیش فرض از پورت 443 استفاده شده است.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت Wireguard استفاده نمایید.
- اگر میخواهید چندین پورت استفاده نمایید مانند مثال بالاتر > TCP مولتی پورت، عمل کنید.


------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل Icmptunnel همراه با Socat UDP - تک پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : Icmptunnel > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/57c70b57-1386-4f01-a915-5a450ed69dee" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- کار خاصی نیازنیست در سرور خارج انجام دهید و سرور خودش کانفیگ میشود.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Icmptunnel > IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/86e4a96d-bd28-40e5-98c6-6f2fa0f2157d" alt="Image" />
</p>


- ایپی 4 سرور خارج را میدهیم تا ارتباط تانل برقرار شود.
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- سپس از بین SOCAT و HAPROXY ، من سوکت را انتخاب میکنم چون میخوام پورت UDP را فوروارد کنم.
- با سوکت میتوان پورت TCP هم فوروارد کرد.
- پورت کانفیگ خارج هم 50824 بود
- پورت لوکال، پورتی است که در سمت ایران وارد مینمایید. من پورت 443 را قرار میدم.
- در کلاینت وایرگارد من به جای 50824 از 443 استفاده خواهد کرد
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت Wireguard استفاده نمایید.


------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل HANS همراه با Socat TCP - تک پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : Hans > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/57c70b57-1386-4f01-a915-5a450ed69dee" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- مانند icmtunnel کار خاصی نیاز نیست در سرور خارج انجام دهید و سرور خودش کانفیگ میشود.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Hans > IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/a8296ed3-dbbd-484c-bae6-1f191b7bcba2" alt="Image" />
</p>


- ایپی 4 سرور خارج را میدهیم تا ارتباط تانل برقرار شود.
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- سپس از بین SOCAT و HAPROXY ، من سوکت را انتخاب میکنم و تک پورت TCP را فوروارد میکنم.
- من یک کانفیگ vmess با پورت 8080 دارم پس پورت خارج من 8080 میباشد.
- پورت لوکال، پورتی است که در سمت ایران وارد مینمایید. من پورت 443 را قرار میدم.
- پس در کلاینت v2rayng من به جای 8080 از 443 استفاده خواهد کرد.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت V2rayng استفاده نمایید.


------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل HANS همراه با Haproxy TCP - مولتی پورت**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : Hans > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/57c70b57-1386-4f01-a915-5a450ed69dee" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- مانند icmtunnel کار خاصی نیاز نیست در سرور خارج انجام دهید و سرور خودش کانفیگ میشود.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Hans > IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/2c59c7ee-50e9-46c6-8af2-e0e1c1f60761" alt="Image" />
</p>


- ایپی 4 سرور خارج را میدهیم تا ارتباط تانل برقرار شود.
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- سپس از بین SOCAT و HAPROXY ، من Haproxy را انتخاب میکنم و دو عدد پورت TCP را فوروارد میکنم.
- من دو کانفیگ vmess با پورت 8080 و 8081 دارم پس پورت های خارج من 8080 و 8081 میباشد.
- پورت لوکال، پورتی است که در سمت ایران وارد مینمایید. من پورت 443 را به صورت پیش فرض قرار دادم. شما نیازی نیست انتخاب کنید.
- در آخر، ایپی سرور ایرانتان با پورت های مورد نظر را مشاهده میکنید. از این ادرس ها میتوانید در کلاینت V2rayng استفاده نمایید.

![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/ICMP_tunnels/assets/119934376/0ad5704c-24a5-40b1-8701-2cb98bba162c)**نکته**

- شما میتوانید از این نمونه ها استفاده کنید تا مدل های دیگر تانل و پورت فوروارد هم انجام دهید.


------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل HANS همراه با ریورس تانل FRP - مولتی پورت - TCP**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر :  FRP TCP ICMPs > Hans icmps + frp > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/2bd4e136-1365-4eef-a7d8-2384b3e8ad89" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم با اینکه همیشه در ریورس تانل FRP از سرور ایران شروع میکردیم.
- پس از نصب تانل Hans، از ما سوال میشود که چند کانفیگ داریم. من دو عدد کانفیگ با پورت های 8080 و 8081 دارم پس عدد 2 را وارد میکنم.
- من برای remote port و local port از پورت یکسان استفاده میکنم. شما میتوانید از پورت متفاوت استفاده کنید
- پورت ریورس تانل FRP به صورت پیش فرض 443 میباشد.
- دقت کنید در آخر از شما سوال میشود که ایا کانفیگ سرور ایران تمام شده است یا خیر. پس از انکه سرور ایران را کانفیگ کردید به این صفحه برگردید و گزینه y را بزنید تا تانل شما فعال شود در غیر اینصورت کار نخواهد کرد.

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر :  FRP TCP ICMPs > Hans icmps + frp > IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/1d2efcc1-896f-45a8-b10f-c4b8acea91ea" alt="Image" />
</p>


- ایپی 4 سرور خارج را میدهیم تا ارتباط تانل برقرار شود.
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- پورت های کانفیگ من در سرور خارج 8080 و 8081 بود، پس همان ها را وارد میکنم.
- من برای remote port و local port از پورت یکسان استفاده میکنم. شما میتوانید از پورت متفاوت استفاده کنید
- بین هر پورت از کاما [ , ] استفاده میکنم.
- پس از نهایی شدن کانفیگ سرور ایران ، به سرور خارج برگردید و گرینه y را بزنید تا تانل برقرار شود.
- برای UDP هم مانند همین نمونه، انجام دهید.

---------------------


![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/1b367bc9-aaed-4a8d-84a6-a2a1fc31b831)**نکات**
  
  - در صورت ریبوت شدن سرور ایران ، یک ایپی جدید برای تانل Hans انتخاب میشود و این باعث میشود که در تانل شما اختلال پیش بیاید.
  - دقت نمایید این مشکل در تانل HANS است و تنها در صورتی اتفاق میوفتد که سرور ایران ریبوت شود و خارج ریبوت نشود.
  - راه ساده  : با ریبوت کردن سرور خارج و ایران، مشکل حل میشود.(این روش ساده تر است)
  
------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل Icmptunnel همراه با ریورس تانل FRP - مولتی پورت - UDP**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر :  FRP UDP ICMPs > Icmptunnel + frp > Kharej**


 <p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/16bf33a2-d215-4c57-98dc-382ad55d47fb" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم با اینکه همیشه در ریورس تانل FRP از سرور ایران شروع میکردیم.
- در این تانل میتوان چندین پورت را تانل کرد اما من تک پورت را به عنوان نمونه نشان میدم.
- پس از نصب تانل Icmptunnel، از ما سوال میشود که چند کانفیگ داریم. من 1 عدد کانفیگ با پورت 50824 دارم پس عدد 1 را وارد میکنم.
- من برای remote port و local port از پورت یکسان 50824 استفاده میکنم. شما میتوانید از پورت متفاوت استفاده کنید
- پورت ریورس تانل FRP به صورت پیش فرض 443 میباشد.
- دقت کنید در آخر از شما سوال میشود که ایا کانفیگ سرور ایران تمام شده است یا خیر. پس از انکه سرور ایران را کانفیگ کردید به این صفحه برگردید و گزینه y را بزنید تا تانل شما فعال شود در غیر اینصورت کار نخواهد کرد.

----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر :  FRP UDP ICMPs > Icmptunnel + frp > IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/c28fe423-9847-41e6-ae22-a632c752e3ee" alt="Image" />
</p>


- ایپی 4 سرور خارج را میدهیم تا ارتباط تانل برقرار شود.
- خود اسکریپت پیش نیاز ها را دانلود میکند.
- پورت کانفیگ من در سرور خارج 50824 بود. پس همان را وارد میکنم.
- من برای remote port و local port از پورت یکسان استفاده میکنم. شما میتوانید متفاوت استفاده کنید
- بین هر پورت از کاما [ , ] استفاده میکنم.
- پس از نهایی شدن کانفیگ سرور ایران ، به سرور خارج برگردید و گرینه y را بزنید تا تانل برقرار شود.
- برای TCP هم مانند همین نمونه، انجام دهید.

------------------
**اسکرین شات**


<details>
  <summary align="right">Click to reveal image</summary>
  
  <p align="right">
    <img src="https://github.com/Azumi67/ICMP_tunnels/assets/119934376/616afd12-6c29-438c-b5b3-00886908d0d8" alt="menu screen" />
  </p>
</details>


------------------------------------------
![scri](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/cbfb72ac-eff1-46df-b5e5-a3930a4a6651)
**اسکریپت های کارآمد :**
- این اسکریپت ها optional میباشد.


 
 Opiran Script
```
apt install curl -y && bash <(curl -s https://raw.githubusercontent.com/opiran-club/VPS-Optimizer/main/optimizer.sh --ipv4)
```

Hawshemi script

```
wget "https://raw.githubusercontent.com/hawshemi/Linux-Optimizer/main/linux-optimizer.sh" -O linux-optimizer.sh && chmod +x linux-optimizer.sh && bash linux-optimizer.sh
```

-----------------------------------------------------
![R (a2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/716fd45e-635c-4796-b8cf-856024e5b2b2)
**اسکریپت من**
----------------
- اگر با دستور دوم نتوانستید اسکریپت را اجرا کنید، نخست دستور زیر را اجرا نمایید و سپس دستور اصلی اسکریپت را اجرا نمایید.(تنها زمانی این دستور را استفاده کنید که با دستور دوم موفق به اجرای اسکریپت نشدید)

```
sudo apt-get install python-pip -y  &&  apt-get install python3 -y && alias python=python3 && python -m pip install colorama && python -m pip install netifaces
```
- سپس این دستور را اجرا نمایید.
```
sudo apt-get install python3 -y && apt-get install wget -y && apt-get install python3-pip -y && pip3 install colorama && pip3 install netifaces && apt-get install curl -y && python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/ICMP_tunnels/main/icmp.py --ipv4)
```
--------------------------------------
 <div dir="rtl">&bull;  دستور زیر برای کسانی هست که پیش نیاز ها را در سرور، نصب شده دارند</div>
 
```
python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/ICMP_tunnels/main/icmp.py --ipv4)
```
--------------------------------------
 <div dir="rtl">&bull; اگر سرور شما خطای externally-managed-environment داد از دستور زیر اقدام به اجرای اسکریپت نمایید.</div>
 
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Azumi67/ICMP_tunnels/main/managed.sh)"
```

---------------------------------------------
![R (7)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/42c09cbb-2690-4343-963a-5deca12218c1)
**تلگرام** 
![R (6)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/f81bf6e1-cfed-4e24-b944-236f5c0b15d3) [اپیران- OPIRAN](https://github.com/opiran-club)

---------------------------------
![R23 (1)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/18d12405-d354-48ac-9084-fff98d61d91c)
**سورس ها**


![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس  Pingtunnel](https://github.com/esrrhs/pingtunnel)

![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس  icmptunnel](https://github.com/jamesbarlow/icmptunnel)

![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس  hans](https://github.com/friedrich/hans)

![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس  OPIRAN](https://github.com/opiran-club)

![R (9)](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4758a7da-ab54-4a0a-a5a6-5f895092f527)[سورس  Hwashemi](https://github.com/hawshemi/Linux-Optimizer)



-----------------------------------------------------

![youtube-131994968075841675](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/24202a92-aff2-4079-a6c2-9db14cd0ecd1)
**ویدیوی آموزش**

-----------------------------------------


